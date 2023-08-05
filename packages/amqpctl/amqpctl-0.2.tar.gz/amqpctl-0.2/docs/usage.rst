Usage
=====

.. program:: amqpctl

Generally, as a comand line program, usage is::

    amqpctl [options]

General options or configuration
--------------------------------

.. cmdoption:: -s host, --server host
.. cmdoption:: -u username, --username username (default: guest)
.. cmdoption:: -p password, --password password (default: guest)

   The above options are required, as they give the coordinates of the 
   AMQP server and the login credentials

.. cmdoption:: -e name, --exchange name (default: test_exchange)
.. cmdoption:: -t type, --type type (default: direct)

   For manipulation of exchanges, the exchange name and exchange type
   are required. Exchange type can be either *direct* or *fanout*.

.. cmdoption:: -q name, --queue name (default: test_queue)

   For manipulation of queues, the queue name is required.

Actions, manipulation of exchanges and queues
---------------------------------------------

Quite purposefully, these are all long options to prevent potentially
disastrous typeos with short options.

.. cmdoption:: --delete-exchange
.. cmdoption:: --declare-exchange

.. cmdoption:: --delete-queue
.. cmdoption:: --declare-queue
.. cmdoption:: --purge-queue
