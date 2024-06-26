from typing import Optional, List, Tuple, Dict, Any
from numpy import array, ndarray
import Sofa

from SimExporter.core.factory import Factory


class Recorder(Sofa.Core.Controller):

    def __init__(self, root: Sofa.Core.Node, dt: Optional[float], *args, **kwargs):
        """
        Component to record the registered Data fields in the SOFA simulation.

        :param root: Root node of the SOFA scene graph.
        :param dt: Time between each frame record.
        """

        super().__init__(name='Exporter', *args, **kwargs)

        # Add the component to the graph to catch the AnimateEndEvent
        root.addObject(self)
        self.dt = dt

        # Memory
        self.__sofa_objects_data: Dict[str, Dict[str, Any]] = {}
        self.__sofa_callbacks: Dict[str, List[Tuple[str, Sofa.Core.Data, List[ndarray]]]] = {}

    def onSimulationInitDoneEvent(self, _):
        """
        SOFA event, automatically called when the initialization on the simulation is done.
        """

        # Convert the dt between frame to the number of steps between frames
        root_dt = self.getContext().dt.value
        self.dt = root_dt if self.dt is None else max(self.dt, root_dt)
        self.dt = int(self.dt / root_dt)

    def onAnimateBeginEvent(self, _):
        """
        SOFA event, automatically called at the end of each time step of the simulation.
        """

        # Record a frame each dt
        root = self.getContext()
        if round((root.time.value + root.dt.value) / root.dt.value) % self.dt == 0:

            # Record each object
            for callbacks in self.__sofa_callbacks.values():

                # Record each callback
                for (_, data, time_series) in callbacks:

                    # Data callback (usually positions): get the current SOFA Data field value
                    if isinstance(data, Sofa.Core.Data):
                        time_series.append(data.array().copy())
                    # Function callback (usually colormap values): get the current return of the function
                    else:
                        time_series.append(data())

    def add_object(self,
                   object_type: str,
                   object_data: Dict[str, Any],
                   callbacks: List[Tuple[str, Sofa.Core.Data, List[ndarray]]]) -> None:
        """
        Define a new object to record.

        :param object_type: Type of the object('mesh', 'points, 'arrows').
        :param object_data: Core object data.
        :param callbacks: SOFA callbacks to record data.
        """

        key_name = f'{len(self.__sofa_objects_data)}_{object_type}'
        self.__sofa_objects_data[key_name] = object_data
        self.__sofa_callbacks[key_name] = callbacks

    def process(self, factory: Factory):
        """
        Add the SOFA recorded objects to the k3d scene.

        :param factory: Objects API used to build the scene.
        """

        # Add each object
        for key_name in self.__sofa_objects_data.keys():

            # Add each time series to the core data
            object_data = self.__sofa_objects_data[key_name]
            for (field_name, _, time_series) in self.__sofa_callbacks[key_name]:
                object_data[field_name] = time_series[0]
                object_data[f'time_{field_name}'] = array(time_series)

            # Add the object in the k3d scene
            factory.__getattribute__(f'add_{key_name.split("_")[1]}')(**object_data)
