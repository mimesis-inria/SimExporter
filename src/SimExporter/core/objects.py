from typing import Optional
from numpy import ndarray, float32, float64
import k3d
from vedo import Mesh, Plotter
from colour import Color


class Objects:

    def __init__(self, plt: k3d.Plot):

        self._objects = []
        self._plt = plt

    def add_mesh(self,
                 positions: ndarray,
                 cells: ndarray,
                 color: str = 'chartreuse',
                 alpha: float = 1.,
                 wireframe: bool = False,
                 flat_shading: bool = True,
                 animation: Optional[ndarray] = None) -> None:

        # Create a temporary Vedo mesh to get vtkPolyData as k3d.Mesh objects only accept triangle cells
        poly_mesh = Mesh([positions, cells])

        mesh = k3d.vtk_poly_data(poly_data=poly_mesh.dataset,
                                 color=int(Color(color).get_hex_l().replace('#', '0x'), 16),
                                 opacity=alpha,
                                 wireframe=wireframe,
                                 flat_shading=flat_shading)
        if animation is not None:
            if animation.dtype == float64:
                animation = animation.astype(float32)
            mesh.vertices = {str(i): pos for i, pos in enumerate(animation)}

        self._plt += mesh

    def add_points(self,
                   positions: ndarray,
                   color: str = 'salmon',
                   alpha: float = 1.,
                   point_size: int = 0.1,
                   animation: Optional[ndarray] = None) -> None:

        points = k3d.points(positions=positions.astype(float32),
                            color=int(Color(color).get_hex_l().replace('#', '0x'), 16),
                            opacity=alpha,
                            point_size=point_size,
                            shader='3d')
        if animation is not None:
            if animation.dtype == float64:
                animation = animation.astype(float32)
            points.positions = {str(i): pos for i, pos in enumerate(animation)}

        self._plt += points
