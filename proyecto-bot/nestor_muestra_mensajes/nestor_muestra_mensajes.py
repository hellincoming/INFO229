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
result = channel.queue_declare(queue="mostrar", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='nestor', queue=queue_name, routing_key="mostrar")


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

print(db)
def callback(ch, method, properties, body):
    print(body)
    
    if str(body).startswith("b'[link*]"):
        links = link.find()
        n_link = link.count()
        print(links)
        count = 0
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Se han encontrado '+str(n_link)+' links en el canal')
        for i in links:
            time.sleep(1)
            count += 1
            channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body=str(count)+': '+str(i['link']))

    if str(body).startswith("b'[fecha*]"):
        fechas = fecha.find()
        n_fecha = fecha.count()
        print(fechas)
        count = 0
        channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Se han encontrado '+str(n_fecha)+' fechas importantes en el canal')
        for i in fechas:
            time.sleep(1)
            count += 1
            channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body=str(count)+': '+str(i['fecha']))

    if str(body).startswith("b'[cierre_semestre*]"):
        cierre_sem = cierre_semestre.find()
        print(cierre_sem)
        count = 0
        for i in cierre_sem:
            time.sleep(1)
            count += 1
            if count == 1:
                channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='El semestre finalizara en la siguiente fecha: '+str(i['cierre']))
        if count== 0:
            channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='no existe fecha agregada')


    if str(body).startswith("b'[programa*]"):
        programa_cu = programa_c.find()
        print(programa_cu)
        count = 0
        for i in programa_cu:
            time.sleep(1)
            count += 1
            if count == 1:
                channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='Programa del curso: '+str(i['programa']))
        
        if count== 0:
            channel.basic_publish(exchange='nestor', routing_key="publicar_slack", body='no existe programa asociado')

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

###########################################################
