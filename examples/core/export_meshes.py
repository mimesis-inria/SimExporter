from os.path import join
from numpy import load, mean
from numpy.linalg import norm
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
heart = Mesh(join('data', 'heart.obj'))
heart_positions = load(join('data', 'heart.npy'))
vessel = Mesh(join('data', 'vessels.obj'))
vessel_positions = load(join('data', 'vessels.npy'))


# Create the exporter
exporter = Exporter(animation=True, fps=50)


# Add meshes to the scene
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          color=[192, 28, 40],
                          alpha=0.6,
                          flat_shading=False,
                          wireframe=True,
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


# Export to HTML with custom camera parameters
exporter.set_camera(factor=0.8, yaw=-80, pitch=60)
exporter.to_html(filename=join('html', 'meshes.html'), background_color='#0D1117', grid_visible=False,
                 menu_visible=True, frame_visible=True)
