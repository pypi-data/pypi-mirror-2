ComplexNetworkSim is a Python package for the simulation of agents 
connected in a complex network.  

The framework can can create a virtual complex network with virtual agents
that can interact with each other. This can be used for example to study
the spread of an epidemic over this simulated network and compare it
with a phenomenon in the real world. Agent-based simulation tools
generally operate on a simple topology such as grids or lattices, but
this framework goes beyond this limitation by providing support for
simulation over complex topologies (i.e. any kind of non-regularly 
connected graph). In addition, this project is not 
limited to a static network, but also takes into account temporal
networks, where processes can dynamically change the underlying network
structure over time. 

The package requires `NetworkX`_ and `SimPy`_ to run simulations. It also requires
`matplotlib`_ (and `NumPy`_) for the visualisations and optionally `ImageMagick`_ for animated .gif images.

Please see http://complexnetworksim.0sites.net/ for documentation, installation instructions, background information and how to get started using this package.

Please note that the documentation does not explain the more advanced features in detail yet, but it is complete for the simple cases. Please refer to the examples folder for code structures beyond those detailed in the documentation so far. 

As this is my first project I would appreciate some feedback. Thanks! :)

.. _SimPy: http://simpy.sourceforge.net/
.. _NetworkX: http://networkx.lanl.gov/
.. _ImageMagick: http://www.imagemagick.org/
.. _NumPy: http://sourceforge.net/projects/numpy/files/NumPy/
.. _matplotlib: http://sourceforge.net/projects/matplotlib/files/matplotlib/