==========
How to use
==========

This light tutorial reviews the whole project API to create 3D objects and export them in HTML.


Step 1: Create the Exporter
---------------------------

The :py:class:`Exporter<SimExporter.core.exporter.Exporter>` class is the main user API to create and export 3D objects:

.. code-block:: python

    from SimExporter.Core import Exporter

    exporter = Exporter(animation=True,
                        fps=30)

The :guilabel:`animation` option defines if the exported output will be a static 3D plot or an animation (in that case,
the frame rate :guilabel:`fps` can be specified).


Step 2: Add 3D objects
----------------------

The **Exporter** exposes the methods to create several 3D objects in the :guilabel:`objects` attribute.

* Adding **mesh** with :py:meth:`objects.add_mesh<SimExporter.core.factory.Factory.add_mesh>`:

  .. code-block:: python

      exporter.objects.add_mesh(positions=my_mesh_positions,
                                cells=my_mesh_cells)

* Adding **points** with :py:meth:`objects.add_points<SimExporter.core.factory.Factory.add_points>`:

  .. code-block:: python

      exporter.objects.add_points(positions=my_points_positions)

* Adding **arrows** with :py:meth:`objects.add_arrows<SimExporter.core.factory.Factory.add_arrows>`:

  .. code-block:: python

      exporter.objects.add_arrows(positions=my_arrows_positions,
                                  vectors=my_arrows_vectors)

* Adding standard **k3d objects** with :py:meth:`objects.add_k3d_objects<SimExporter.core.factory.Factory.add_k3d_objects>`:

  .. code-block:: python

      import k3d

      lines = k3d.lines(vertices=my_lines_vertices,
                        indices=my_lines_indices)
      exporter.objects.add_k3d_objects(lines)


Step 3: Export in HTML
----------------------

Finally, the call to :py:meth:`to_html<SimExporter.core.exporter.Exporter.to_html>` will export the 3D scene in HTML:

.. code-block:: python

    exporter.to_html(filename='scene.html')


Step 4: Include in a webpage
----------------------------

To include an exported animation, you can simply use an **HTML Iframe**:

.. code-block:: html

    <iframe src="animation.html" height="600px" width="100%"></iframe>
