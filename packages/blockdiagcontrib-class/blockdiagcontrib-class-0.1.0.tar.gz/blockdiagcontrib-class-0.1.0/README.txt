A plugin for `blockdiag` that provides Square node-renderer

`blockdiagcontrib-class` is a sample implementation for blockdiag plugin.

Diagram examples
================

`blockdiagcontrib-class` renders class as node's shape.

Example::

    diagram admin {
      node_width = 120;
      node_height = 120;

      // label attribute includes class name and method list combined with '|'
      A [shape = class, label = "class_name|method1()\nmethod2()"];
    }


Requirements
============

* blockdiag 0.7.0 or later


License
=======

Python Software Foundation License.
