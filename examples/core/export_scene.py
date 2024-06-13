import numpy as np

from SimExporter.core.exporter import Exporter


exporter = Exporter()
exporter.objects.add_points(positions=np.random.randn(10, 3),
                            animation=np.random.randn(100, 10, 3))
exporter.export_scene(filename='scene')

