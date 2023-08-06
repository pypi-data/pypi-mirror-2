# -*- encoding: utf-8 -*-
import random
import unittest
import pilas

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_mono_attributes(self):
        mono = pilas.actores.Mono()

        # Verifica que las rotaciones alteren el estado del personaje.
        mono.x = 100
        mono.y = 100

        self.assertEqual(mono.x, 100)
        self.assertEqual(mono.y, 100)

        # Se asegura que inicialmente no tenga rotacion asignada.
        self.assertEqual(mono.rotacion, 0)

        # Verifica que las rotaciones alteren el estado del personaje.
        mono.rotacion = 180
        self.assertEqual(mono.rotacion, 180)

        mono.rotacion = 20
        self.assertEqual(mono.rotacion, 20)

        mono.rotacion = 400
        self.assertEqual(mono.rotacion, (400 % 360))

        # Analiza que el personaje se ha agregado a la lista de actores.
        self.assertTrue(mono in pilas.actores.todos)

        # Utiliza los atributos de escala.
        self.assertEqual(mono.escala, 1)
        mono.escala = 5
        self.assertEqual(mono.escala, 5)

        # Ejecuta mas metodos del mono.
        mono.sonreir()
        mono.gritar()

        # Verifica que el personaje se pueda matar.
        mono.eliminar()
        self.assertFalse(mono in pilas.actores.todos)

    def test_posicion_y_magnitud(self):
        mono = pilas.actores.Mono()
        self.assertEqual(mono.x, 0)
        self.assertEqual(mono.y, 0)

        mono.izquierda = mono.izquierda - 100
        self.assertEqual(mono.x, -100)

        mono.derecha = mono.derecha + 100
        self.assertEqual(mono.x, 0)

        mono.arriba = mono.arriba + 100
        self.assertEquals(mono.y, 100)

        mono.abajo = mono.abajo - 100
        self.assertEquals(mono.y, 0)

    def test_colisiones(self):
        mono = pilas.actores.Mono()
        self.assertTrue(mono.colisiona_con_un_punto(0, 0))
        self.assertFalse(mono.colisiona_con_un_punto(200, 200))

if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
