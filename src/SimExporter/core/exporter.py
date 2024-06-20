from typing import List, Union
from os.path import join, dirname
import k3d
from base64 import b64encode
from zlib import compress
from msgpack import packb

from SimExporter.core.factory import Factory, convert_color


class Exporter:

    def __init__(self, animation: bool = False, fps: float = 25.):

        self.__plt = k3d.Plot(camera_mode='orbit', lighting=1., fps=fps)
        self.__animation = animation

        self.objects = Factory(plt=self.__plt, animation=self.__animation)

    def process(self,
                filename: str,
                background_color: Union[str, List] = 'white',
                grid_visible: bool = True,
                menu_visible: bool = True,
                frame_visible: bool = True) -> None:

        self.__plt.background_color = convert_color(background_color)

        static_dir = join(dirname(dirname(__file__)), 'static')
        with open(join(static_dir, 'snapshot_standalone.txt'), 'r') as file:
            content = file.read()
        with open(join(static_dir, 'standalone.js'), 'r') as file:
            content = content.replace('[K3D_SOURCE]', b64encode(compress(file.read().encode())).decode('utf-8'))
        with open(join(static_dir, 'require.js'), 'r') as file:
            content = content.replace('[REQUIRE_JS]', file.read())
        with open(join(static_dir, 'fflate.js'), 'r') as file:
            content = content.replace('[FFLATE_JS]', file.read())
        content = content.replace('[ADDITIONAL]', '')

        snapshot = self.__plt.get_binary_snapshot_objects()
        plot_params = self.__plt.get_plot_params()
        plot_params['menuVisibility'] = menu_visible
        plot_params['gridVisible'] = grid_visible
        plot_params['axesHelper'] = 1. if frame_visible else 0.
        snapshot['plot'] = plot_params

        data = compress(packb(snapshot, use_bin_type=True), 9)
        content = content.replace('[DATA]', b64encode(data).decode('utf-8'))

        filename = f'{filename}.html' if not filename.endswith('.html') else filename
        with open(filename, 'w') as file:
            file.write(content)
