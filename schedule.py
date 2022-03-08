"""This file contain the class that structure a schedule for the scenerio and generate the timeline of jobs to do.
Created by: Edgar RP
Version: 0.0.4
"""

import numpy as np
import utils.jobs as uj

class schedule():
    
    def __init__(self, project, random_generator, n_jobs_risks, risks_per_job):
        """When you create a project schedule, it generates a schedule containing all the jobs in a sequential way executed in any mode and also add the random duration for risk and no risk duration.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            beta_generator (np.random.beta): Instance of numpy beta random value generator to get random values.
            n_jobs_risks (Integer): Quantity of jobs which will have risks.
            risks_per_job (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
        """
        #Parameters for the object
        self.schedule = {}
        self.renewable_resources_available = project["renewable_resources_total"] #Its mantained as tuple
        self.nonrenewable_resources_available = np.array(project["nonrenewable_resources_total"])
        self.doubly_constrained_available = np.array(project["doubly_constrained_total"])
        self.total_time = project["time_horizon"]
        self.total_jobs = project["nr_jobs"]
        self.initial_job = uj.get_initial_job(project["jobs"])
        self.final_job = uj.get_final_job(project["jobs"])
        

    def __get_available_jobs__(self, to_do, done, beta_generator):
        """This function return a randomized list of the availables 
        jobs ids based in the to_do list and the done list.
        Args:
            to_do (List[Tuple]): A list of tuples with (job_id, predecessor_id).
            done (List[Tuple]): A list of tuples with (job_id, job_mode, start_tick).
            beta_generator (np.random.beta): Instance of numpy beta random value 
            generator to get random values.
        """
        candidates = []
        for job_id, predecessor_id in to_do:
            if predecessor_id in [j[0] for j in done]:
                candidates.append(job_id)
        available = []
        while len(candidates) != 0:
            available.append(
                candidates.pop(int(beta_generator() * len(candidates)))
            )
        return available

    def __get_finished_jobs__(self, doing, time):
        """This function return a list of the finished jobs ids and the 
        using the doing jobs list.
        Args:
            doing (List[Tuple]): A list of tuples with (job_id, job_mode, start_tick).
            time (Integer): An integer specifying in what tick of time is actually.
        """
        finished = []
        for job_id, _, start in doing:
            if abs(start - time) == 0:
                finished.append(job_id)
        return finished

    def __set_jobs_durations__(self, jobs, beta_generator):
        """This function stablish the new base duration for all the jobs 
        excluding the initial and final jobs. Return nothing
        Args:
            jobs (List[Dict]): A list of dictionary of each job.
            beta_generator (np.random.beta): Instance of numpy beta random value 
            generator to get random values.
        """
        for job in jobs:
            if job["id"] not in [self.initial_job, self.final_job]:
                job["init_random_duration"] = uj.get_new_job_base_duration(job["base_duration"], beta_generator)

    def __set_jobs_durations_risks__(self, jobs, n_jobs, risks_per, beta_generator):
        """This function stablish the new total durations with risk
        for all the jobs excluding the initial and final jobs.
        Args:
            jobs (List[Dict]): A list of dictionary of each job.
            n_jobs (Integer): Quantity of jobs which will have risks.
            risks_per (Tuple): Tuple of the percentages of happening that risk and
            its length is the quantity of risks.
            beta_generator (np.random.beta): Instance of numpy beta random value 
            generator to get random values.
        """
        jobs_modified = []
        while len(jobs_modified) < n_jobs:
            for job in jobs:
                if job["id"] not in [self.initial_job, self.final_job]:
                    duration = job["init_random_duration"]
                    risks = uj.get_job_risks(duration, risks_per, beta_generator)
                    if risks["total_duration"] != duration:
                        for key in risks:
                            job[key] = risks[key]
                    if job["id"] not in jobs_modified:
                        jobs_modified.append(job["id"])

    def __check_resources__(self):
        pass

    def __build_schedule__(self, jobs, beta_generator):
        """This function build the schedule dict for all the jobs given 
        and return a dict with all the ticks in time. The structure of 
        the schedule will be keys the time t and values a list of jobs done 
        in that tick:
        {
            0: [
                {
                    "id": Int,
                    "mode": Int,
                    "total_duration": Int
                    "successors": List[Int]
                }
            ],
            1: [
                {
                    "id": Int,
                    "mode": Int,
                    "total_duration": Int
                    "successors": List[Int]
                }
            ]
            ...
        }
        Args:
            jobs (List[Dict]): A list of dictionary of each job.
            beta_generator (np.random.beta): Instance of numpy beta random value 
                generator to get random values.
        """
        to_do = [] # (job_id, predecessor_id)
        done = [] # (job_id, job_mode, start_tick)
        doing = [] # (job_id, job_mode, start_tick)
        for i in range(self.total_time + 1):
            if i == 0: 
                job = uj.get_job(jobs, self.initial_job, 1)
                done.append((self.initial_job, 1, i))
                self.schedule[i] = [job]
                for j in job["successors"]:
                    to_do.append((j, self.initial_job))
            else:
                # Check if there are jobs doing it and get what jobs finish
                # Append new jobs in to_do after a job finish
                # Try to do as many jobs as it can
                if len(doing) == 0:
                    # There are no jobs, then add some to doing
                    candidates = []
                    for job_id, predecessor_id in to_do:
                        if predecessor_id in [j[0] for j in done]:
                            candidates.append(job_id)
                    while len(candidates) != 0:
                        pass
                        #idx = np.floor(beta_generator() * len(candidates))
                        #job_id = 

        # Falta revisar que los recursos se mantengan bien en el trasncurso del proyecto
        # Falta comprobar que al finalizar el calendario este el total de jobs
        # Falta cambiar la estructura del dict que pasara a ser la lista de done
        # Falta calcular el tiempo total usado por el cronograma