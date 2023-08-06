Ver. 0.4.2 - 2010 Nov 17
============================
* Added ``tags`` in tests. You can now run specific tags::

	python runtests.py hash
	
 will run tests specific to hashtables.
* Added ``bench`` module for benchmarking. To run benchmark::

	python runbench.py
	python runbench.py tag1 tag2
	
* Removed ``ts`` tests since the timeseries structure is not in redis yet. You can run them by setting tag ``ts``.
* **54** tests.

Ver. 0.4.1 - 2010 Nov 14
============================
* Added ``CONTRIBUTING`` to distribution.
* Corrected spelling error in Exception ``ObjectNotFound`` exception class.
* Added initial support for ``Map`` structures. Ordered Associative Containers.
* **63 tests**


Ver. 0.4 - 2010 Nov 11
============================
* Development status set to ``beta``.
* **This version is incompatible with previous versions**.
* Documentation hosted at github.
* Added new ``contrib`` module ``djstdnet`` which uses `djpcms`_ content management system to display an admin
  interface for a :class:`stdnet.orm.StdModel`. Experimental for now.
* Added :class:`stdnet.CacheClass` which can be used as django_ cache backend. For example, using redis database 11 as cache is obtained by::

	CACHE_BACKEND = 'stdnet://127.0.0.1:6379/?type=redis&db=11&timeout=300'
	
* Overall refactoring of :mod:`stdnet.orm` and :mod:`stdnet.backends` modules.
* Lazy loading of models via the :mod:`stdnet.dispatch` module.
* Added :mod:`stdnet.dispatch` module from django_.
* Added :class:`stdnet.orm.AtomField` subclasses. 
* Before adding elements to a :class:`stdnet.orm.MultiField` the object needs to be saved, i.e. it needs to have a valid id.
* Made clear that :class:`stdnet.orm.StdModel` classes are mapped to :class:`stdnet.HashTable`
  structures in a :class:`stdnet.BackendDataServer`.
* Moved ``structures`` module into ``backends`` directory. Internal reorganisation of several modules.
* Added ``app_label`` attribute to :class:`stdnet.orm.DataMetaClass`.
* **47 tests**

Ver. 0.3.3 - 2010 Sep 13
========================================
* If a model is not registered and the manager method is accessed, it raises ``ModelNotRegistered``
* Changed the way tests are run. See documentation
* ``redis`` set as requirements
* **29 tests**

Ver. 0.3.2 - 2010 Aug 24
========================================
* Bug fixes
* Fixed a bug on ``orm.DateField`` when ``required`` is set to ``False``
* ``Changelog`` included in documentation
* **27 tests**

Ver. 0.3.1 - 2010 Jul 19
========================================
* Bug fixes
* **27 tests**

Ver. 0.3.0 - 2010 Jul 15
========================================
* Overall code refactoring
* Added ListField and OrderedSetField with Redis implementation
* ``StdModel`` raise ``AttributError`` when method/attribute not available. Previously it returned ``None``
* ``StdModel`` raise ``ModelNotRegistered`` when trying to save an instance of a non-registered model
* **24 tests**

Ver. 0.2.2 - 2010 Jul 7
========================================
* ``RelatedManager`` is derived by ``Manager`` and therefore implements both all and filter methods
* **10 tests**

Ver. 0.2.0  - 2010 Jun 21
========================================
* First official release in pre-alpha
* ``Redis`` backend
* Initial ``ORM`` with ``AtomField``, ``DateField`` and ``ForeignKey``
* **8 tests**


.. _djpcms: http://djpcms.com
.. _django: http://www.djangoproject.com/
