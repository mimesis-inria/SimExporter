from os.path import join
from numpy import load, mean
from numpy.linalg import norm
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh(join('data', 'heart.obj'))
heart_positions = load(join('data', 'heart.npy'))


# Create the exporter
exporter = Exporter(animation=True, fps=50)


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
                            time_colormap_values=norm(heart_positions - mean(heart_positions, axis=0), axis=2),
                            time_positions=heart_positions)


# Export to HTML with custom camera parameters
exporter.set_camera(factor=0.8, yaw=-80, pitch=60)
exporter.to_html(filename=join('html', 'points.html'), background_color='#0D1117', grid_visible=False,
                 menu_visible=True, frame_visible=True)
