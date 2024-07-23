.. _api:

=============
API Reference
=============

.. currentmodule:: framalytics

FRAM
----

The FRAM class holds the function, aspect and connection data associated with a
given FRAM model.

FRAM objects are constructed by specifying an .xfmv file containing the FRAM
model information. The .xfmv file format is specified `here
<https://github.com/functionalresonance/FMV_Community_Edition/wiki/Data-Format-and-.xfmv-file-structure>`_.
These files are created using the `FRAM Model Visualizer (FMV)
<https://functionalresonance.com/the%20fram%20model%20visualiser/>`_.

Constructor
"""""""""""
.. autosummary::
   :toctree: api/
   :nosignatures:

   FRAM


Statistics
""""""""""
.. autosummary::
   :toctree: api/
   :nosignatures:

   FRAM.number_of_functions
   FRAM.number_of_edges


Visualization
"""""""""""""
.. autosummary::
   :toctree: api/
   :nosignatures:

   FRAM.visualize
   FRAM.highlight_data
   FRAM.highlight_function_outputs
   FRAM.highlight_full_path_from_function


Interface
"""""""""
.. autosummary::
   :toctree: api/
   :nosignatures:

   FRAM.get_function_metadata
   FRAM.get_aspect_data
   FRAM.get_connections
   FRAM.get_function_id
   FRAM.get_function_name
   FRAM.get_function_inputs
   FRAM.get_function_outputs
   FRAM.get_function_preconditions
   FRAM.get_function_resources
   FRAM.get_function_controls
   FRAM.get_function_times