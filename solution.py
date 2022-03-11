"""This file contain the class that structure a solution for the project and estimates the base line, makespan and solution metrics as robust and quality of solution.
Created by: Edgar RP
Version: 0.1
"""

import numpy as np
import utils.jobs as uj
class Solution():
    
    def __init__(self, project, random_generator, n_jobs_risks, risks_per_job):
        """When you create a solution for the project, it generate multiples scenarios where each one have its own schedule and makespan for that schedule but share across scenarios the risks and distribution params (mean, std) by job in all the modes. Every schedule use the priority policies to generate its own execution line.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
            n_jobs_risks (Integer): Quantity of jobs which will have risks.
            risks_per_job (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
        """
        self.makespan = None
        self.initial_job = uj.get_initial_job(project["jobs"])
        self.final_job = uj.get_final_job(project["jobs"])
        self.__set_job_list__(project["jobs"])
        self.__set_jobs_dist_params__(project["jobs"], random_generator)
        self.__set_jobs_risks__(n_jobs_risks, risks_per_job, random_generator)
        self.base_line = None # Generate the first sceneario which will be the base line
    
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