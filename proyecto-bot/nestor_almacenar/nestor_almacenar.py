#!/usr/bin/env python
import pika
import time
import os
import pymongo

from pymongo import MongoClient
client = MongoClient()
time.sleep(30)


########### CONNEXIÓN A RABBIT MQ #######################
HOST = os.environ['RABBITMQ_HOST']

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'nestor'
channel.exchange_declare(exchange='nestor', exchange_type='topic', durable=True)

#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="guardar", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='nestor', queue=queue_name, routing_key="guardar")


##########################################################


########## ESPERA Y HACE UN BUSQUEDA WIKIPEDIA CUANDO RECIBE UN MENSAJE ####

print(' [*] Waiting for messages. To exit press CTRL+C')

#########CONEXION MONGODB############
client = MongoClient(host=os.environ['MONGO_HOST'], port=int(os.environ['MONGO_PORT']))
db = client.slack
link = db.link
fecha = db.fecha
cierre_semestre = db.cierre
programa_c = db.programa

def callback(ch, method, properties, body):
    print(body)
    if str(body).startswith("b'[link]"):
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Guardando link, por favor espere')
        query = str(body)[9:-1]
        print(query)
        result=link.insert_one({"link": query})
        print(result)
        ########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Link guardado correctamente '+query)
    
    if str(body).startswith("b'[fecha]"):
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Guardando fecha por favor espere')
        query = str(body)[10:-1]
        print(query)
        result=fecha.insert_one({"fecha": query})
        print(result)
        ########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Fecha guardado correctamente '+query)

    if str(body).startswith("b'[programa]"):
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Guardando programa')
        query = str(body)[13:-1]
        print(query)
        result=programa_c.insert_one({"programa": query})
        print(result)
        ########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='programa agregado correctamente: '+query)

    if (str(body).startswith("b'[cierre_semestre]") and cierre_semestre.count() < 1):
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Guardando fecha por favor espere')
        query = str(body)[20:-1]
        print(query)
        result=cierre_semestre.insert_one({"cierre": query})
        print(result)
        ########## PUBLICA EL RESULTADO COMO EVENTO EN RABBITMQ ##########
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Fecha guardado correctamente '+query)

    if (str(body).startswith("b'[cierre_semestre]") and cierre_semestre.count() >= 1):
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='la fecha ya esta agregada, si desea agregar una nueva elimine la anterior ')

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

###########################################################
