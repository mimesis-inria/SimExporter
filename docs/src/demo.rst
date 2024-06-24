====
Demo
====

.. raw:: html

    <iframe src="_static/meshes.html" height="600px" width="100%"></iframe>

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
                              time_colormaps=...,
                              time_positions=...)

    # Export to HTML
    exporter.process(filename='scene.html',
                     background_color='black',
                     menu_visible=True,
                     grid_visible=False,
                     frame_visible=True)
