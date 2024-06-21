from typing import Optional, List, Union
from numpy import ndarray, float32
from k3d import Plot
from colour import Color

from SimExporter.core import objects as obj


def convert_color(color: Union[str, List]) -> int:
    """
    Convert a color input into its hex value.

    :param color: A string with the color name or a list with [R, G, B] values.
    """

    kwargs = {}

    # Case 1: RGB values
    if isinstance(color, list):
        if max(color) > 1:
            color = [c / 255 for c in color]
        kwargs['rgb'] = color

    # Case 2: color name
    elif isinstance(color, str):
        kwargs['color'] = color

    # Convert to hex value
    return int(Color(**kwargs).get_hex_l().replace('#', '0x'), 16)


class Factory:

    def __init__(self, plt: Plot, animation: bool):
        """
        API to create k3d objects.

        :param plt: k3d plotter used to render the objects.
        :param animation: If True, existing time series are associated to the 3D objects.
        """

        self.__animation = animation

        # The plotter to render the 3D objects
        self.__plt = plt

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
        """
        Create a new Mesh object.

        :param positions: Positions of the mesh.
        :param cells: Faces of the mesh.
        :param color: Color of the mesh, either the 'color name' or the [R, G, B] values.
        :param alpha: Opacity of the mesh.
        :param wireframe: If True, the mesh has a wireframe representation.
        :param flat_shading: If True, the faces are rendered flat, otherwise they are smoothed.
        :param colormap_name: Color map scheme name, see
                              https://matplotlib.org/stable/users/explain/colors/colormaps.html#classes-of-colormaps.
        :param colormap_range: Range of the color map.
        :param colormap_values: Scalar values to color the mesh regarding the color map.
        :param time_positions: Time series array for the positions.
        :param time_colormaps: Time series array for the color map scalar values.
        """

        # Create the mesh
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

        # Add to the plotter
        self.__plt += mesh

        # Associate time series if animation
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
                   colormap_name: str = 'jet',
                   colormap_range: Optional[List[int]] = None,
                   colormap_values: Optional[ndarray] = None,
                   time_positions: Optional[ndarray] = None,
                   time_colormaps: Optional[ndarray] = None) -> None:
        """
        Create a new Points object.

        :param positions: Positions of the points.
        :param color: Color of the points, either the 'color name' or the [R, G, B] values.
        :param alpha: Opacity of the points.
        :param point_size: Size of the points.
        :param colormap_name: Color map scheme name, see
                              https://matplotlib.org/stable/users/explain/colors/colormaps.html#classes-of-colormaps.
        :param colormap_range: Range of the color map.
        :param colormap_values: Scalar values to color the points regarding the color map.
        :param time_positions: Times series array for the positions.
        :param time_colormaps: Time series array for the color map scalar values.
        """

        # Create the points
        points = obj.points(positions=positions.astype(float32),
                            color=convert_color(color),
                            opacity=alpha,
                            point_size=point_size,
                            colormap_name=colormap_name,
                            colormap_range=colormap_range,
                            colormap_values=colormap_values,
                            time_colormaps=time_colormaps)

        # Add to the plotter
        self.__plt += points

        # Associate time series if animation
        if self.__animation:
            if time_positions is not None:
                points.positions = {str(i): t for i, t in enumerate(time_positions.astype(float32))}
            if time_colormaps is not None:
                points.attribute = {str(i): t for i, t in enumerate(time_colormaps.astype(float32))}

    def add_arrows(self,
                   positions: ndarray,
                   vectors: ndarray,
                   color: Union[str, List] = 'green',
                   scale: float = 1.,
                   head_size: float = 1.,
                   line_width: float = 0.02,
                   time_positions: Optional[ndarray] = None,
                   time_vectors: Optional[ndarray] = None) -> None:
        """
        Create a new Vectors object.

        :param positions: Positions of the vectors bases.
        :param vectors: Vectors values.
        :param color: Color of the vectors, either the 'color name' or the [R, G, B] values.
        :param scale: Scale to apply on the vectors.
        :param head_size: Size of the head of the vectors.
        :param line_width: Width of the vectors.
        :param time_positions: Time series array for the positions.
        :param time_vectors: Time series array for the vectors values.
        """

        # Create the vectors
        arrows = obj.vectors(origins=positions.astype(float32),
                             vecs=vectors.astype(float32) * scale,
                             color=convert_color(color),
                             head_size=max(head_size, 1e-6),
                             line_width=line_width)

        # Add to the plotter
        self.__plt += arrows

        # Associate time series if animation
        if self.__animation:
            if time_positions is not None:
                arrows.origins = {str(i): t for i, t in enumerate(time_positions.astype(float32))}
            if time_vectors is not None:
                arrows.vectors = {str(i): t for i, t in enumerate(time_vectors.astype(float32) * scale)}

    def add_k3d_objects(self, *objs) -> None:
        """
        Add standard k3d objects to the scene.

        :param objs: k3d objects.
        """

        # Add each k3d object to the plotter
        for o in objs:
            self.__plt += o
