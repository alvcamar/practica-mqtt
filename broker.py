"""
@author: alvarocamarafernandez
"""

"""
    El protocolo MQTT (Message Queuing Telemetry Transport) es un protocolo de comunicacion de mensajes
    Es ligero, de bajo consumo y utiliza un modelo de publicacion/suscripción para comunicarse.

        -> Es decir, los clientes se suscriben a un canal y ahí reciben los mensajes
        que son publicados por otros clientes que estén conectados al mismo canal.
"""

"""
El broker es el componente que permite la comunicación entre clientes.
Aquí se reciben los mensajes de los clientes y se distribuye a aquellos que quieran recibirlos.
"""

#APARTADO 1.-
from paho.mqtt.client import Client
import sys
#pip install paho-mqtt
#broker = "simba.fdi.ucm.es"

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    pass

def main(broker, ruta):
    client = Client()
    client.on_message = on_message
    
    print(f'Connecting on channels {ruta} on {broker}')
    client.connect(broker)

    for elem in ruta:
        client.subscribe(elem)

    client.loop_forever()

if __name__ == "__main__":
    if len(sys.argv) < 3: 
        #sys.argv es una lista. Cuando en la terminal se introduce 'Python3 nombre1.py nombre2 .....'
        #usando sys.argv podemos acceder a cada una de esas componentes (es la lista de lo que introducimos, separadas justo donde está el espacio)
        #así, para poder recuperar 'nombre2', por ejemplo, basta con poner sys.argv[1]
        #por defecto, sys.argv[0] es el nombre del script de Python (nombre.py)
        print ("Faltan argumentos por introducir. Hazlo de la siguiente manera:")
        print ("Python3 " + sys.argv[0] + " broker direccion")
        print ("Donde broker es algo del tipo: 'simba.fdi.ucm.es'")
        print ("Donde dirección es algo del siguiente estilo: 'clients/mi_tema/mi_subtema'.")
        sys.exit(1) #salimos del programa indicando que ha habido un fallo. Por eso el 1.
    else:
        broker = sys.argv[1]
        ruta = sys.argv[2:]
        main(broker, ruta)
