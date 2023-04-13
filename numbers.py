#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: alvarocamarafernandez
"""
import sys
from paho.mqtt.client import Client
from multiprocessing import Lock, Process, Value
import traceback


def contar(userdata, msg):
    mqttc = Client()
    mqttc.connect(userdata['broker'])
    print("Realizando conteo de números...")
    if '.' in msg.payload: #esto representa que el valor leido es un numero de tipo float
        userdata['float'].value += 1
    else: #si no tiene el '.', tenemos un entero
        userdata['int'].value +1
    mqttc.publish(payload = "cantidad de numeros reales leídos: " + str(userdata['float'].value) + 
                  "cantidad de enteros leídos: " + str(userdata['int'].value))
    print("recuento finalizado")
    mqttc.disconnect()
    


def on_message(mqttc, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload)
    lock = userdata['lock']
    lock.acquire()
    try:
        process = Process(target = contar, 
                          args = (userdata, msg) )
        process.start()
    except:
        traceback.print_exc()
    finally:
        lock.release()

def main(broker, num_int, num_float):
    userdata = {
        'lock':Lock(),
        'broker': broker,
        'int': num_int,
        'float': num_float
    }
    mqttc = Client(userdata = userdata)
    mqttc.on_message = on_message
    

    mqttc.connect(broker)

    mqttc.subscribe('/numbers')

    mqttc.loop_forever() #está activo hasta que lo paremos manualmente.
    

if __name__ == "__main__":
    if len(sys.argv) < 2: 
        #sys.argv es una lista. Cuando en la terminal se introduce 'Python3 nombre1.py nombre2 .....'
        #usando sys.argv podemos acceder a cada una de esas componentes (es la lista de lo que introducimos, separadas justo donde está el espacio)
        #así, para poder recuperar 'nombre2', por ejemplo, basta con poner sys.argv[1]
        #por defecto, sys.argv[0] es el nombre del script de Python (nombre.py)
        print ("Faltan argumentos por introducir. Hazlo de la siguiente manera:")
        print ("Python3 " + sys.argv[0] + " broker")
        print ("Donde broker es algo del tipo: 'simba.fdi.ucm.es'")
        sys.exit(1) #salimos del programa indicando que ha habido un fallo. Por eso el 1.
    else:
        broker = sys.argv[1]
        num_float, num_int = Value('i', 0), Value('i', 0)
        main(broker, num_int, num_float)
