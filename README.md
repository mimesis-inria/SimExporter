# SimExporter

A small **python** tool to **export standalone 3D interactive animations** in **HTML files** using K3D.

![gallery](docs/src/_static/gallery.gif)


## Presentation

**SimExporter** is a Python module for creating **3D interactive scenes** of various 3D objects using 
[**K3D**](http://www.k3d-jupyter.org/) and exporting a **3D plot** or a **3D animation** in a **standalone HTML file**.

This HTML file can then be shared and opened in any browsers and laptop, it can also be easily integrated into a
**website** or **presentation slides**.


## Gallery

See the interactive gallery in the [**documentation**](https://mimesis-inria.github.io/SimExporter/) !

![gallery](docs/src/_static/gallery.png)

Try an integrated animation on our [**team website**](https://mimesis.inria.fr/) !

![gallery](docs/src/_static/mimesis_website.gif)


## Install

``` bash
# Option 1 (USERS): install with pip
$ pip install git+https://github.com/mimesis-inria/SimExporter.git

# Option 2 (DEVS): install as editable
$ git clone https://github.com/mimesis-inria/SimExporter.git
$ cd SimExporter
$ pip install -e .
```


## How to use

The code below is the minimum for exporting a **3D scene** with various objects to a **standalone HTML file**: 

``` python
from SimExporter.core import Exporter

# Create the exporter
exporter = Exporter()

# Add 3D objects to the scene
exporter.objects.add_points(positions=...)
exporter.objects.add_mesh(positions=..., 
                          cells=...)

# Export the scene to an HTML file
exporter.to_html(filename='scene.html')
```

The code below is the minimum for exporting a **3D animation** with various objects to a **standalone HTML file**:

``` python
from SimExporter.core import Exporter

# Create the exporter
exporter = Exporter(animation=True)

# Add 3D objects to the scene
exporter.objects.add_points(positions=..., 
                            time_positions=...)
exporter.objects.add_mesh(positions=..., 
                          cells=..., 
                          time_positions=...)

# Export the animation to an HTML file
exporter.to_html(filename='animation.html')                          
```

To integrate the HTML file into a website or presentation slides, see the dedicated section in the 
[**documentation**](https://mimesis-inria.github.io/SimExporter/).


## Documentation

See more ⟶ [**documentation**](https://mimesis-inria.github.io/SimExporter/)
