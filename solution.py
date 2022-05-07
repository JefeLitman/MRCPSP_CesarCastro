"""This file contain the class that structure a solution for the project and estimates the base line, makespan and solution metrics as robust and quality of solution.
Created by: Edgar RP
Version: 1.2
"""

import numpy as np
import utils.jobs as uj
import utils.metrics as um
from schedule import Schedule
class Solution():
    
    def __init__(self, project, random_generator, job_params, n_scenarios_sol, initial_job, final_job, tol_invalid_sch = 10):
        """When you create a solution for the project, it generate multiples scenarios where each one have its own makespan and the same execution_line of the base line schedule but share across scenarios the risks and distribution params (mean, std) by job in all the modes. Every schedule use the priority policies to generate its own execution line.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            n_scenarios_job (Int): Number of scenarios per solution, an integer indicating how many scenarios must be created using the base line to obtain the mean makespan.
            initial_job (Int): Integer indicating the id of the initial job of the project.
            final_job (Int): Integer indicating the id of the final job of the project.
            tol_invalid_sch (Int): Tolerance of invalid schedules created, an integer indicating how many retries it can until to get a valid schedule solution.
        """
        self.renewable_resources_total = project["renewable_resources_total"]
        self.nonrenewable_resources_total = project["nonrenewable_resources_total"]
        self.doubly_constrained_total = project["doubly_constrained_total"]
        self.tolerance = tol_invalid_sch
        self.n_scenarios = n_scenarios_sol
        self.set_baseline(project, job_params)

    def __check_valid_schedule__(self, schedule, jobs):
        """This function checks the resource use of the given schedule to determine if its valid. The time of the schedule is already checked when its created to not go beyond the time_horizon of the project. Everytime is executed the use of resources is updated.
        Args:
            schedule (Schedule): Instance of the class schedule that contains and execution_line and a time_line.
            jobs (List[Dict]): A list of dictionary of each job in its raw format.
        """
        valid = len(schedule.execution_line) == len(schedule.time_line) == schedule.total_jobs
        self.renewable_resources_use = np.zeros_like(self.renewable_resources_total)
        self.nonrenewable_resources_use = np.zeros_like(self.nonrenewable_resources_total)
        self.doubly_constrained_use = np.zeros_like(self.doubly_constrained_total)
        for job_str in schedule.execution_line:
            job_id, job_mode = job_str.split(".")
            job = uj.get_job(jobs, int(job_id), int(job_mode))
            self.renewable_resources_use += job["renewable_resources_use"]
            self.nonrenewable_resources_use += job["nonrenewable_resources_use"]
            self.doubly_constrained_use += job["doubly_constrained_use"]

            # Disabling the validation of non renewable resources, but the code will be stay available
            # for i in range(len(self.nonrenewable_resources_use)):
            #     valid = valid and \
            #         self.nonrenewable_resources_use[i] <= self.nonrenewable_resources_total[i]
            for i in range(len(self.renewable_resources_use)):
                valid = valid and \
                    job["renewable_resources_use"][i] <= self.renewable_resources_total[i]
        return valid

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

    def __create_valid_base_line__(self, project, job_params, exec_line = None):
        """This function create a valid base_line given the project data, job parameters, the tolerance for invalid schedules and an execution line to use. It returns nothing but set the base_line parameter in the object.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            exec_line (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
        """
        creator = lambda: Schedule(project, job_params, exec_line) 
        for i in range(self.tolerance):
            self.base_line = creator()
            valid = self.__check_valid_schedule__(self.base_line, project["jobs"]) 
            if valid:
                break
            else:
                if exec_line:
                    creator = lambda: Schedule(project, job_params) 
                elif i == self.tolerance - 1:
                    raise InterruptedError("There was a invalid solution in the resources use, for that reason check the jobs resource use and total available resources in the project.")

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
            self.scenarios.append(Schedule(project, job_params, self.base_line.execution_line))

    def set_baseline(self, project, job_params, exec_line = None):
        """This method set the base_line, scenarios, makespan and others in the object using the project data, job parameters and optionally the execution line to create the base_line.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            exec_line (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
        """
        self.__create_valid_base_line__(project, job_params, exec_line)
        self.make_scenarios(project, job_params)
        self.__set_metrics__()

    def __set_metrics__(self):
        """This function set the basic metrics for the solution like the value, mean, std  of makespan, the solution robustness and solution quality. It doesn't return nothing."""
        self.makespan = self.base_line.time_line[-1]
        makespans = [i.time_line[-1] for i in self.scenarios] + [self.makespan]
        self.mean_makespan = np.mean(makespans)
        self.std_makespan = np.std(makespans)
        self.robustness = um.get_solution_robustness(self.base_line, self.scenarios)
        self.quality = um.get_quality_robustness(self.base_line, self.scenarios)

# En este archivo deberia hacer el secuenciador de la solucion 