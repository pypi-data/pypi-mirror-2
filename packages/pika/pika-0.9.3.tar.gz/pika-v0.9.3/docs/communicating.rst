Communicating with RabbitMQ
===========================

Applications primarily interface with RabbitMQ via the :py:meth:`channel.Channel` object. It is
with the :py:meth:`channel.Channel` that you issue commands to RabbitMQ to send messages and
receive messages.

:py:meth:`channel.Channel` is invoked by the active connection by calling *connection.channel(on_connected_callback)*. While you may
pass in a channel number, it is recommended that Pika manage this for you.

Example of opening a channel::

    import pika
    from pika.adapters import SelectConnection

    # Step #2
    def on_open(connection):
        """Called when we are fully connected to RabbitMQ"""
        # Open a channel
        connection.channel(on_channel_open)

    # Step #3
    def on_channel_open(new_channel):
        """Called when our channel has opened"""
        global channel
        channel = new_channel

    # Step #1: Connect to RabbitMQ
    connection = SelectConnection(on_open_callback=on_open)

    try:
        # Loop so we can communicate with RabbitMQ
        connection.ioloop.start()
    except KeyboardInterrupt:
        # Gracefully close the connection
        connection.close()
        # Loop until we're fully closed, will stop on its own
        connection.ioloop.start()

Once the channel is open you may use it with any of the AMQP `basic <http://www.rabbitmq.com/amqp-0-9-1-quickref.html#class.basic>`_, `exchange <http://www.rabbitmq.com/amqp-0-9-1-quickref.html#class.exchange>`_, `queue <http://www.rabbitmq.com/amqp-0-9-1-quickref.html#class.queue>`_, or `tx <http://www.rabbitmq.com/amqp-0-9-1-quickref.html#class.tx>`_ commands.

Asynchronous programming style
------------------------------

This style of programming is the only technique suitable for
programming large or complex event-driven systems in python. It makes
all control flow explicit using continuation-passing style, in a
manner reminiscent of Javascript or Twisted network programming. Once
you get your head around the unusual presentation of the code,
reasoning about control becomes much easier than in the synchronous
style.

Example that sends 1 message::

    import pika

    # Variables to hold our connection and channel
    connection = None
    channel = None

    # Called when our connection to RabbitMQ is closed
    def on_closed(frame):
        global connection

        # connection.ioloop is blocking, this will stop and exit the app
        connection.ioloop.stop()

    # Called when we have connected to RabbitMQ
    def on_connected(connection):
        global channel

        # Create a channel on our connection passing the on_channel_open callback
        connection.channel(on_channel_open)

    # Called after line #110 is finished, when our channel is open
    def on_channel_open(channel_):
        global channel

        # Our usable channel has been passed to us, assign it for future use
        channel = channel_

        # Declare a queue
        channel.queue_declare(queue="test", durable=True,
                              exclusive=False, auto_delete=False,
                              callback=on_queue_declared)

    # Called when line #119 is finished, our queue is declared.
    def on_queue_declared(frame):
        global channel

        # Send a message
        channel.basic_publish(exchange='',
                              routing_key="test",
                              body="Hello World!",
                              properties=pika.BasicProperties(
                                content_type="text/plain",
                                delivery_mode=1))

        # Add a callback so we can stop the ioloop
        connection.add_on_close_callback(on_closed)

        # Close our connection
        connection.close()

    # Create our connection parameters and connect to RabbitMQ
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.SelectConnection(parameters, on_connected)

    # Start our IO/Event loop
    connection.ioloop.start()

The asynchronous programming style can be used in both multi-threaded and
single-threaded environments. The same care must be taken when
programming in a multi-threaded environment using an asynchronous
style as is taken when using a synchronous style.

Synchronous programming style, no concurrency
---------------------------------------------
This style of programming is especially appropriate for small scripts,
short-lived programs, or other simple tasks. Code is easy to read and
somewhat easy to reason about.

Example that sends 1 message::

    import pika

    # Create our connection parameters and connect to RabbitMQ
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)

    # Open the channel
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue="test", durable=True,
                      exclusive=False, auto_delete=False)

    # Construct a message and send it
    channel.basic_publish(exchange='',
                      routing_key="test",
                      body="Hello World!",
                      properties=pika.BasicProperties(
                          content_type="text/plain",
                          delivery_mode=1))

Synchronous programming style, with concurrency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This style of programming can be used when small scripts grow bigger
(as they always seem to do). Code is still easy to read, but reasoning
about it becomes more difficult, and care must be taken when sharing
Pika resources among multiple threads of control. Beyond a certain
point, the complexity of the approach will outweigh the benefits, and
rewriting for the asynchronous style will look increasingly
worthwhile.

The main consideration when throwing threading into the mix is
locking. Each connection, and all AMQP channels carried by it, must be
guarded by a connection-specific mutex, if sharing Pika resources
between threads is desired.

The recommended alternative is sidestepping the locking complexity
completely by making sure that a connection and its channels is never
shared between threads: that each thread owns its own AMQP connection.

Channel
---------------

To get the most out of using Pika, it is advisable to know the AMQP 0-9-1
command specification. The :py:meth:`channel.Channel` documentation below
provides a detailed class level specification with links to the RabbitMQ
AMQP Reference page.

.. automodule:: channel
.. autoclass:: Channel
   :members:
   :inherited-members:
   :member-order: bysource

BlockingChannel
-----------------------------------

Implements blocking behaviors on top of the Channel class.

.. automodule:: blocking_connection
.. autoclass:: BlockingChannel
   :members:
   :inherited-members:
   :member-order: bysource
