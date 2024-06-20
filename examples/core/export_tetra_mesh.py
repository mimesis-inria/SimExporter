from vedo import Mesh

from SimExporter.core import Exporter


mesh = Mesh('heart.obj')
tetra = mesh.clone().tetralize(side=0.05)


# Create the exporter
exporter = Exporter()

# Add meshes to the scene
exporter.objects.add_mesh(positions=mesh.vertices,
                          cells=mesh.cells,
                          color='#f5c211',
                          alpha=0.9,
                          wireframe=True)
exporter.objects.add_mesh(positions=tetra.vertices,
                          cells=tetra.cells,
                          color='#1c71d8',
                          alpha=0.05)

# Export to HTML
exporter.process(filename='tetra.html',
                 background_color='white',
                 menu_visible=True,
                 grid_visible=False,
                 frame_visible=True)

