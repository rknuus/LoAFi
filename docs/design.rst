Introduction
============
LoAFi stands for Log Analysis Filter and intends to support interactive
analysis of log files (or any text files). The tool supports identification of
interesting patterns to radically filter all non-matching lines with the idea
to quickly understand the structure of the relevant information.

Requirements
============
* When opening a text file the system shall show the original file and the
  filtered file.
* The system shall support creation, reading, updating, and deleting of filters
  operating on single lines.
* When creating, updating, or deleting a filter the system shall update the
  filtered file.

Quality attributes
------------------
* The system shall be "reasonably reactive" to user interactions within <1s
  even for files up to 100MB.
* The system shall support Windows, Mac, and Linux.

Core use cases
==============
Currently there is only one core use case:

.. uml::

  start
  :load log file;
  repeat
    :create, update, or delete filter;
  repeat while (quit?) is (no)
  -> yes;
  stop

Volatilities
============
The following areas are either only vaguely clear at the time of the design or
might change in unknown ways in the future:

* Types of filters (e.g. exclusion filters, sorting filters, coloring filters,
  substitution filters, filters to identify lines with a common sub-pattern
  like an identifier etc.).
* Different log file formats.
* GUI technology (as experiments for my personal experience).

Decomposition
=============
Above volatilities lead to the following decomposition:

.. uml::

  package "Client layer" {
    [TogaClient]
  }

  package "Business logic layer" {
    [LogFileManager]
    [FilteringEngine]
  }

  package "Resource access layer" {
    [RawFileAccess]
  }

  package "Utilities cross-cutting layer" {
    [Pub/Sub]
  }

  [TogaClient] -down-> [LogFileManager]
  [LogFileManager] -down-> [FilterEngine]
  [FilterEngine] -down-> [RawFileAccess]
  [TogaClient] -right-> [Pub/Sub]
  [LogFileManager] -right-> [Pub/Sub]

The `FilteringEngine` might be integrated into `LogFileManager` if the
separation leaves `LogFileManager` with no other responsibility than
forwarding all requests to the `FilteringEngine`.

Use case validation
===================
%%TODO(KNR)%%

Filtering
---------
The filters shall be applied in the order they are created by the user. The
first matching filter shall be applied and no further filters shall be
applied. As a start this works for reducing filters, but requires a revisit
for mapping filters. Without in depth analysis this feels as if it should
provide the necessary flexibility at reasonable complexity.

By default all lines are excluded.

References
==========
* "Righting Software" by Juwal Loewy
* "Domain-Driven Design" by Eric Evans