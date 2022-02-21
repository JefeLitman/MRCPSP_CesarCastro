"""This file contain the class that structure a schedule for 
the project and estimates the duration and execution of all tasks.
Created by: Edgar RP
Version: 0.0.2
"""

import numpy as np
import utils.jobs as uj

class project_schedule():
    
    def __init__(self, project, beta_generator, n_jobs_risks, risks_per_job):
        """When you create a project schedule, it generates a schedule 
        containing all the jobs in a sequential way executed in any mode
        and also add the random duration for risk and no risk duration.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            beta_generator (np.random.beta): Instance of numpy beta random value 
            generator to get random values.
            n_jobs_risks (Integer): Quantity of jobs which will have risks.
            risks_per_job (Tuple): Tuple of the percentages of happening that risk and
            its length is the quantity of risks.
        """
        #Parameters for the object
        self.schedule = {}
        self.renewable_resources_available = np.r_[project["renewable_resources_total"]]
        self.nonrenewable_resources_available = np.r_[project["nonrenewable_resources_total"]]
        self.doubly_constrained_available = np.r_[project["doubly_constrained_total"]]
        self.total_time = project["time_horizon"]
        self.limit_time = project["duedate"]
        self.additional_time = project["tardcost"]
        #self.jobs = project["jobs"]
        self.initial_job = uj.get_initial_job(project["jobs"])
        self.final_job = uj.get_final_job(project["jobs"])

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
        to_do = [] # (job_id, priority)
        done = [] # (job_id, job_mode, job_order)
        doing = [] # (job_id, job_mode)
        job_order = 0
        priority = 1
        for i in range(self.total_time + 1):
            if i == 0: 
                job = uj.get_job(jobs, self.initial_job, 1)
                done.append((self.initial_job, 1, job_order))
                self.schedule[i] = [job]
                job_order += 1
                for j in job["successors"]:
                    to_do.append((j, priority))
                priority += 1
            else:
                if len(doing)==0: