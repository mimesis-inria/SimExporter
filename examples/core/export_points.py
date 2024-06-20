from numpy import load, mean
from numpy.linalg import norm
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh('heart.obj')
heart_positions = load('heart.npy')

# Create the exporter
exporter = Exporter(animation=True,
                    fps=50)

# Add mesh and points to the scene
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          color='grey',
                          alpha=0.6,
                          wireframe=True,
                          time_positions=heart_positions)
exporter.objects.add_points(positions=heart.vertices,
                            point_size=2,
                            colormap_name='YlOrBr',
                            time_colormaps=norm(heart_positions - mean(heart_positions, axis=0), axis=2),
                            time_positions=heart_positions)

# Export to HTML
exporter.process(filename='points.html',
                 background_color='white',
                 menu_visible=True,
                 grid_visible=False,
                 frame_visible=True)
