from os.path import join
from numpy import load, zeros, mean, array
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh(join('data', 'heart.obj'))
heart_positions = load(join('data', 'heart.npy'))


# Create the exporter
exporter = Exporter(animation=True, fps=50)


# Add mesh and arrows to the scene
exporter.objects.add_mesh(positions=mean(heart_positions, axis=0),
                          time_positions=array([mean(heart_positions, axis=0) for _ in range(heart_positions.shape[0])]),
                          cells=heart.cells,
                          color='grey',
                          alpha=0.6,
                          wireframe=True)
exporter.objects.add_arrows(positions=mean(heart_positions, axis=0),
                            vectors=zeros((heart.npoints, 3)),
                            time_positions=array([mean(heart_positions, axis=0) for _ in range(heart_positions.shape[0])]),
                            scale=3,
                            line_width=0.5,
                            head_size=0.,
                            time_vectors=heart_positions[:] - mean(heart_positions, axis=0))


# Export to HTML with custom camera parameters
exporter.set_camera(factor=0.8, yaw=-80, pitch=60)
exporter.to_html(filename=join('html', 'arrows.html'), background_color='#0D1117', grid_visible=False,
                 menu_visible=True, frame_visible=False)
