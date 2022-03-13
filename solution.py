"""This file contain the class that structure a solution for the project and estimates the base line, makespan and solution metrics as robust and quality of solution.
Created by: Edgar RP
Version: 0.2
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
            n_scenearios_job (Int): Number of scenarios per solution, an integer indicating how many scenarios must be created using the base line to obtain the mean makespan.
            tol_invalid_sch (Int): Tolerance of invalid schedules created, an integer indicating how many retries it can until to get a valid schedule solution.
        """
        self.renewable_resources_total = project["renewable_resources_total"]
        self.nonrenewable_resources_total = project["nonrenewable_resources_total"]
        self.doubly_constrained_total = project["doubly_constrained_total"]
        # Create a valid base line checking every creation
        for i in range(tol_invalid_sch):
            self.base_line = Schedule(project, job_params) 
            if self.__check_valid_schedule__(self.base_line, project["jobs"]):
                break
            elif i == tol_invalid_sch - 1:
                raise InterruptedError("There was a invalid solution in the resources use, for that reason check the jobs resource use and total available resources in the project.")
        # Creation of every scenario for the base line
        self.scenarios = []
        for _ in range(n_scenarios_sol):
            self.scenarios.append(Schedule(project, job_params, self.base_line.execution_line))

        self.makespan = self.base_line.time_line[-1]
        self.mean_makespan = np.mean([i.time_line[-1] for i in self.scenarios])

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
