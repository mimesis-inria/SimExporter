from os.path import join
from numpy import array, float32
import k3d
from vedo import Mesh

from SimExporter.core import Exporter


# Load the data
mesh = Mesh(join('data', 'heart.obj'))
mesh = k3d.vtk_poly_data(mesh.dataset)


# Create the exporter
exporter = Exporter()


# Create k3d objects
lines = k3d.lines(vertices=array(mesh.vertices, dtype=float32),
                  indices=array(mesh.indices, dtype=float32),
                  shader='mesh',
                  width=0.25)
text = k3d.text(text='heart',
                position=mesh.vertices[500],
                is_html=True)


# Add k3d objects to the scene
exporter.objects.add_k3d_objects(lines, text)


# Export to HTML
exporter.to_html(filename=join('html', 'others.html'))
