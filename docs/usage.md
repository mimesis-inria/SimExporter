# How to use

This light tutorial reviews the whole project API to create 3D objects and export them in HTML.


## Step 1: Create the Exporter

The **Exporter** class is the main user API to create and export 3D objects:

``` python
from SimExporter.Core import Exporter

exporter = Exporter(animation=True,
                    fps=30)
```

The `animation` option defines if the exported output will be a static 3D plot or an animation (in that case, the frame
rate `fps` can be specified).


## Step 2: Add 3D objects

The **Exporter** exposes the methods to create several 3D objects in the `objects` attribute.

### Mesh

``` python
exporter.objects.add_mesh(positions=my_mesh_positions,
                          cells=my_mesh_cells)
```
  
### Points

``` python
exporter.objects.add_points(positions=my_points_positions)
```
  
### Arrows

``` python
exporter.objects.add_arrows(positions=my_arrows_positions,
                            vectors=my_arrows_vectors)
```

### Others

``` py
import k3d

lines = k3d.lines(vertices=my_lines_vertices,
                  indices=my_lines_indices)
exporter.objects.add_k3d_objects(lines)
```
  

## Step 3: Export in HTML

Finally, the call to `process` will export the 3D scene in HTML:

``` python
exporter.process(filename='scene.html')
```
