CHANGES
=======

0.9 (2011-07-07)
----------------

Features
++++++++

- Add wesgi.filter_app_factory which can be used by Paste to configure wesgi as
  a filter_app_factory.
- A ``max_object_size`` option for ``wesgi.LRUCache`` to limit the maximum size
  of objects stored.
- Major refactoring to use ``httplib2`` as the backend to get ESI includes. This
  brings along HTTP Caching.
- A memory based implementation of the LRU caching algoritm at ``wesgi.LRUCache``.
- Handle ESI comments.

Bugfixes
++++++++

- Fix bug where regular expression to find ``src:includes`` could take a long time.
- Sigh. Add MANIFEST.in so necessary files end up in the tarball.


0.5 (2011-07-04)
----------------

- Initial release.
