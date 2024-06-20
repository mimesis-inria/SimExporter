import numpy as np
from k3d.objects import TimeSeries, Array, Vectors
from k3d.helpers import array_serialization_wrap
from k3d.transform import process_transform_arguments


def vectors(origins,
            vectors=None,
            colors=[],
            origin_color=None,
            head_color=None,
            color=0x0000FF,
            use_head=True,
            head_size=1.0,
            labels=[],
            label_size=1.0,
            line_width=0.01,
            name=None,
            group=None,
            custom_data=None,
            compression_level=0,
            **kwargs) -> Vectors:

    class _Vectors(Vectors):
        origins = TimeSeries(Array(dtype=np.float32)).tag(sync=True, **array_serialization_wrap('origins'))
        vectors = TimeSeries(Array(dtype=np.float32)).tag(sync=True, **array_serialization_wrap('vectors'))

    return process_transform_arguments(_Vectors(vectors=vectors if vectors is not None else origins,
                                                origins=origins if vectors is not None else np.zeros_like(vectors),
                                                colors=colors,
                                                origin_color=origin_color if origin_color is not None else color,
                                                head_color=head_color if head_color is not None else color,
                                                use_head=use_head,
                                                head_size=head_size,
                                                labels=labels,
                                                label_size=label_size,
                                                line_width=line_width,
                                                name=name,
                                                group=group,
                                                custom_data=custom_data,
                                                compression_level=compression_level),
                                       **kwargs)
