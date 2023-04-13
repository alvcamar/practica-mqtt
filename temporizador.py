"""
@author: alvarocamarafernandez
"""
import sys
from paho.mqtt.client import Client
from multiprocessing import Process, Lock
import paho.mqtt.publish as publish
import time

def espera_ruta_txt(userdata, msg):
    lock = userdata['lock']
    lock.acquire()
    wait, ruta, mens = str(msg.payload)[2:-1].split(',')
    time.sleep(int(wait))
    publish(ruta, payload = mens, hostname = userdata['broker'])
    lock.release()
    
    
def on_message(mqttc, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload)
    pr = Process (target = espera_ruta_txt,
                  args = (userdata, msg))
    pr.start()
    

def main(broker, ruta):
    userdata = {
        'broker': broker,
        'lock': Lock()
    }
    mqttc = Client(userdata = userdata)
    mqttc.on_message = on_message
    mqttc.connect(broker)
    mqttc.suscribe(ruta)
    #mqttc.loop_forever()
    

if __name__ == "__main__":
    if len(sys.argv) < 3:
        #sys.argv es una lista. Cuando en la terminal se introduce 'Python3 nombre1.py nombre2 .....'
        #usando sys.argv podemos acceder a cada una de esas componentes (es la lista de lo que introducimos, separadas justo donde está el espacio)
        #así, para poder recuperar 'nombre2', por ejemplo, basta con poner sys.argv[1]
        #por defecto, sys.argv[0] es el nombre del script de Python (nombre.py)
        print ("Faltan argumentos por introducir. Hazlo de la siguiente manera:")
        print ("Python3 " + sys.argv[0] + " broker ruta")
        print ("Donde broker es algo del tipo: 'simba.fdi.ucm.es'")
        print ("Y ruta es algo del tipo 'escribir/aquí' que es donde va a publicar el mensaje correspondiente")
        sys.exit(1) #salimos del programa indicando que ha habido un fallo. Por eso el 1.
    else:
        broker = sys.argv[1]
        ruta = sys.argv[2]
        main(broker)
