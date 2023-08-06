============
Ibidem Utils
============

``ibidem.util.workpool``
------------------------

A simple, generic threaded workpool. When creating the pool, you specify how many workers should be started.
When adding work orders to the pool queue, the next available worker will pick up the order and execute it.
Allows subclassing to create specialized workers. Allows the user to supply the queue instead of letting the
pool create it.

``ibidem.util.downloader``
--------------------------

A work order for ``ibidem.util.workpool`` to download arbitrary URLs in an efficient manner. Allows specifying
callbacks to handle the file completed downloads, and to update progress.
