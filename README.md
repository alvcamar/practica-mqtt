# practica-mqtt
En este proyecto encontramos 6 archivos Python.

Empezamos con el broker, el cual es el que se encarga de permitir la comunicacion entre clientes. Recibe 2 argumentos, la direccion del servidor (algo del estilo a 'simba.fdi.ucm.es') y el otro argumento es la ruta o la direccion en la que se va a ejecutar el broker, donde va a estar escuchando, y es algo del tipo 'clients/mi_tema/mi_subtema'.

En el numbers.py, lo que hacemos es conectarnos al topic "/numbers" que es donde vamos a estar recibiendo una serie de numeros. Tambien, se inicializan 2 variables compartidas que se van a encargar
de, cuando escuchemos un numero, identificar si es un numero de tipo 'int' o un numero de tipo 'float'. Esto se hace, por ejemplo, pasando el número a string y viendo si hay un '.' en el número.
Si le hay, el numero es float, y sin no, es un numero de tipo entero.
Se sigue este proceso indefinidamente usando el loop_forever() hasta que se pare manualmente.

En temperatura.py, se hace una cosa similar al archivo anterior. En este caso, se escucha del topic "/temperature" una serie de numeros
y un numero aleatorio entre 4 y 8. Este numero aleatorio representa el tiempo que va a estar escuchando el cliente números del topic 
"/temperature". Durante este tiempo, se van almacenando una lista (que está dentro del diccionario "userdata"), para que, despues de haber
terminado de estepar el tiempo necesario, podamos calcular la media de los valores obtenidos, así como el maximo y mínimo valor.

En temperaturahumedad.py, tenemos definidas 2 variables globales (TEMP y HUM) que representan el valor K_0 y el K_1 del enunciado, respectivamente.
En este archivo, recibimos un broker, como en el caso de 'temperatura.py', y tenemos que suscribirnos y desuscribirnos de un par de topics cuando pasen ciertas cosas:
primero se comprueba si estamos suscritos al tipic '/humidity'. Si no lo estamos, entonces suponemos que estamos escuchando del topic '/temperature', por lo que estamos escuchando un valor relacionado a una temperatura. Si ese valor es mayor estricto que la variable TEMP, entonces pasamos a escuchar al topic '/humidity' y terminamos.
Si, por otro lado, inicialmente estamos suscritos al topic '/humidity', comprobamos si tambien estamos escuchando en '/temperature' o no. Si lo estamos y la temperatura que hemos leído es menor que TEMP, entonces lo que hacemos es desuscribirnos de '/humidity'. Si no escuchamos de '/temperature' (es decir, unicamente escuchamos de '/humidity'), entonces comprobamos si el valor leído es mayor que HUM, y si lo es, nos desuscribimos.

En el archivo temporizador.py, tenemos que proporcionarle una ruta que va a ser donde va a escuchar mensajes donde se indicaran "tiempo de espera, topic y mensaje a publicar". 
Cuando ya nos ahayamos conectado a esta ruta, lo que hacemos es crear un proceso que se va a encargar de separar los 3 datos leídos y los agregara a 3 variables distintas. Después, ese proceso se "duerme" durante la cantidad de tiempo que diga el número leído y seguidamente publicara el mensaje en la dirección "topic", que es otro dato leído.

Finalmente, en el encadena_clientes.py, se crea una variable que limita la cantidad de valores leídos. Para ejecutar este chivo, se le establece un broker y va a crear un diccionario con el nombre del broker y una lista compartida. Inicialmente, nos vamos a suscribir al topic "/numbers" y vamos a escuchar numeros. Si el numero que hemos leido es primo, nos desuscribimos temporalmente del topic '/numbers' y nos suscribimos a "/humidity". Ahí, nos ponemos a escuchar valores de humedad y los añadimos a la lista compartida siempre y cuando el tamaño de la lista no supere al valor de la cota inicial y repetimos el proceso hasta que pase el numero primo leído anteriormente en segundos.
Una vez despertado, terminamos de escuchar de "/humidity", calculamos la media de los valores obtenidos y la mostramos por pantalla. Para terminar, nos volvemos a conectar al topic "/numbers".
