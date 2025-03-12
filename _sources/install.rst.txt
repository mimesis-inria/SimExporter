=======
Install
=======

Requirements
------------

**SimExporter** has the following dependencies:

.. table::
    :widths: 30 30 50

    +---------------------+--------------+--------------------------------+
    | **Dependency**      | **Type**     | **Instructions**               |
    +=====================+==============+================================+
    | :Numpy:`Numpy <>`   | **Required** | :guilabel:`pip install numpy`  |
    +---------------------+--------------+--------------------------------+
    | :K3D:`K3D <>`       | **Required** | :guilabel:`pip install k3d`    |
    +---------------------+--------------+--------------------------------+
    | :Vedo:`Vedo <>`     | **Required** | :guilabel:`pip install vedo`   |
    +---------------------+--------------+--------------------------------+
    | :Colour:`Colour <>` | **Required** | :guilabel:`pip install colour` |
    +---------------------+--------------+--------------------------------+


Install
-------

Install with *pip*
""""""""""""""""""

**SimExporter** can be easily installed with :guilabel:`pip` for users:

.. code-block:: bash

    pip install git+https://github.com/mimesis-inria/SimExporter.git

You should be able to run:

.. code-block:: python

    import SimExporter


Install from sources
""""""""""""""""""""

**SimExporter** can also be installed from sources for developers:

.. code-block:: bash

    git clone https://github.com/mimesis-inria/SimExporter.git
    cd SimExporter
    pip install -e .

You should be able to run:

.. code-block:: python

    import SimExporter
