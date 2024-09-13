====
Demo
====


.. tabs::

    .. group-tab:: Meshes

        .. raw:: html

            <iframe src="_static/html/meshes.html" height="600px" width="100%"></iframe>

    .. group-tab:: Points

        .. raw:: html

            <iframe src="_static/html/points.html" height="600px" width="100%"></iframe>

.. tabs::

    .. group-tab:: Meshes

        .. code-block:: python

            from SimExporter.core import Exporter

            # Load data
            ...

            # Create the exporter
            exporter = Exporter(animation=True,
                                fps=50)

            # Add meshes to the scene
            exporter.objects.add_mesh(positions=...,
                                      cells=...,
                                      color=[192, 28, 40],
                                      alpha=0.6,
                                      flat_shading=False,
                                      time_positions=...)
            exporter.objects.add_mesh(positions=...,
                                      cells=...,
                                      alpha=1.,
                                      flat_shading=False,
                                      wireframe=True,
                                      colormap_name='Reds',
                                      colormap_range=[0, 1],
                                      time_colormap_values=...,
                                      time_positions=...)

            # Export to HTML
            exporter.to_html(filename='scene.html',
                             background_color='black',
                             menu_visible=True,
                             grid_visible=False,
                             frame_visible=True)

    .. group-tab:: Points

        .. code-block:: python

            from SimExporter.core import Exporter

            # Load data
            ...

            # Create the exporter
            exporter = Exporter(animation=True,
                                fps=50)

            # Add meshes to the scene

            exporter.objects.add_points(positions=...,
                                        point_size=2.,
                                        colormap_name='YlOrBr',
                                        time_colormap_values=...,
                                        time_positions=...)
            exporter.objects.add_mesh(positions=...,
                                      cells=...,
                                      color='grey',
                                      alpha=0.6,
                                      wireframe=True,
                                      time_positions=...)

            # Export to HTML
            exporter.to_html(filename='scene.html',
                             background_color='black',
                             menu_visible=True,
                             grid_visible=False,
                             frame_visible=True)
