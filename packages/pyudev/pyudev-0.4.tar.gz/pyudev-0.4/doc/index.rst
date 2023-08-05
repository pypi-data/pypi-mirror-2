Welcome to pyudev's documentation!
==================================

pyudev is a Python_ and PyQt4_ binding to libudev_, the hardware management
library and service found in modern linux systems.  It is available under
the same licence as the original library, which is the `GNU LGPL 2.1`_ (see
:doc:`licencing` for details).


Installation
------------

The current release is pyudev |release|, available in the `Python Package
Index`_.  Refer to the :doc:`changes` for a list of important changes since
the last release [#changes]_.

pyudev is built atop of ctypes_ and does not contain any native code.  The
only requirements are Python 2.6 or newer (Python 3.x is not supported as of
now) and apipkg_.  Installation is rather simple, just run::

   pip install pyudev

apipkg_ will be installed automatically.  To load the module, libudev must
be available.


Documentation
-------------

Usage of pyudev is rather simple:

>>> from pyudev import Context
>>> context = Context()
>>> devices = context.list_devices()
>>> for device in devices.match_subsystem('input').match_property('ID_INPUT_MOUSE', True):
...     if device.sys_name.startswith('event'):
...         device.parent['NAME']
...
u'"Logitech USB-PS/2 Optical Mouse"'
u'"Broadcom Corp"'
u'"PS/2 Mouse"'

Please read the :doc:`API documentation <api>` for detailed information.


Contribution and Development
----------------------------

Please report issues and feature requests to the `issue tracker`_
[#issues]_.

Development happens on GitHub_.  The complete source code is available in a
git_ repository::

   git clone git://github.com/lunaryorn/pyudev.git

Feel free to fork the repository.  Pull requests and patches are welcome!


.. rubric:: Footnotes

.. [#changes] A detailed list of changesets_ is also available.
.. [#issues] Please assign proper labels to the issue and provide detailed
   information about the issue.  If possible, include copied and pasted
   output from the programs, or a code example demonstrating the issue.


.. _`GNU LGPL 2.1`: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
.. _Python: http://www.python.org/
.. _PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/intro/
.. _libudev: http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev.html
.. _`Python Package Index`: http://pypi.python.org/pypi/pyudev
.. _ctypes: http://docs.python.org/library/ctypes.html
.. _apipkg: http://pypi.python.org/pypi/apipkg/
.. _`issue tracker`: http://github.com/lunaryorn/pyudev/issues
.. _GitHub: http://github.com/lunaryorn/pyudev
.. _git: http://www.git-scm.com/
.. _changesets: http://github.com/lunaryorn/pyudev/commits/master


.. toctree::
   :hidden:

   api
   licencing
   changes
