# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

'''
Pilas
=====

Pilas es un motor para crear videojuegos de manera
simple y didáctica.

Para iniciar el módulo debes llamar a la función ``iniciar``::

    pilas.iniciar()

y opcionalmente puedes indicarle parámetros si quieres. Te
recomiendo ejecutar la siguiente funcion para obtener
mas informacion::

    help(pilas.iniciar)

Ten en cuenta que este motor se pude ejecutar directamente
desde la consola interactiva de python, así podrás investigar
y divertirte de forma interactiva.

Puedes obtener mas información en nuestro sitio:

    - http:://www.pilas-engine.com.ar

'''


mundo = None
motor = None
bg = None
__all__ = ['actores', 'iniciar', 'terminar', 'ejecutar', 'interpolar', 'avisar']

import utils
import motores
import simbolos
import os
import sys
import time
import estudiante
import baseactor
import colores
import imagenes
import sonidos
import actores
import fps
from interpolaciones import Lineal
import dispatch
import eventos
import habilidades
import ventana
import comportamientos
import escenas
import fondos
from control import Control
from camara import Camara
import copy
import pilas.utils
from mundo import Mundo
from colisiones import Colisiones
import random
import ejemplos
import red

import atajos
import fisica
import grupo
import lienzo
import interfaz















    
    
# Carga el modulo de autocompletado si esta
# en sesion interactiva.
if utils.esta_en_sesion_interactiva():
    utils.cargar_autocompletado()

def iniciar(ancho=640, alto=480, titulo='Pilas', usar_motor='pysfml', modo='detectar', rendimiento=60, economico=True, gravedad=(0, -90)):
    """Inicia el motor y abre la ventana principal del videojuego.
    
    Esta funcion se ejecuta al principio de cualquier juego, porque
    además de crear la ventana principal inicializa otros submódulos
    de pilas que te permites hacer mas cosas.
    
    Un ejemplo de invocación para esta función es::

        pilas.iniciar()

    aunque también puedes indicarle puntualmente el valor de algún
    argumento::

        pilas.iniciar(titulo='titulo de mi juego')

    """
    global mundo
    global motor


    (motores_disponibles, recomendado) = obtener_motores_disponibles()

    if not recomendado:
        raise Exception("No se encuentran bibliotecas multimedia, tiene que instalar SFML o pygame.")

    if usar_motor not in motores_disponibles.keys():
        print "Advertencia: El sistema solicitado '%s' no esta disponible, cargado '%s' en su lugar." %(usar_motor, recomendado)
        usar_motor = recomendado

    if usar_motor not in ['sfml', 'pysfml']:
        print "Advertencia: Te recomendamos usar SFML, busca en la web de pilas como instalarlo..."

    motor = motores_disponibles[usar_motor]()

    pilas.colisiones = Colisiones()

    # Cuando inicia en modo interactivo se asegura
    # de crear la ventana dentro del mismo hilo que
    # tiene el contexto opengl.
    if modo == 'detectar':
        if utils.esta_en_sesion_interactiva():
            iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo + " [Modo Interactivo]", rendimiento, economico, gravedad)
        else:
            mundo = pilas.mundo.Mundo(ancho, alto, titulo, rendimiento, economico, gravedad)
            escenas.Normal()
    elif modo == 'interactivo':
        iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo + " [Modo Interactivo]", rendimiento, economico, gravedad)
    else:
        raise Exception("Lo siento, el modo indicado es invalido, solo se admite 'interactivo' y 'detectar'")


def iniciar_y_cargar_en_segundo_plano(ancho, alto, titulo, fps, economico, gravedad):
    "Ejecuta el bucle de pilas en segundo plano."
    import threading
    global gb

    bg = threading.Thread(target=__iniciar_y_ejecutar, args=(ancho, alto, titulo, fps, economico, gravedad))
    bg.start()

def reiniciar():
    actores.utils.eliminar_a_todos()

def __iniciar_y_ejecutar(ancho, alto, titulo, fps, economico, gravedad, ignorar_errores=False):
    global mundo

    mundo = Mundo(ancho, alto, titulo, fps, economico, gravedad)
    escenas.Normal()
    ejecutar(ignorar_errores)

def terminar():
    "Finaliza la ejecución de pilas y cierra la ventana principal."
    global mundo

    if mundo:
        mundo.terminar()
    else:
        print "No se puede terminar pilas porque no la has inicializado."

def ejecutar(ignorar_errores=False):
    """Pone en funcionamiento el ejecutar principal.

    Esta función se comporta diferente en modo interactivo y modo script:

        - En modo interactivo pilas generará un hilo que te permitirá seguir
          escribiendo comandos interactivamente y viendo los resultados en la
          ventana.

        - En modo script, la función bloqueará la ejecución lineal de tu
          script y llevará todo el control al bucle de juego interno de
          pilas. Por lo que es buena idea poner la linea ``pilas.ejecutar()`` al
          final del script...
    """
    global mundo

    if mundo:
        mundo.ejecutar_bucle_principal(ignorar_errores)
    else:
        raise Exception("Tienes que llamar a pilas.iniciar() antes de ejecutar el juego.")


def interpolar(valor_o_valores, duracion=1, demora=0, tipo='lineal'):
    """Retorna un objeto que representa cambios de atributos progresivos.
    
    El resultado de esta función se puede aplicar a varios atributos
    de los actores, por ejemplo::
        
        bomba = pilas.actores.Bomba()
        bomba.escala = pilas.interpolar(3)

    Esta función también admite otros parámetros cómo:

        - duracion: es la cantidad de segundos que demorará toda la interpolación.
        - demora: cuantos segundos se deben esperar antes de iniciar.
        - tipo: es el algoritmo de la interpolación, puede ser 'lineal'.
    """


    import interpolaciones

    algoritmos = {
            'lineal': interpolaciones.Lineal,
            }

    if algoritmos.has_key('lineal'):
        clase = algoritmos[tipo]
    else:
        raise ValueError("El tipo de interpolacion %s es invalido" %(tipo))

    # Permite que los valores de interpolacion sean un numero o una lista.
    if not isinstance(valor_o_valores, list):
        valor_o_valores = [valor_o_valores]

    return clase(valor_o_valores, duracion, demora)

anterior_texto = None

def avisar(mensaje):
    "Emite un mensaje en la ventana principal."
    global anterior_texto

    if anterior_texto:
        anterior_texto.eliminar()

    texto = actores.Texto(mensaje)
    texto.magnitud = 22
    texto.centro = ("centro", "centro")
    texto.izquierda = -310
    texto.abajo = -230
    anterior_texto = texto

def ver(objeto):
    "Imprime en pantalla el codigo fuente asociado a un objeto o elemento de pilas."
    import inspect

    try:
        codigo = inspect.getsource(objeto.__class__)
    except TypeError:
        codigo = inspect.getsource(objeto)

    print codigo

def obtener_motores_disponibles():
    """Retorna una tupla con dos valores: los motores disponibles y el recomendado.

    Dado que pilas soporta dos motores multimadia (SFML y Pygame), esta
    función intentará decetar cual de estos sistemas multimedia esta
    disponible en el sistema.
    """

    motores_disponibles = {}
    sistema_recomendado = None
    import pilas.motores

    try:
        motores_disponibles['pygame'] = pilas.motores.Pygame
        sistema_recomendado = "pygame"
    except AttributeError:
        pass

    try:
        motores_disponibles['sfml'] = pilas.motores.pySFML
        motores_disponibles['pysfml'] = pilas.motores.pySFML
        sistema_recomendado = "sfml"
    except AttributeError:
        pass

    return (motores_disponibles, sistema_recomendado)


def ejecutar_cada(segundos, funcion):
    """Ejecuta una funcion con la frecuencia que indica el argumento segundos.
    
    La funcion ejecutada tiene que retornar True para volver a
    ejecutarse, si retorna False se elimina el temporizador y la funcion
    no se vuelve a ejecutar.
    """
    pilas.mundo.agregar_tarea(segundos, funcion)
