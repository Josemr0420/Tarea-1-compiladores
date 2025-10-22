Minimización de Autómatas Finitos Deterministas (AFD)

Este programa implementa el algoritmo de minimización de autómatas finitos deterministas (AFD) utilizando el método de tabla de distinguibilidad.
Permite identificar pares de estados equivalentes que pueden ser combinados para reducir el tamaño del autómata sin alterar su comportamiento.

Autor: José Miguel Muñoz Ríos
Fecha: 05/08/2025
Lenguaje: Python 3

REQUISITOS PREVIOS

Antes de ejecutar el programa, asegúrate de tener instalado:

Python 3.8 o superior

Un archivo de entrada llamado input.txt en el mismo directorio del script

Puedes verificar tu versión de Python ejecutando:
python3 --version

ESTRUCTURA DE ARCHIVOS

Tu carpeta debe contener los siguientes archivos:

proyecto_afd/
│
├── minimizacion_afd.py (Código fuente principal)
├── input.txt (Archivo de entrada con los datos del autómata)
└── README.txt (Este archivo de instrucciones)

FORMATO DEL ARCHIVO input.txt

El programa leerá los datos del autómata desde el archivo input.txt.
Su estructura debe ser la siguiente:

<num_casos>
<num_estados>
<alfabeto_separado_por_espacios>
<estados_finales_separados_por_espacios>
<matriz_de_transiciones>

EJEMPLO DE ARCHIVO DE ENTRADA

Contenido del archivo input.txt:

1
6
a b
1 2 5
0 1
2 3
4 3
5 5
5 5
5 5

(Nota: Cada fila de la matriz de transiciones corresponde a un estado del autómata.
En este caso hay 6 estados numerados del 0 al 5 y dos símbolos: 'a' y 'b'.)

INTERPRETACIÓN DEL ARCHIVO

Número de casos: 1

Número de estados: 6

Alfabeto: a, b

Estados finales: 1, 2, 5

Matriz de transiciones:

Estado	con 'a' →	con 'b' →
0	0	1
1	2	3
2	4	3
3	5	5
4	5	5
5	5	5
EJECUCIÓN DEL PROGRAMA

Coloca el archivo input.txt en el mismo directorio donde se encuentra el script minimizacion_afd.py

Abre una terminal en esa carpeta

Ejecuta el siguiente comando:

python3 minimizacion_afd.py

EJEMPLO DE SALIDA EN CONSOLA
Procesando 1 caso(s) de prueba...
Caso 1:

Pares de estados equivalentes: (3,4)
Total de pares equivalentes: 1

==================================================
Procesamiento completado.

VALIDACIONES INCLUIDAS

El programa verifica automáticamente:

Que el número de estados sea positivo

Que los estados finales estén dentro del rango válido

Que la matriz de transiciones tenga las dimensiones correctas

Que los estados destino sean válidos

Si se detecta un error, se mostrará un mensaje claro indicando el problema.

NOTAS ADICIONALES

Si el archivo input.txt no existe o tiene formato incorrecto, el programa mostrará un error explicativo.

Los pares equivalentes se muestran en el formato (i,j).

Si no existen estados equivalentes, el programa imprimirá “None”.

En este ejemplo, el programa identifica que los estados 3 y 4 son equivalentes.
