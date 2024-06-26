from typing import Optional, Union, List, Callable
from numpy import ndarray
from k3d import Plot
import Sofa

from SimExporter.core.factory import Factory as _Factory
from SimExporter.sofa.recorder import Recorder


class Factory(_Factory):

    def __init__(self, recorder: Recorder, plt: Plot, animation: bool):
        """
        API to create k3d objects and record data during a SOFA simulation.

        :param recorder: SOFA Data recorder.
        :param plt: k3d plotter used to render the objects.
        :param animation: If True, existing time series are associated to the 3D objects.
        """

        super().__init__(plt=plt, animation=animation)
        self.__recorder = recorder

    def add_sofa_mesh(self,
                      positions_data: Sofa.Core.Data,
                      cells: ndarray,
                      color: Union[str, List] = 'chartreuse',
                      alpha: float = 1.,
                      wireframe: bool = False,
                      flat_shading: bool = True,
                      colormap_name: str = 'jet',
                      colormap_range: Optional[List[int]] = None,
                      colormap_function: Optional[Callable] = None) -> None:
        """
        Create a new Mesh object and record it automatically during the SOFA simulation.

        :param positions_data: SOFA Data field containing the positions of the mesh.
        :param cells: Faces of the mesh.
        :param color: Color of the mesh, either the 'color name' or the [R, G, B] values.
        :param alpha: Opacity of the mesh.
        :param wireframe: If True, the mesh has a wireframe representation.
        :param flat_shading: If True, the faces are rendered flat, otherwise they are smoothed.
        :param colormap_name: Color map scheme name, see
                              https://matplotlib.org/stable/users/explain/colors/colormaps.html#classes-of-colormaps.
        :param colormap_range: Range of the color map.
        :param colormap_function: Function to compute at each time step the scalar values to color the mesh regarding
                                  the color map.
        """

        # Core mesh data
        args = {key: value for key, value in locals().items()
                if key not in ['self', 'positions_data', 'colormap_function']}

        # SOFA callbacks
        callbacks = [('positions', positions_data, [positions_data.array().copy()])]
        if colormap_function is not None:
            callbacks.append(('colormap_values', colormap_function, [colormap_function()]))

        # Record the object
        self.__recorder.add_object(object_type='mesh',
                                   object_data=args,
                                   callbacks=callbacks)

    def add_sofa_points(self,
                        positions_data: Sofa.Core.Data,
                        color: Union[str, List] = 'salmon',
                        alpha: float = 1.,
                        point_size: int = 0.1,
                        colormap_name: str = 'jet',
                        colormap_range: Optional[List[int]] = None,
                        colormap_function: Optional[Callable] = None) -> None:
        """
        Create a new Points object and record it automatically during the SOFA simulation.

        :param positions_data: SOFA Data field containing the positions of the points.
        :param color: Color of the points, either the 'color name' or the [R, G, B] values.
        :param alpha: Opacity of the points.
        :param point_size: Size of the points.
        :param colormap_name: Color map scheme name, see
                              https://matplotlib.org/stable/users/explain/colors/colormaps.html#classes-of-colormaps.
        :param colormap_range: Range of the color map.
        :param colormap_function: Function to compute at each time step the scalar values to color the points regarding
                                  the color map.
        """

        # Core points data
        args = {key: value for key, value in locals().items()
                if key not in ['self', 'positions_data', 'colormap_function']}

        # Sofa callbacks
        callbacks = [('positions', positions_data, [positions_data.array().copy()])]
        if colormap_function is not None:
            callbacks.append(('colormap_values', colormap_function, [colormap_function()]))

        # Record the object
        self.__recorder.add_object(object_type='points',
                                   object_data=args,
                                   callbacks=callbacks)

    def add_sofa_arrows(self,
                        positions_data: Sofa.Core.Data,
                        vectors_data: Sofa.Core.Data,
                        color: Union[str, List] = 'green',
                        scale: float = 1.,
                        head_size: float = 1.,
                        line_width: float = 0.02):
        """
        Create a new Vectors object and record it automatically during the SOFA simulation.

        :param positions_data: SOFA Data field containing the positions of the arrows.
        :param vectors_data: SOFA Data field containing the vector values of the arrows.
        :param color: Color of the vectors, either the 'color name' or the [R, G, B] values.
        :param scale: Scale to apply on the vectors.
        :param head_size: Size of the head of the vectors.
        :param line_width: Width of the vectors.
        """

        # Core arrows data
        args = {key: value for key, value in locals().items()
                if key not in ['self', 'positions_data', 'vectors_data']}

        # SOFA callbacks
        callbacks = [('positions', positions_data, [positions_data.array().copy()]),
                     ('vectors', vectors_data, [vectors_data.array().copy()])]

        # Record the object
        self.__recorder.add_object(object_type='arrows',
                                   object_data=args,
                                   callbacks=callbacks)
