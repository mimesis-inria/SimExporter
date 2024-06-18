from os.path import join, dirname
import k3d
from base64 import b64encode
from zlib import compress
from msgpack import packb

from SimExporter.core.objects import Objects


class Exporter:

    def __init__(self):

        self.__plt = k3d.Plot(camera_mode='orbit', lighting=1.)
        self.__time_series = []
        self.objects = Objects(plt=self.__plt, time_series=self.__time_series)

    def export_scene(self,
                     filename: str,
                     grid_visible: bool = False,
                     menu_visible: bool = False,
                     frame_visible: bool = True) -> None:

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

    def export_animation(self,
                         filename: str,
                         grid_visible: bool = False,
                         menu_visible: bool = False,
                         frame_visible: bool = True) -> None:

        # Set the time series
        for (obj, obj_type, time_series) in self.__time_series:
            if obj_type == 'mesh':
                obj.vertices = {str(i): t for i, t in enumerate(time_series)}
            elif obj_type == 'points':
                obj.positions = {str(i): t for i, t in enumerate(time_series)}

        self.export_scene(filename=filename,
                          grid_visible=grid_visible,
                          menu_visible=menu_visible,
                          frame_visible=frame_visible)
