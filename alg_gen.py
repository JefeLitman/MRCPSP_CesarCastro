"""This file contain the class that execute and do the genetic algorithm of 
the given project with mutation, crossover and other methods neccessary.
Created by: Edgar RP
Version: 0.0.1
"""

import numpy as np
from coche import coche as carro
from copy import deepcopy

class genetica():
    
    def __init__(self,poblacion,ganadores,dim_mapa):
        self.tam_poblacion = poblacion
        self.num_ganadores = ganadores

        if (self.tam_poblacion < self.num_ganadores):
            self.num_ganadores = self.tam_poblacion

        self.poblacion = []

        self.reset()
        self.crear_poblacion(dim_mapa)

    def reset(self):
        self.iteracion = 0
        self.radio_mutacion = 1
        self.mejor_poblacion = (None,None)
        self.mejor_puntaje = 999

    def get_posiciones(self):
        posiciones = []
        for ind in self.poblacion:
            posiciones.append(ind.posicion)
        return posiciones

    def set_posicion_inicial(self,posicion_inicial):
        for coche in self.poblacion:
            coche.posicion = deepcopy(posicion_inicial)

    def get_estados(self):
        return [c.vivo for c in self.poblacion]

    def revivir_poblacion(self):
        for ind in self.poblacion:
            ind.vivo = True

    def crear_poblacion(self,limites):
        for i in range(self.tam_poblacion):
            coche = carro(i)
            coche.definir_limites(limites[0],limites[1])
            self.poblacion.append(coche)

    def escoger_ganadores(self):
        """Esta funcion ordena la poblacion entera por puntuacion"""
        self.poblacion = sorted(self.poblacion,key=lambda objeto: objeto.puntuacion)

    def ordenar_poblacion(self):
        self.poblacion = sorted(self.poblacion,key=lambda objeto: objeto.indice)

    def actualizar_mejor(self):
        if(self.poblacion[0].puntuacion <= self.mejor_puntaje):
            self.mejor_puntaje = self.poblacion[0].puntuacion
            self.mejor_poblacion = (self.poblacion[0].indice,self.iteracion)

    def activar_individuos(self,punto_final,mapa):
        """punto_final es la coordenada en el mapa seleccionada por el usuario
        entregada en forma de lista [Xf,Yf]"""
        for ind in self.poblacion:
            if( ind.vivo == True):
                ind.mover(punto_final)
                if(ind.lugar_valido(mapa) == False):
                    ind.matar()

    def evolucionar_poblacion(self):
        """Funcion que se encarga de evolucionar toda la poblacion a la sig
        generacion, si llega a fallar retornara Falso"""
        """Escojo los ganadores"""
        self.escoger_ganadores()

        """Actualizo al mejor de la poblacion"""
        self.actualizar_mejor()

        """Reviso que cada ganador este en un lugar valido o de lo contrario
        vuelvo a crear una poblacion. En caso de que todos sean validos defino
        el radio de mutacion"""
        for ind in self.poblacion[:4]:
            if(ind.vivo == False):
                return False #Si retorno falso es que no se pudo evolucionar

        """Si todos los ganadores estan bien entonces modifico el radio de mutacion
        y aumento la iteracion"""
        self.radio_mutacion = np.random.random()

        """Se va rellenar la poblacion con los nuevos hijos"""
        nue_poblacion = self.poblacion[:4]

        #1 Hijo de los dos mejores ganadores
        nue_poblacion.append(self.cruzar_individuos(self.poblacion[0],self.poblacion[1],self.poblacion[4].get_indice()))

        #3 Hijos de dos ganadores aleatorios
        for i in range(5,8):
            ind_padre = np.random.randint(4)
            ind_madre = np.random.randint(4)
            nue_poblacion.append(self.cruzar_individuos(self.poblacion[ind_padre], self.poblacion[ind_madre], self.poblacion[i].get_indice()))

        #2 Hijos como copia directa
        for i in range(8,10):
            copia = deepcopy(self.poblacion[np.random.randint(4)])
            copia.indice = self.poblacion[i].get_indice()
            nue_poblacion.append(copia)

        """Ahora es tiempo de mutar los individuos de la nueva poblacion"""
        for ind in nue_poblacion:
            self.mutar_individuo(ind)

        """Debemos colocar en posicion los nuevos individuos de la nueva poblacion"""
        for i,ind in enumerate(nue_poblacion):
            limites = self.poblacion[i].get_limites()
            ind.definir_limites(limites[0],limites[1])
            ind.posicion = self.poblacion[i].posicion

        """Por ultimo debemos cambiar la poblacion y ordenarla por indice"""
        self.poblacion = nue_poblacion
        self.ordenar_poblacion()
        self.iteracion = self.iteracion + 1
        return True

    def cruzar_individuos(self,padre,madre,indice):
        """Funcion que realiza el cruzado, el padre es de quien mas
        heredara"""
        hijo = carro(indice)

        for i in range(len(hijo.cerebro.red_neuronal)):
            divisor = np.random.randint(1,padre.cerebro.red_neuronal[i].W.shape[1])

            w_padre = padre.cerebro.red_neuronal[i].W[:,:divisor]
            w_madre = madre.cerebro.red_neuronal[i].W[:,divisor:]
            b_padre = padre.cerebro.red_neuronal[i].b[:,:divisor]
            b_madre = madre.cerebro.red_neuronal[i].b[:,divisor:]

            hijo.cerebro.red_neuronal[i].W = np.append(w_padre,w_madre,axis=1)
            hijo.cerebro.red_neuronal[i].b = np.append(b_padre, b_madre, axis=1)

        return hijo

    def mutar_individuo(self,individuo):
        """Esta funcion muta los w y b del individuo en cada capa
        No retorna nada porque supuestamente debe modificar el individuo original"""
        for capa in individuo.cerebro.red_neuronal:
            self.mutar_variable(capa.W)
            self.mutar_variable(capa.b)

    def mutar_variable(self,variable):
        """Esta funcion muta cada elemento de la variable tomando probabilidad aleatoria
        No retorna nada porque supuestamente debe modificar la variable original"""
        for i in range(variable.shape[0]):
            for j in range(variable.shape[1]):
                if(np.random.random() < self.radio_mutacion):
                    variable[i,j] = variable[i,j] * np.random.random()