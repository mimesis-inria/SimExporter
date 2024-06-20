from typing import Optional, List, Union
from numpy import ndarray, float32
import k3d
from colour import Color

from SimExporter.core import objects as obj


def convert_color(color) -> int:
    kwargs = {}
    if isinstance(color, list):
        if max(color) > 1:
            color = [c / 255 for c in color]
        kwargs['rgb'] = color
    elif isinstance(color, str):
        kwargs['color'] = color
    return int(Color(**kwargs).get_hex_l().replace('#', '0x'), 16)


class Factory:

    def __init__(self, plt: k3d.Plot, animation: bool):

        self.__plt = plt
        self.__animation = animation

    def add_mesh(self,
                 positions: ndarray,
                 cells: ndarray,
                 color: Union[str, List] = 'chartreuse',
                 alpha: float = 1.,
                 wireframe: bool = False,
                 flat_shading: bool = True,
                 colormap_name: str = 'jet',
                 colormap_range: Optional[List[int]] = None,
                 colormap_values: Optional[ndarray] = None,
                 time_positions: Optional[ndarray] = None,
                 time_colormaps: Optional[ndarray] = None) -> None:

        mesh = obj.mesh(positions=positions,
                        cells=cells,
                        color=convert_color(color),
                        opacity=alpha,
                        wireframe=wireframe,
                        flat_shading=flat_shading,
                        colormap_name=colormap_name,
                        colormap_range=colormap_range,
                        colormap_values=colormap_values,
                        time_colormaps=time_colormaps)
        self.__plt += mesh

        if self.__animation:
            if time_positions is not None:
                mesh.vertices = {str(i): t for i, t in enumerate(time_positions.astype(float32))}
            if time_colormaps is not None:
                mesh.attribute = {str(i): t for i, t in enumerate(time_colormaps.astype(float32))}

    def add_points(self,
                   positions: ndarray,
                   color: Union[str, List] = 'salmon',
                   alpha: float = 1.,
                   point_size: int = 0.1,
                   time_positions: Optional[ndarray] = None) -> None:

        points = k3d.points(positions=positions.astype(float32),
                            color=convert_color(color),
                            opacity=alpha,
                            point_size=point_size,
                            shader='3d')
        self.__plt += points

        if self.__animation:
            if time_positions is not None:
                points.positions = {str(i): t for i, t in enumerate(time_positions.astype(float32))}

    def add_arrows(self,
                   positions: ndarray,
                   vectors: ndarray,
                   color: Union[str, List] = 'green',
                   scale: float = 1.,
                   head_size: float = 1.,
                   line_width: float = 0.02,
                   time_positions: Optional[ndarray] = None,
                   time_vectors: Optional[ndarray] = None) -> None:

        arrows = obj.vectors(origins=positions.astype(float32),
                             vectors=vectors.astype(float32) * scale,
                             color=convert_color(color),
                             head_size=max(head_size, 1e-6),
                             line_width=line_width)
        self.__plt += arrows

        if self.__animation:
            if time_positions is not None:
                arrows.origins = {str(i): t for i, t in enumerate(time_positions.astype(float32))}
            if time_vectors is not None:
                arrows.vectors = {str(i): t for i, t in enumerate(time_vectors.astype(float32) * scale)}

    def add_k3d_objects(self, *objs):

        for o in objs:
            self.__plt += o
