"""This file contain the class that execute and do the genetic algorithm of the given project with mutation, crossover and other methods neccessary.
Created by: Edgar RP
Version: 0.1
"""

import numpy as np
from solution import Solution
import utils.jobs as uj

class Genetic_Algorithm():
    
    def __init__(self, project, random_generator, poblation_size, n_winners, n_jobs_risks, risks_per_job, n_scenarios_sol, tol_invalid_sch):
        """This class is the main class, it creates the quantity of solutons given, make crossover, mutation and select the best samples. This class contain important classes as to create a new generation and stablish the risks in the jobs.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
            poblation_size (Int): Quantity of solutions to have for generation.
            n_winners (Int): Quantity of solutions that will be taken into account as parents to generate the new sons. It can not be greater than poblation_size.
            n_jobs_risks (Int): Quantity of jobs which will have risks.
            risks_per_job (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
            n_scenearios_job (Int): Number of scenarios per solution, an integer indicating how many scenarios must be created using the base line to obtain the mean makespan.
            tol_invalid_sch (Int): Tolerance of invalid schedules created, an integer indicating how many retries it can until to get a valid schedule solution.
        """
        if poblation_size <= n_winners:
            raise AssertionError("The size of the poblation must be greater than the quantity of winners for generation. Values given {} <= {}".format(
                poblation_size,
                n_winners
            ))
        self.n_total_sol = poblation_size
        self.n_winners = n_winners

        self.initial_job = uj.get_initial_job(project["jobs"])
        self.final_job = uj.get_final_job(project["jobs"])
        self.__set_job_list__(project["jobs"])
        self.__set_jobs_dist_params__(project["jobs"], random_generator)
        self.__set_jobs_risks__(n_jobs_risks, risks_per_job, random_generator)
        
        self.solutions = []
        for _ in range(poblation_size):
            self.solutions.append(
                Solution(project, self.jobs, n_scenarios_sol, tol_invalid_sch)
            )

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

    def __set_job_list__(self, jobs):
        """This function set the dictionary of all the jobs in the project. This dictionary doesn't take into account the modes for the jobs but instead only focus in summarize the general parameters accross the scenearios like the risks and distribution params in the value elements.
        Args:
            jobs (List[Dict]): A list of dictionary of each job.
        """
        self.jobs = {}
        for job in jobs:
            job_id = job["id"]
            if job_id not in self.jobs.keys():
                if job_id == self.initial_job:
                    self.jobs[job_id] = {"initial": True}
                elif job_id == self.final_job:
                    self.jobs[job_id] = {"final": True}
                else:
                    self.jobs[job_id] = {}

    def __set_jobs_dist_params__(self, jobs, random_generator):
        """This function set the distribution params (mean and std) for all the jobs, excluding initial and final, to have common parameters to generate random values in its duration and risks.
        Args:
            jobs (List[Dict]): A list of dictionary of each job.
            random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
        """
        prob = lambda: random_generator.cdf(random_generator.rvs())
        for job_id in self.jobs:
            if job_id not in [self.initial_job, self.final_job]:
                modes = uj.get_job_modes_duration(jobs, job_id)
                index = int(prob()*len(modes)) #Chose a random mode to use as base duration to generate the mean and std for all the jobs
                duration = modes[list(modes.keys())[index]]
                mean, std = uj.get_job_dist_params(duration, random_generator)
                self.jobs[job_id]["normal_dist_mean"] = mean
                self.jobs[job_id]["normal_dist_std"] = std

    def __set_jobs_risks__(self, n_jobs, risks_per, random_generator):
        """This function set the risk for every job in the solution given the n_jobs with risks and risk_per job.
        Args:
            n_jobs (Integer): Quantity of jobs which will have risks.
            risks_per (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
            random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
        """
        prob = lambda: random_generator.cdf(random_generator.rvs())
        jobs_modified = []
        while len(jobs_modified) < n_jobs:
            index = int(prob()*len(self.jobs))
            job_id = list(self.jobs.keys())[index]
            if job_id not in [self.initial_job, self.final_job] + jobs_modified:
                mean = self.jobs[job_id]["normal_dist_mean"]
                std = self.jobs[job_id]["normal_dist_std"]
                risks = uj.get_job_risks(risks_per, mean, std)
                is_none = True
                for r in risks:
                    is_none = is_none and risks[r] == None
                    self.jobs[job_id][r] = risks[r]
                if not is_none:
                    jobs_modified.append(job_id)

        # Let the remaining jobs with risks as None value
        for job_id in self.jobs:
            if job_id not in [self.initial_job, self.final_job] + jobs_modified:
                risks = uj.get_job_risks(np.zeros_like(risks_per), 0, 1)
                for r in risks:
                    self.jobs[job_id][r] = risks[r]
