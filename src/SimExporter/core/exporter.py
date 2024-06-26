from typing import List, Union
from os.path import join, dirname
from k3d import Plot
from base64 import b64encode
from zlib import compress
from msgpack import packb

from SimExporter.core.factory import Factory, convert_color


class Exporter:

    def __init__(self, animation: bool = False, fps: float = 25.):
        """
        Main API to create a scene with 3D objects and export a standalone 3D plot or animation in an HTML file.

        :param animation: If False, a static 3D plot is exported. If True, a 3D animation is exported if time series
                          are associated to a 3D object.
        :param fps: Frame rate of the animation (not used if animation = False).
        """

        # Create a plotter to render the 3D objects
        self._plt = Plot(fps=fps, camera_rotate_speed=5.)

        # Create a factory to easily add 3D objects in the scene
        self.objects = Factory(plt=self._plt, animation=animation)

    def process(self,
                filename: str,
                background_color: Union[str, List] = 'white',
                grid_visible: bool = True,
                menu_visible: bool = True,
                frame_visible: bool = True) -> None:
        """
        Export the current scene in a standalone HTML file.

        :param filename: Name of the HTML file.
        :param background_color: Color of the background in the 3D view.
        :param grid_visible: If True, the reference grid is displayed.
        :param menu_visible: If True, the menu panel is displayed.
        :param frame_visible: If True, the reference frame is displayed.
        """

        # Set the background color
        self._plt.background_color = convert_color(background_color)

        # Get the directory that contains the javascript files and fill the standalone snapshot
        static_dir = join(dirname(dirname(__file__)), 'static')
        with open(join(static_dir, 'snapshot_standalone.txt'), 'r', encoding='utf-8') as file:
            content = file.read()
        with open(join(static_dir, 'standalone.js'), 'r', encoding='utf-8') as file:
            content = content.replace('[K3D_SOURCE]', b64encode(compress(file.read().encode())).decode('utf-8'))
        with open(join(static_dir, 'require.js'), 'r', encoding='utf-8') as file:
            content = content.replace('[REQUIRE_JS]', file.read())
        with open(join(static_dir, 'fflate.js'), 'r', encoding='utf-8') as file:
            content = content.replace('[FFLATE_JS]', file.read())
        content = content.replace('[ADDITIONAL]', '')

        # Get the scene snapshot
        snapshot = self._plt.get_binary_snapshot_objects()

        # Update the plot parameters with the options
        plot_params = self._plt.get_plot_params()
        plot_params['menuVisibility'] = menu_visible
        plot_params['gridVisible'] = grid_visible
        plot_params['axesHelper'] = 1. if frame_visible else 0.
        snapshot['plot'] = plot_params

        # Compress data and fill the standalone snapshot
        data = compress(packb(snapshot, use_bin_type=True), 9)
        content = content.replace('[DATA]', b64encode(data).decode('utf-8'))

        # Write in the HTML file
        filename = f'{filename}.html' if not filename.endswith('.html') else filename
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
