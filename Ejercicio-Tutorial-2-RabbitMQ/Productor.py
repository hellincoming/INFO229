#!/usr/bin/env python
import pika
import sys

#Nuestra tarea pasada como argumento
message = ' '.join(sys.argv[1:]) or "Hello World!"

#Conexión al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Creación de la cola
channel.queue_declare(queue='Wikipedia')
channel.queue_declare(queue='Youtube')
#Publicación del mensaje
channel.basic_publish(exchange='',
                      routing_key='Wikipedia',
                      body=message)
print(" [x] Sent %r" % message)

channel.basic_publish(exchange='',
                      routing_key='Youtube',
                      body=message)
print(" [x] Sent %r" % message)

connection.close()




