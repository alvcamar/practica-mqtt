"""
@author: alvarocamarafernandez
"""

import sys
from paho.mqtt.client import Client
TEMP = 25
HUM = 50
#canales donde se escucha:
    #temperature
    #humidity

def on_message(mqttc, userdata, msg):
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload)
    if not mqttc.is_suscribed("humidity"):
        temp = float(msg.payload)
        if temp > userdata['temp_K0']: #si supera la temperatura, tenemos que suscribirnos
            print("Temperatura registrada mayor que " + str(userdata['temp_K0']))
            mqttc.suscribe("humidity")
    else: #estamos suscritos al topic '/humidity'
        #distingimos si estamos escuchando de '/humidity' o de '/temperature'
        if 'temperature' in msg.topic: #estamos escuchando de "/temperature"
            temp = float(msg.payload)
            if temp < userdata['temp_K0']:
                print("Temperatura registrada menor que " + str(userdata['temp_K0']))
                mqttc.unsuscribe('humidity')
        else: #escuchamos de '/humidity'
            hum = float(msg.payload)
            if hum > userdata['humid_K1']:
                print("Humedad registrada mayor que " + str(userdata['hum_K1']))
                mqttc.unsuscribe('humidity')
    


def main(broker):
    """
    Tenemos que suscribirnos y desuscribirnos al topic 'humidity'
    cuando pasen ciertas cosas. Inicialmente NO estamos suscritos.
    Para comprobar si estamos suscritos, utilizamos la funcion
    is_suscribed().
    is_suscribed(topic) -> True si estamos suscritos a topic
                        -> False en otro caso
    """
    userdata = {'temp_K0': TEMP,
                'humid_K1': HUM,
    }
    
    mqttc = Client(userdata = userdata)
    mqttc.on_message = on_message
    mqttc.connect(broker)
    mqttc.loop_forever()


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
        main(broker)
