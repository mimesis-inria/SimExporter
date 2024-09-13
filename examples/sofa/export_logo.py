from os.path import join
import numpy as np

import Sofa.Gui

from SimExporter.sofa import Exporter
from simulation import Simulation


def displacement_field():
    return np.linalg.norm(node.logo.getObject('state').position.value - node.logo.getObject('mesh').position.value,
                          axis=1)


if __name__ == '__main__':

    # Create the SOFA simulation
    node = Sofa.Core.Node()
    node.addObject(Simulation(root=node))

    # Create the Exporter and add objects
    exporter = Exporter(root=node,
                        dt=0.2,
                        animation=True,
                        fps=70)
    exporter.objects.add_sofa_mesh(positions_data=node.logo.visual.getObject('ogl').position,
                                   cells=node.logo.visual.getObject('ogl').triangles.value,
                                   flat_shading=False,
                                   color='#ff7800',
                                   alpha=0.5)
    exporter.objects.add_sofa_mesh(positions_data=node.logo.visual.getObject('ogl').position,
                                   cells=node.logo.visual.getObject('ogl').triangles.value,
                                   wireframe=True,
                                   color='#ff7800',
                                   alpha=0.95)
    exporter.objects.add_sofa_points(positions_data=node.logo.getObject('state').position,
                                     colormap_name='plasma',
                                     colormap_function=displacement_field)

    # Init the SOFA simulation AFTER creating the exporter (otherwise, callbacks will not work)
    Sofa.Simulation.init(node)

    # Launch the SOFA Gui, run a few time steps
    Sofa.Gui.GUIManager.Init(program_name="main", gui_name="qglviewer")
    Sofa.Gui.GUIManager.createGUI(node, __file__)
    Sofa.Gui.GUIManager.SetDimension(1200, 900)
    Sofa.Gui.GUIManager.MainLoop(node)
    Sofa.Gui.GUIManager.closeGUI()

    # Export to HTML file
    exporter.set_camera(factor=0.8, yaw=0, pitch=0)
    exporter.to_html(filename=join('html', 'sofa.html'), background_color='black', grid_visible=False,
                     menu_visible=True, frame_visible=True)
