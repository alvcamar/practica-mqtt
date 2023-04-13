"""
@author: alvarocamarafernandez
"""

import sys
from paho.mqtt.client import Client
from multiprocessing import Lock
import traceback
import random
import time

# def on_log(mqttc, userdata, level, string):
#     print("LOG", userdata, level, string)

def on_message(mqttc, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload)
    pos = 12 #len('/temperature') = 12
    lock = userdata['lock']
    lock.acquire()
    try:
        datos = msg.topic[pos:] #leemos todo lo que está delante de '/temperature'
        dic = userdata['temperatura']
        temp = float (msg.payload)
        if datos in dic:
            dic[datos].append(temp)
        else:
            dic[datos] = [temp]
    except:
        traceback.print_exc()
    finally:
        lock.release()

def main(broker, client_s):
    userdata = {
        'lock': Lock(),
        'broker': broker,
        'temperatura': {}
    }
    mqttc = Client(userdata = userdata)
    #mqttc.enable_logger()
    mqttc.on_message = on_message
    #mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(client_s)
    
    mqttc.loop_start()
    
    while True:
        #mqttc.on_log = on_log
        pause = random.randint(4,8)
        time.sleep(pause)
        val_lst = list(userdata['temperatura'].values())
        media = sum(val_lst)/len(val_lst)
        maxi = max(val_lst)
        mini = min(val_lst)
        print ("Valor máximo encontrado: " + str(maxi))
        print ("Valor minimo encontrado: " + str(mini))
        print ("Valor medio: " + str(media))
        keys_lst = list(userdata['temperatura'].keys())
        for clave in keys_lst:
            userdata['temperatura'][clave] = [] #reseteamos los valores


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
        client_s = "/temperature"
        main(broker, client_s)
