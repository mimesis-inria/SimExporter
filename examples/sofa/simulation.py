from os.path import join, dirname
import numpy as np
import Sofa

from SimExporter.sofa import Exporter

file = lambda f: join(dirname(__file__), 'data', f)


class Simulation(Sofa.Core.Controller):

    def __init__(self, root: Sofa.Core.Node, exporter: Exporter, *args, **kwargs):
        """
        Simulation of a deformable SOFA logo.
        """

        Sofa.Core.Controller.__init__(self, name='PyController', *args, **kwargs)

        # The exporter will be used in the simulation init done event
        self.exporter = exporter

        # Create the scene graph: root node
        root.dt.value = 0.1
        with open(file('plugins.txt'), 'r') as f:
            required_plugins = [plugin[:-1] if plugin.endswith('\n') else plugin for plugin in f.readlines()
                                if plugin != '\n']
        root.addObject('RequiredPlugin', pluginName=required_plugins)
        root.addObject('VisualStyle', displayFlags='showVisualModels showBehaviorModels showForceFields')
        root.addObject('DefaultAnimationLoop')
        root.addObject('GenericConstraintSolver', maxIterations=10, tolerance=1e-3)
        root.addObject('CollisionPipeline')
        root.addObject('BruteForceBroadPhase')
        root.addObject('BVHNarrowPhase')
        root.addObject('DiscreteIntersection')
        root.addObject('DefaultContactManager')

        # Create the scene graph: logo object node
        root.addChild('logo')
        root.logo.addObject('EulerImplicitSolver', firstOrder=False, rayleighMass=0.1, rayleighStiffness=0.1)
        root.logo.addObject('CGLinearSolver', iterations=25, tolerance=1e-9, threshold=1e-9)
        root.logo.addObject('MeshVTKLoader', name='mesh', filename=file('volume.vtk'), rotation=[90, 0, 0])
        root.logo.addObject('TetrahedronSetTopologyContainer', name='topology', src='@mesh')
        root.logo.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
        root.logo.addObject('MechanicalObject', name='state', src='@topology')
        root.logo.addObject('TetrahedronFEMForceField', youngModulus=2000, poissonRatio=0.4, method='svd')
        root.logo.addObject('MeshMatrixMass', totalMass=0.01)
        root.logo.addObject('FixedConstraint', name='constraints', indices=np.load(file('constraints.npy')))

        # Create the scene graph: forces node
        root.logo.addChild('forces')
        root.logo.forces.addObject('MechanicalObject', name='state', src='@../topology')
        root.logo.forces.addObject('IdentityMapping')
        # Get the indices of the DOF to apply the forces
        indices = np.load(file('forces.npy'))
        n = {int(i): np.array([], dtype=int) for i in indices}
        for i in n.keys():
            idx = np.where(np.isin(root.logo.topology.triangles.value[:], i))[0]
            n[i] = np.unique(np.concatenate(root.logo.topology.triangles.value[idx]))
        clusters = []
        for idx, nei in n.items():
            if len(clusters) == 0:
                clusters.append([idx])
            else:
                new_cluster = True
                for i_c in range(len(clusters)):
                    if len(set(clusters[i_c]).intersection(set(nei))) > 0:
                        clusters[i_c].append(idx)
                        new_cluster = False
                        break
                if new_cluster:
                    clusters.append([idx])
        # Create ForceFields
        for i, cluster in enumerate(clusters):
            root.logo.forces.addObject('ConstantForceField', name=f'cff_{i}', indices=cluster,
                                       forces=np.random.choice([-0.5, 0.5], (3,)), showArrowSize=1)

        # Create the scene graph: collision node
        root.logo.addChild('collision')
        root.logo.collision.addObject('TriangleSetTopologyContainer', name='topology')
        root.logo.collision.addObject('TriangleSetTopologyModifier', name='Modifier')
        root.logo.collision.addObject('Tetra2TriangleTopologicalMapping', input='@../topology', output='@topology')
        root.logo.collision.addObject('MechanicalObject', name='state', rest_position="@../state.rest_position")
        root.logo.collision.addObject('TriangleCollisionModel')
        root.logo.collision.addObject('IdentityMapping')

        # Create the scene graph: visual node
        root.logo.addChild('visual')
        root.logo.visual.addObject('MeshOBJLoader', name='mesh', filename=file('surface.obj'), rotation=[90, 0, 0])
        root.logo.visual.addObject('OglModel', name='ogl', color='0.85 .3 0.1 0.9', src='@mesh')
        root.logo.visual.addObject('BarycentricMapping')

    def onSimulationInitDoneEvent(self, _):

        def disp():
            """
            Compute the surface displacement field.
            """

            diff = root.logo.visual.getObject('ogl').position.value - root.logo.visual.getObject('mesh').position.value
            return np.linalg.norm(diff, axis=1)

        # Record data automatically
        self.exporter.objects.add_sofa_mesh(positions_data=root.logo.visual.getObject('ogl').position,
                                            cells=root.logo.visual.getObject('ogl').triangles.value,
                                            color='grey',
                                            wireframe=True)
        self.exporter.objects.add_sofa_points(positions_data=root.logo.visual.getObject('ogl').position,
                                              colormap_name='gnuplot',
                                              colormap_range=[0, 3],
                                              colormap_function=disp)
        # Record data manually
        self.arrows_data = {'positions': [root.logo.forces.getObject('state').position.array().copy()],
                            'vectors': [root.logo.forces.getObject('state').force.array().copy()]}

    def onAnimateEndEvent(self, _):

        # Record data manually
        self.arrows_data['positions'].append(root.logo.forces.getObject('state').position.array().copy())
        self.arrows_data['vectors'].append(root.logo.forces.getObject('state').force.array().copy())


if __name__ == '__main__':

    import Sofa.Gui
    from os import listdir, remove

    # Create Exporter, create and init the SOFA simulation
    root = Sofa.Core.Node()
    exporter = Exporter(root=root, dt=0.2, animation=True, fps=50)
    simu = root.addObject(Simulation(root=root, exporter=exporter))
    Sofa.Simulation.init(root)

    # Launch the SOFA Gui, run a few time steps
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(root, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(root)
    Sofa.Gui.GUIManager.closeGUI()
    for file in [f for f in listdir() if f.endswith('.ini') or f.endswith('.log')]:
        remove(file)

    # Add manually the arrows to the exporter (the exporter did record 1 / 2 frames)
    steps = np.arange(0, len(simu.arrows_data['positions']), 2)
    exporter.objects.add_arrows(positions=simu.arrows_data['positions'][0],
                                vectors=simu.arrows_data['vectors'][0],
                                color=[50, 230, 75],
                                line_width=0.1,
                                head_size=0.,
                                time_positions=np.array(simu.arrows_data['positions'])[steps],
                                time_vectors=np.array(simu.arrows_data['vectors'])[steps])

    # Export to HTML file
    exporter.process(filename='sofa.html',
                     background_color='black',
                     grid_visible=False,
                     menu_visible=True,
                     frame_visible=True)
