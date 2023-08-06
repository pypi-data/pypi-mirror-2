# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import pilas
import os
import cairo

def cargar(ruta):
    """Intenta cargar la imagen indicada por el argumento ``ruta``.

    Por ejemplo::

        import pilas

        imagen = pilas.imagenes.cargar("mi_archivo.png")

    En caso de éxito retorna el objeto Image, que se puede asignar
    a un Actor.

    El directorio de búsqueda de la imagen sigue el siguiente orden:

        * primero busca en el directorio actual.
        * luego en 'data'.
        * por último en el directorio estándar de la biblioteca.

    En caso de error genera una excepción de tipo IOError.
    """

    if not pilas.motor:
        mensaje = "Tiene que invocar a la funcion ``pilas.iniciar()`` para comenzar."
        print mensaje
        raise Exception(mensaje)
    
    ruta = pilas.utils.obtener_ruta_al_recurso(ruta)
    return pilas.motor.cargar_imagen(ruta)

def cargar_imagen_cairo(ruta):
    ruta = pilas.utils.obtener_ruta_al_recurso(ruta)
    return cairo.ImageSurface.create_from_png(ruta)

def cargar_grilla(ruta, columnas=1, filas=1):
    """Representa una grilla de imagenes con varios cuadros de animación.

    Una grilla es un objeto que se tiene que inicializar con la ruta
    a una imagen, la cantidad de columnas y filas.

    Por ejemplo, si tenemos una grilla con 2 columnas y 3 filas
    podemos asociarla a un actor de la siguiente manera::

        grilla = pilas.imagenes.cargar_grilla("animacion.png", 2, 3)
        grilla.asignar(actor)

    Entonces, a partir de ahora nuestro actor muestra solamente un
    cuadro de toda la grilla.

    Si quieres avanzar la animacion tienes que modificar el objeto
    grilla y asignarlo nuevamente al actor::

        grilla.avanzar()
        grilla.asignar(actor)
    """
    return pilas.motor.obtener_grilla(ruta, columnas, filas)

def cargar_lienzo(ancho=640, alto=480):
    """Representa un rectangulo (inicialmente transparente) para dibujar.
    
    Internamente el lienzo tiene un contexto cairo, lo que permite
    realizar dibujos vectoriales avanzados.
    
    Generalmente este objeto se utiliza usando al actor Pizarra.
    """
    return pilas.lienzo.Lienzo(ancho, alto)

# Pronto en desuso
# Grilla = pilas.motor.Grilla
