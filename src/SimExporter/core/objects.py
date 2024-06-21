from typing import Optional, List
import numpy as np
from numpy import ndarray, array, float32, zeros_like
import k3d
from k3d.objects import Vectors, TimeSeries, Array
from k3d.helpers import array_serialization_wrap
from vedo import Mesh, Points


def mesh(positions: ndarray,
         cells: ndarray,
         color: int,
         opacity: float,
         wireframe: bool,
         flat_shading: bool,
         colormap_name: str,
         colormap_range: Optional[List[int]],
         colormap_values: Optional[ndarray],
         time_colormaps: Optional[ndarray]) -> k3d.objects.Mesh:
    """
    Create a new Mesh object.

    :param positions: Positions of the mesh.
    :param cells: Faces of the mesh.
    :param color: Color of the mesh.
    :param opacity: Opacity of the mesh.
    :param wireframe: Wireframe mesh or not.
    :param flat_shading: Flat or smoothed mesh faces.
    :param colormap_name: Color map scheme name.
    :param colormap_range: Color map range.
    :param colormap_values: Color map scalar values.
    :param time_colormaps: Time series array for the color map scalar values.
    """

    # Create a temporary Vedo mesh to get vtkPolyData as k3d.Mesh objects only accept triangle cells
    poly_mesh = Mesh(inputobj=[positions, cells])

    # Get the first value of the time series if the color map array is empty
    if time_colormaps is not None and colormap_values is None:
        colormap_values = time_colormaps[0]

    # Define color map variables
    color_map, color_attribute = None, None
    if colormap_values is not None:
        # Add the color map to the vedo mesh
        poly_mesh.cmap(input_cmap=colormap_name, input_array=colormap_values, name='scalars')
        # Get the created lookup table
        lut = poly_mesh.mapper.GetLookupTable()
        n_color = lut.GetTable().GetNumberOfTuples()
        # Build the color map array with values [i/n, R, G, B]
        color_map = []
        for i in range(n_color):
            color_map.append([i / (n_color - 1)] + list(lut.GetTableValue(i))[:3])
        color_map = array(color_map, dtype=float32)
        # Define the color map attribute as ['array_name', v_min, v_max]
        color_attribute = ['scalars']
        # Add the color map range to the attributes
        if colormap_range is not None:
            color_attribute += colormap_range
        else:
            if time_colormaps is not None:
                color_attribute += [time_colormaps.min(), time_colormaps.max()]
            else:
                color_attribute += [colormap_values.min(), colormap_values.max()]

    # Actually create the k3d mesh
    return k3d.vtk_poly_data(poly_data=poly_mesh.dataset,
                             color=color,
                             opacity=opacity,
                             wireframe=wireframe,
                             flat_shading=flat_shading,
                             color_map=color_map,
                             color_attribute=color_attribute)


def points(positions: ndarray,
           color: int,
           opacity: float,
           point_size: float,
           colormap_name: str,
           colormap_range: Optional[List[int]],
           colormap_values: Optional[ndarray],
           time_colormaps: Optional[ndarray]) -> k3d.objects.Points:
    """
    Create a new Points object.

    :param positions: Positions of the points.
    :param color: Color of the points.
    :param opacity: Opacity of the points.
    :param point_size: Size of the points.
    :param colormap_name: Color map scheme name.
    :param colormap_range: Color map range.
    :param colormap_values: Color map scalar values.
    :param time_colormaps: Time series array for the color map scalar values.
    """

    # Get the first value of the time series if the color map array is empty
    if time_colormaps is not None and colormap_values is None:
        colormap_values = time_colormaps[0]

    # Define color map variables
    color_map, color_attribute, color_range = None, [], []
    if colormap_values is not None:
        # Create a temporary Vedo points to create the color map
        pcd = Points(inputobj=positions).cmap(input_cmap=colormap_name, input_array=colormap_values)
        # Get the created lookup table
        lut = pcd.mapper.GetLookupTable()
        n_color = lut.GetTable().GetNumberOfTuples()
        # Build the color map array with values [i/n, R, G, B]
        color_map = []
        for i in range(n_color):
            color_map.append([i / (n_color - 1)] + list(lut.GetTableValue(i))[:3])
        color_map = array(color_map, dtype=float32)
        # Define the color map attribute
        color_attribute = colormap_values
        # Define the color map range
        if colormap_range is not None:
            color_range = colormap_range
        else:
            if time_colormaps is not None:
                color_range += [time_colormaps.min(), time_colormaps.max()]
            else:
                color_range += [colormap_values.min(), colormap_values.max()]

    # Actually create the k3d points
    return k3d.points(positions=positions,
                      color=color,
                      opacity=opacity,
                      point_size=point_size,
                      shader='3D',
                      color_map=color_map,
                      attribute=color_attribute,
                      color_range=color_range)


def vectors(origins,
            vecs,
            color,
            head_size,
            line_width) -> Vectors:
    """
    Create a new Vectors object.

    :param origins: Positions of the vectors bases.
    :param vecs: Vectors values.
    :param color: Color of the vectors.
    :param head_size: Size of the head of the vectors.
    :param line_width: Width of the vectors.
    """

    class _Vectors(Vectors):
        origins = TimeSeries(Array(dtype=np.float32)).tag(sync=True, **array_serialization_wrap('origins'))
        vectors = TimeSeries(Array(dtype=np.float32)).tag(sync=True, **array_serialization_wrap('vectors'))

    return _Vectors(vectors=vecs if vecs is not None else origins,
                    origins=origins if vecs is not None else np.zeros_like(vecs),
                    colors=[],
                    origin_color=color,
                    head_color=color,
                    use_head=True,
                    head_size=head_size,
                    labels=[],
                    label_size=1.0,
                    line_width=line_width,
                    name=None,
                    group=None,
                    custom_data=None,
                    compression_level=0)
