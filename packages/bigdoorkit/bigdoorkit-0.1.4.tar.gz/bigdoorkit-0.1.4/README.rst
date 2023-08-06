BigDoor Client
==============

This is a Python client library for the `BigDoor API`_.

.. _BigDoor API: http://www.bigdoor.com/

Basic Usage
-----------

The ``bigdoorkit`` client requires your keys as provided by BigDoor::

    >>> from bigdoorkit import Client
    >>> client = Client(app_secret, app_key)
    >>> currency_types = client.get('currency_type')
    >>> from pprint import pprint
    >>> pprint(currency_types)
    [[{u'can_be_cross_publisher': 0,
       u'can_be_purchased': 1,
       u'can_be_rewarded': 0,
       u'created_timestamp': 1263933875,
       u'description': None,
       u'has_dollar_exchange_rate_integrity': 1,
       u'id': 1,
       u'modified_timestamp': 1263933875,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'Purchase'},
      {u'can_be_cross_publisher': 0,
       u'can_be_purchased': 0,
       u'can_be_rewarded': 1,
       u'created_timestamp': 1263933875,
       u'description': None,
       u'has_dollar_exchange_rate_integrity': 0,
       u'id': 2,
       u'modified_timestamp': 1263933875,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'Reward'},
      {u'can_be_cross_publisher': 0,
       u'can_be_purchased': 1,
       u'can_be_rewarded': 1,
       u'created_timestamp': 1263933875,
       u'description': u'',
       u'has_dollar_exchange_rate_integrity': 0,
       u'id': 3,
       u'modified_timestamp': 1264002256,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'Hybrid'},
      {u'can_be_cross_publisher': 1,
       u'can_be_purchased': 0,
       u'can_be_rewarded': 0,
       u'created_timestamp': 1263933875,
       u'description': None,
       u'has_dollar_exchange_rate_integrity': 1,
       u'id': 4,
       u'modified_timestamp': 1263933875,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'\xdcber'}],
     {}]

Known Issues
------------

* The ``resource`` module is under heavy development and should not be used for now.
* Very little formal documentation.
* Unit tests are sparse.

