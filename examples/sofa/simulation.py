from os.path import join, dirname
from numpy import load

import Sofa
import Sofa.Gui


class Simulation(Sofa.Core.Controller):

    def __init__(self, root: Sofa.Core.Node, *args, **kwargs):
        """
        Simulation of a deformable SOFA logo.
        """

        Sofa.Core.Controller.__init__(self, name='PyController', *args, **kwargs)
        get_file = lambda f: join(dirname(__file__), 'data', f)

        # Create the root node
        root.dt.value = 0.1
        with open(get_file('plugins.txt'), 'r') as f:
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

        # Create the logo object node
        root.addChild('logo')
        root.logo.addObject('EulerImplicitSolver', firstOrder=False, rayleighMass=0.1, rayleighStiffness=0.1)
        root.logo.addObject('CGLinearSolver', iterations=25, tolerance=1e-9, threshold=1e-9)
        root.logo.addObject('MeshVTKLoader', name='mesh', filename=get_file('volume.vtk'), rotation=[90, 0, 0])
        root.logo.addObject('TetrahedronSetTopologyContainer', name='topology', src='@mesh')
        root.logo.addObject('TetrahedronSetGeometryAlgorithms', template='Vec3d')
        root.logo.addObject('MechanicalObject', name='state', src='@topology')
        root.logo.addObject('TetrahedronFEMForceField', youngModulus=15000, poissonRatio=0.4, method='svd')
        root.logo.addObject('MeshMatrixMass', totalMass=0.01)
        root.logo.addObject('FixedConstraint', name='constraints', indices=load(get_file('constraints.npy')))

        # Create the visual node
        root.logo.addChild('visual')
        root.logo.visual.addObject('MeshOBJLoader', name='mesh', filename=get_file('surface.obj'), rotation=[90, 0, 0])
        root.logo.visual.addObject('OglModel', name='ogl', color='0.85 .3 0.1 0.9', src='@mesh')
        root.logo.visual.addObject('BarycentricMapping')


if __name__ == '__main__':

    # Create the SOFA simulation
    node = Sofa.Core.Node()
    node.addObject(Simulation(root=node))

    # Init the SOFA simulation
    Sofa.Simulation.init(node)

    # Launch the SOFA Gui, run a few time steps
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(node, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(node)
    Sofa.Gui.GUIManager.closeGUI()
