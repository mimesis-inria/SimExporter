from os.path import join
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data and create tetra mesh
mesh = Mesh(join('data', 'heart.obj'))
tetra = mesh.clone().tetralize(side=0.05)


# Create the exporter
exporter = Exporter()


# Add meshes to the scene
exporter.objects.add_mesh(positions=mesh.vertices,
                          cells=mesh.cells,
                          color='#f5c211',
                          alpha=0.2,
                          wireframe=True)
exporter.objects.add_mesh(positions=tetra.vertices,
                          cells=tetra.cells,
                          color='#1c71d8',
                          alpha=0.05)


# Export to HTML with custom camera parameters
exporter.set_camera(factor=0.8, yaw=-80, pitch=60)
exporter.to_html(filename=join('html', 'tetra.html'), background_color='grey', grid_visible=False, menu_visible=True,
                 frame_visible=True)
