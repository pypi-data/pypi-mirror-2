.. currentmodule:: pyudev

:class:`Context` – the central object
=====================================

.. autoclass:: Context

   .. automethod:: __init__

   .. autoattribute:: sys_path

   .. autoattribute:: device_path

   .. autoattribute:: log_priority

   .. automethod:: list_devices

.. autoclass:: Enumerator()

   .. automethod:: match

   .. automethod:: match_subsystem

   .. automethod:: match_sys_name

   .. automethod:: match_property

   .. automethod:: match_tag

   .. automethod:: match_is_initialized

   .. automethod:: match_children

   .. automethod:: __iter__
