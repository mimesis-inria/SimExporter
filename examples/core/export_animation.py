from vedo import Mesh
import numpy as np

from SimExporter.core.exporter import Exporter


heart = Mesh('heart.obj').scale(0.001)
vessel = Mesh('vessels_fine.obj').scale(0.001)

exporter = Exporter()
exporter.objects.add_mesh(positions=heart.vertices,
                          cells=heart.cells,
                          color='#c01c28',
                          alpha=0.6,
                          flat_shading=False,
                          animation=np.load('heart.npy'))
exporter.objects.add_mesh(positions=vessel.vertices,
                          cells=vessel.cells,
                          color='white',
                          alpha=1.,
                          flat_shading=False,
                          animation=np.load('vessels_fine.npy'))
exporter.export_scene(filename='scene',
                      menu_visible=True,
                      grid_visible=False,
                      frame_visible=False)
