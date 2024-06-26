from typing import Optional, Union, List

import Sofa

from SimExporter.core.exporter import Exporter as _Exporter
from SimExporter.sofa.factory import Factory
from SimExporter.sofa.recorder import Recorder


class Exporter(_Exporter):

    def __init__(self, root: Sofa.Core.Node, dt: Optional[float] = None, animation: bool = False, fps: float = 25.):
        """
        Main API to create a scene with 3D objects and export a standalone 3D plot or animation in an HTML file.

        :param root: Root node of the SOFA scene graph.
        :param dt: Time between each frame record.
        :param animation: If False, a static 3D plot is exported. If True, a 3D animation is exported if time series
                          are associated to a 3D object.
        :param fps: Frame rate of the animation (not used if animation = False).
        """

        super().__init__(animation=animation, fps=fps)

        # Create a SOFA factory to easily add 3D objects in the scene and record SOFA Data
        self.__recorder = Recorder(root=root, dt=dt)
        self.objects = Factory(recorder=self.__recorder, plt=self._plt, animation=animation)
        self.dt = dt

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

        # Add the sofa objects to the scene
        self.__recorder.process(factory=self.objects)

        # Export HTML file
        super().process(filename=filename,
                        background_color=background_color,
                        grid_visible=grid_visible,
                        menu_visible=menu_visible,
                        frame_visible=frame_visible)
