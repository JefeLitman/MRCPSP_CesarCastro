"""This file contain the class that structure a solution for the project and estimates the base line, makespan and solution metrics as robust and quality of solution.
Created by: Edgar RP
Version: 1.4
"""

import numpy as np
import utils.jobs as uj
import utils.metrics as um
from schedule import Schedule
class Solution():
    
    def __init__(self, project, random_generator, job_params, n_scenarios_sol, initial_job, final_job):
        """When you create a solution for the project, it generate multiples scenarios where each one have its own makespan and the same execution_line of the base line schedule but share across scenarios the risks and distribution params (mean, std) by job in all the modes. Every schedule use the priority policies to generate its own execution line.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            n_scenarios_job (Int): Number of scenarios per solution, an integer indicating how many scenarios must be created using the base line to obtain the mean makespan.
            initial_job (Int): Integer indicating the id of the initial job of the project.
            final_job (Int): Integer indicating the id of the final job of the project.
        """
        self.job_params = self.__format_job_params__(dict(job_params))
        self.n_scenarios = n_scenarios_sol
        self.initial_job = initial_job
        self.final_job = final_job
        self.set_baseline(project, random_generator)

    def __format_job_params__(self, job_params):
        """This function formats the job params to be a list of dictionaries instead of a dictionary of dictionary, also, add the job id and mode to the dict. Return the job_params formatted.
        Args:
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
        """
        job_list = []
        for job_str in job_params:
            job_list.append(job_params[job_str])
            job_id, job_mode = [int(i) for i in job_str.split(".")]
            job_list[-1]["id"] = job_id
            job_list[-1]["mode"] = job_mode

        return job_list

    def make_scenarios(self, project, job_params, n_scenarios = None):
        """This function is in order to make the number of scenarios given for this solution using the created base line. This method can be only executed after a base line is setted in the solution instance object.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            n_scenarios (Int): An integer indicating how many scenarios must be recreated using the base line.
        """
        self.scenarios = []
        total = n_scenarios if n_scenarios else self.n_scenarios
        for _ in range(total):
            self.scenarios.append(Schedule(project, job_params, base_line = self.base_line))

    def set_baseline(self, project, random_generator,  exec_line = None):
        """This method set the base_line, scenarios, makespan and others in the object using the project data, job parameters and optionally the execution line to create the base_line.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
            exec_line (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
        """
        if exec_line == None:
            self.base_line = Schedule(project, self.job_params, random_generator, self.initial_job, self.final_job)
        else:
            self.base_line.build_schedule(execution_line = exec_line)
        self.make_scenarios(project, self.job_params)
        self.set_metrics()

    def set_metrics(self):
        """This function set the basic metrics for the solution like the value, mean, std  of makespan, the solution robustness and solution quality. It doesn't return nothing."""
        self.makespan = self.base_line.time_line[-1]
        makespans = [i.time_line[-1] for i in self.scenarios]
        self.mean_makespan = np.mean(makespans)
        self.std_makespan = np.std(makespans)
        self.solution = um.get_solution_robustness(self.base_line, self.scenarios)
        self.quality = um.get_quality_robustness(self.base_line, self.scenarios)
 