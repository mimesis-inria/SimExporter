import numpy as np
import k3d
from k3d.objects import TimeSeries, Array, Vectors, Mesh
from k3d.helpers import array_serialization_wrap
from vedo import Mesh as VedoMesh


def mesh(positions, cells, color, opacity, wireframe, flat_shading, colormap_name, colormap_range, colormap_values,
         time_colormaps) -> Mesh:

    # Create a temporary Vedo mesh to get vtkPolyData as k3d.Mesh objects only accept triangle cells
    poly_mesh = VedoMesh(inputobj=[positions, cells])

    color_map, color_attribute = None, None
    if time_colormaps is not None and colormap_values is None:
        colormap_values = time_colormaps[0]
    if colormap_values is not None:
        poly_mesh.cmap(input_cmap=colormap_name, input_array=colormap_values)
        lut = poly_mesh.mapper.GetLookupTable()
        n_color = lut.GetTable().GetNumberOfTuples()
        color_map = []
        for i in range(n_color):
            color_map.append([i / (n_color - 1)] + list(lut.GetTableValue(i))[:3])
        color_map = np.array(color_map, dtype=np.float32)

        color_attribute = ['Scalars']
        if colormap_range is not None:
            color_attribute += colormap_range
        else:
            if time_colormaps is not None:
                color_attribute.append(np.min(time_colormaps))
                color_attribute.append(np.max(time_colormaps))
            else:
                color_attribute.append(np.min(colormap_values))
                color_attribute.append(np.max(colormap_values))

    return k3d.vtk_poly_data(poly_data=poly_mesh.dataset,
                             color=color,
                             opacity=opacity,
                             wireframe=wireframe,
                             flat_shading=flat_shading,
                             color_map=color_map,
                             color_attribute=color_attribute)


def vectors(origins, vectors, color, head_size, line_width) -> Vectors:

    class _Vectors(Vectors):
        origins = TimeSeries(Array(dtype=np.float32)).tag(sync=True, **array_serialization_wrap('origins'))
        vectors = TimeSeries(Array(dtype=np.float32)).tag(sync=True, **array_serialization_wrap('vectors'))

    return _Vectors(vectors=vectors if vectors is not None else origins,
                    origins=origins if vectors is not None else np.zeros_like(vectors),
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
