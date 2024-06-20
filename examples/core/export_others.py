import k3d
from vedo import Mesh

from SimExporter.core import Exporter

# Load the data
mesh = Mesh('heart.obj')
mesh = k3d.vtk_poly_data(mesh.dataset)

# Create the exporter
exporter = Exporter()

# Add k3d objects to the scene
lines = k3d.lines(vertices=mesh.vertices,
                  indices=mesh.indices,
                  shader='mesh',
                  width=0.25)
text = k3d.text(text='heart',
                position=mesh.vertices[500],
                is_html=True)
exporter.objects.add_k3d_objects(lines, text)

# Export to HTML
exporter.process(filename='others.html')
