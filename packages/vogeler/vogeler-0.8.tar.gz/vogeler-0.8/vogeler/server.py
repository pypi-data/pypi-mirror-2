import json

from vogeler.exceptions import VogelerException
from vogeler.messaging import amqp

class VogelerServer(object):
    def __init__(self, callback_function=None, **kwargs):
        try:
            self.ch, self.queue = amqp.setup_server(kwargs['host'], kwargs['username'], kwargs['password'])
            self.callback_function = callback_function
        except:
            raise VogelerException()

    def callback(self, msg):
        message = json.loads(msg.body)
        if(self.callback_function):
            self.callback_function(message)

    def monitor(self):
        try:
            print "Vogeler(Server) is starting up"
            self.ch.basic_consume(self.queue, callback=self.callback, no_ack=True)
        except:
            raise VogelerException()

        while self.ch.callbacks:
            self.ch.wait()

    def message(self, message, durable=True):
        print "Vogeler(Server) is sending a message"
        msg = amqp.amqp.Message(json.dumps(message))
        if durable == True:
            msg.properties['delivery_mode'] = 2
        self.ch.basic_publish(msg, exchange=amqp.broadcast_exchange)

    def close(self):
        self.ch.close()

