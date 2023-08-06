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

The package requires NetworkX and SimPy to run simulations. It also requires
matplotlib for the visualisations and optionally ImageMagick for animated .gif images.

Please see http://complexnetworksim.0sites.net/ for documentation on the project.

Please note that the documentation is not complete yet. I recommend installing the zip
file (easy_install ComplexNetworkSim or pip install ComplexnetworkSim works also), as
it contains some example simulations helpful until the documentation is more complete. 