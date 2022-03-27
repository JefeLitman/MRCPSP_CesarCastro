"""This file contain the class that structure a solution for the project and estimates the base line, makespan and solution metrics as robust and quality of solution.
Created by: Edgar RP
Version: 0.6
"""

import numpy as np
import utils.jobs as uj
from schedule import Schedule
class Solution():
    
    def __init__(self, project, job_params, n_scenarios_sol, tol_invalid_sch = 10):
        """When you create a solution for the project, it generate multiples scenarios where each one have its own makespan and the same execution_line of the base line schedule but share across scenarios the risks and distribution params (mean, std) by job in all the modes. Every schedule use the priority policies to generate its own execution line.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            n_scenarios_job (Int): Number of scenarios per solution, an integer indicating how many scenarios must be created using the base line to obtain the mean makespan.
            tol_invalid_sch (Int): Tolerance of invalid schedules created, an integer indicating how many retries it can until to get a valid schedule solution.
        """
        self.renewable_resources_total = project["renewable_resources_total"]
        self.nonrenewable_resources_total = project["nonrenewable_resources_total"]
        self.doubly_constrained_total = project["doubly_constrained_total"]
        self.tolerance = tol_invalid_sch
        self.n_scenarios = n_scenarios_sol
        self.__set_parameters__(project, job_params)

    def __check_valid_schedule__(self, schedule, jobs):
        """This function checks the resource use of the given schedule to determine if its valid. The time of the schedule is already checked when its created to not go beyond the time_horizon of the project. Everytime is executed the use of resources is updated.
        Args:
            schedule (Schedule): Instance of the class schedule that contains and execution_line and a time_line.
            jobs (List[Dict]): A list of dictionary of each job in its raw format.
        """
        valid = True
        self.renewable_resources_use = np.zeros_like(self.renewable_resources_total)
        self.nonrenewable_resources_use = np.zeros_like(self.nonrenewable_resources_total)
        self.doubly_constrained_use = np.zeros_like(self.doubly_constrained_total)
        for job_str in schedule.execution_line:
            job_id, job_mode = job_str.split(".")
            job = uj.get_job(jobs, int(job_id), int(job_mode))
            self.renewable_resources_use += job["renewable_resources_use"]
            self.nonrenewable_resources_use += job["nonrenewable_resources_use"]
            self.doubly_constrained_use += job["doubly_constrained_use"]

            for i in range(len(self.nonrenewable_resources_use)):
                valid = valid and \
                    self.nonrenewable_resources_use[i] <= self.nonrenewable_resources_total[i]
            for i in range(len(self.renewable_resources_use)):
                valid = valid and \
                    job["renewable_resources_use"][i] <= self.renewable_resources_total[i]
        return valid

    def __create_valid_base_line__(self, project, job_params, exec_line = None):
        """This function create a valid base_line given the project data, job parameters, the tolerance for invalid schedules and an execution line to use. It returns nothing but set the base_line parameter in the object.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            exec_line (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
        """
        for i in range(self.tolerance):
            self.base_line = Schedule(project, job_params, exec_line) 
            if self.__check_valid_schedule__(self.base_line, project["jobs"]):
                break
            elif i == self.tolerance - 1:
                raise InterruptedError("There was a invalid solution in the resources use, for that reason check the jobs resource use and total available resources in the project.")

    def make_scenarios(self, project, job_params):
        """This function is in order to make the number of scenarios given for this solution using the created base line. This method can be only executed after a base line is setted in the solution instance object.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
        """
        self.scenarios = []
        for _ in range(self.n_scenarios):
            self.scenarios.append(Schedule(project, job_params, self.base_line.execution_line))

    def crossover_solutions(self, exec_line_0, exec_line_1, n_points, project, job_params, random_generator):
        """This function is in order to recreate a Solution instance with a new execution line, check if the execution line is valid or re make the crossover operation with an invalid execution_line. It return nothing but instead re set the base line and quantity of scenarios.
        Args:
            exec_line_0 (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
            exec_line_1 (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
            n_points (Int): An integer indicating how many points will be taking to make the crossover operation.
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
        """
        assert len(exec_line_0) == len(exec_line_1) and len(exec_line_0) > 3
        n_jobs = len(exec_line_1)
        assert n_points < int(n_jobs / 2) and n_points > 0
        prob = lambda: random_generator.cdf(random_generator.rvs())
        crossover_points = [(0, int(prob()*2))] # List of tuples with (start_index, parent)
        while len(crossover_points) < n_points + 1:
            index = int(prob()*n_jobs)
            next_parent = (crossover_points[-1][1] + 1) % 2
            if index > crossover_points[-1][0]:
                if len(crossover_points) < n_points and index != n_jobs - 1: 
                    crossover_points.append((index, next_parent))
                elif len(crossover_points) == n_points:
                    crossover_points.append((index, next_parent))
        crossover_points += [(n_jobs - 1, None)]
        
        exec_line = []
        for i in range(len(crossover_points) - 1):
            start_point, parent_index = crossover_points[i]
            end_point, _ = crossover_points[i + 1]
            parent = locals()["exec_line_{}".format(parent_index)]
            self.__add_no_repeated_jobs__(exec_line, parent, start_point, end_point - start_point)

        exec_line.append(parent[-1]) # Add at the end the last fictional job
        assert len(exec_line) == n_jobs
        self.__set_parameters__(project, job_params, exec_line)

    def __add_no_repeated_jobs__(self, exec_line, parent, start_index, n_add):
        """This function add the quantity of end_index - start_jobs in the exec line using all the jobs in the parent until the quantity of jobs is accomplished. It return None but modify the exec_line element
        Args:
            exec_line (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be added from parent.
            parent (List[Str]): A List of strings from the parent in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
            start_index (Int): An integer indicating the index in which the parent jobs will start to add.
            n_add (Int): An integer indicating how many jobs will be added from the parent to exec_line.
        """
        jobs = [int(job_string.split('.')[0]) for job_string in exec_line]
        jobs_to_add = []
        index = start_index
        while len(jobs_to_add) < n_add:
            job_id, _ = [int(i) for i in parent[index].split('.')]
            if job_id not in jobs:
                jobs_to_add.append(parent[index])
                jobs.append(job_id)
            index = (index + 1) % (len(parent) - 1) # Exclude the last job 
        exec_line += jobs_to_add

    def __set_parameters__(self, project, job_params, exec_line = None):
        """This method set the parameters of base_line, scenarios, makespan and mean_makespan in the object using the project data, job parameters and optionally the execution line to create the base_line.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            exec_line (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
        """
        self.__create_valid_base_line__(project, job_params, exec_line)
        self.make_scenarios(project, job_params)
        self.makespan = self.base_line.time_line[-1]
        self.mean_makespan = np.mean([i.time_line[-1] for i in self.scenarios])
        self.std_makespan = np.std([i.time_line[-1] for i in self.scenarios])
