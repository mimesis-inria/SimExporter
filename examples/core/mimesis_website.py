"""
This script was used to generate the 3D interactive animation on the MIMESIS landing page: https://mimesis.inria.fr/.
"""

from os.path import join
from numpy import load
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh(join('data', 'heart.obj'))
heart_positions = load(join('data', 'heart.npy'))
vessel = Mesh(join('data', 'vessels.obj'))
vessel_positions = load(join('data', 'vessels.npy'))


# Create the exporter
exporter = Exporter(animation=True, fps=60)


# Add meshes to the scene
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          time_positions=heart_positions,
                          alpha=0.9, wireframe=True, color='#bb96d9')
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          time_positions=heart_positions,
                          alpha=0.5, flat_shading=False, wireframe=False, color='#bb96d9')
exporter.objects.add_mesh(positions=vessel.vertices,
                          cells=vessel.cells,
                          time_positions=vessel_positions,
                          color='#8300e9', alpha=0.6, flat_shading=False)


# Export to HTML with custom camera parameters
exporter.set_camera(factor=0.8, yaw=-75, pitch=65)
exporter.to_html(filename=join('html', 'website.html'), background_color="#030929", grid_visible=False,
                 menu_visible=False, frame_visible=False)
