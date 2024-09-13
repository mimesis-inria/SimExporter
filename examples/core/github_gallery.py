from os.path import join
from numpy import load, mean, tile
from numpy.linalg import norm
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh(join('data', 'heart.obj'))
heart_positions = load(join('data', 'heart.npy'))
vessel = Mesh(join('data', 'vessels.obj'))
vessel_positions = load(join('data', 'vessels.npy'))


# Get translations
t_heart = heart.clone().x(90)
Th = tile(t_heart.vertices - heart.vertices, heart_positions.shape[0]).reshape(106, -1, 3)


# Create the exporter
exporter = Exporter(animation=True, fps=50)


# Add meshes to the scene
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          color=[192, 28, 40],
                          alpha=0.4,
                          flat_shading=False,
                          time_positions=heart_positions)
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          color=[192, 28, 40],
                          alpha=0.6,
                          wireframe=True,
                          flat_shading=False,
                          time_positions=heart_positions)
exporter.objects.add_mesh(positions=vessel.vertices,
                          cells=vessel.cells,
                          color='white',
                          alpha=1.,
                          flat_shading=False,
                          colormap_name='Reds',
                          colormap_range=[0, 1],
                          time_colormap_values=norm(vessel_positions - mean(vessel_positions, axis=0), axis=2),
                          time_positions=vessel_positions)


# Add mesh and points to the scene
exporter.objects.add_mesh(positions=t_heart.vertices,
                          cells=t_heart.cells,
                          color='grey',
                          alpha=0.6,
                          wireframe=True,
                          time_positions=heart_positions + Th)
exporter.objects.add_mesh(positions=t_heart.vertices,
                          cells=t_heart.cells,
                          color='grey',
                          alpha=0.4,
                          time_positions=heart_positions + Th)
exporter.objects.add_points(positions=heart.vertices,
                            point_size=2,
                            colormap_name='YlOrBr',
                            time_colormap_values=norm(heart_positions - mean(heart_positions, axis=0), axis=2),
                            time_positions=heart_positions + Th)


# Export to HTML with custom camera parameters
exporter.set_camera(factor=0.55, yaw=-90, pitch=60)
exporter.to_html(filename=join('html', 'gallery.html'), background_color='#0D1117', grid_visible=False,
                 menu_visible=False, frame_visible=False)
