from numpy import load, zeros, mean
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh('heart.obj')
heart_positions = load('heart.npy')

# Create the exporter
exporter = Exporter(animation=True,
                    fps=50)

# Add mesh and arrows to the scene
exporter.objects.add_mesh(positions=mean(heart_positions, axis=0),
                          cells=heart.cells,
                          color='grey',
                          alpha=0.6,
                          wireframe=True)
exporter.objects.add_arrows(positions=mean(heart_positions, axis=0),
                            vectors=zeros((heart.npoints, 3)),
                            scale=3,
                            line_width=0.5,
                            head_size=0.,
                            time_vectors=heart_positions[:] - mean(heart_positions, axis=0))

exporter.process(filename='arrows.html',
                 background_color='white',
                 menu_visible=True,
                 grid_visible=False,
                 frame_visible=False)
