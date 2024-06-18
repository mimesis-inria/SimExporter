from typing import Optional, List
from numpy import ndarray, float32, float64
import k3d
from vedo import Mesh
from colour import Color


class Objects:

    def __init__(self, plt: k3d.Plot, time_series: List):

        self.__plt = plt
        self.__time_series = time_series

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
        self.__plt += mesh

        if animation is not None:
            if animation.dtype == float64:
                animation = animation.astype(float32)
            self.__time_series.append([mesh, 'mesh', animation])

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
        self.__plt += points

        if animation is not None:
            if animation.dtype == float64:
                animation = animation.astype(float32)
            self.__time_series.append([points, 'points', animation])
