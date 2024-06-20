from numpy import load
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh('heart.obj')
heart_positions = load('heart.npy')
vessel = Mesh('vessels.obj')
vessel_positions = load('vessels.npy')

# Create the exporter
exporter = Exporter(animation=True,
                    fps=50)

# Add meshes to the scene
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          color=[192, 28, 40],
                          alpha=0.6,
                          flat_shading=False,
                          time_positions=heart_positions)
exporter.objects.add_mesh(positions=vessel.vertices,
                          cells=vessel.cells,
                          color='white',
                          alpha=1.,
                          flat_shading=False,
                          wireframe=True,
                          time_positions=vessel_positions)

# Export to HTML
exporter.process(filename='meshes.html',
                 background_color='white',
                 menu_visible=True,
                 grid_visible=False,
                 frame_visible=True)
