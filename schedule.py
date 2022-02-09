"""This file contain the class that structure a schedule for 
the project and estimates the duration and execution of all tasks.
Created by: Edgar RP
Version: 0.0.1
"""

import numpy as np
import utils.jobs as uj

class project_schedule():
    
    def __init__(self, project, beta_generator):
        """When you create a project schedule, it generates a schedule 
        containing all the jobs in a sequential way executed in any mode
        and also add the random duration for risk and no risk duration.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            beta_generator (np.random.beta): Instance of numpy beta random value 
            generator to get random values.
        """
        #Parameters for the scheself.__dule object
        self.schedule = []
        self.jobs_to_do = []
        self.jobs_done = []
        self.jobs_doing = []
        self.renewable_resources_available = np.r_[project["renewable_resources_total"]]
        self.nonrenewable_resources_available = np.r_[project["nonrenewable_resources_total"]]
        self.doubly_constrained_available = np.r_[project["doubly_constrained_total"]]
        self.total_time = project["time_horizon"]
        self.limit_time = project["duedate"]
        self.additional_time = project["tardcost"]
        #self.jobs = project["jobs"]
        self.initial_job = uj.get_initial_job(project["jobs"])
        self.final_job = uj.get_final_job(project["jobs"])

    def __set_to_do_jobs__(self, jobs):
        """This function fills the list of to do jobs with dictionaries of every job in
        the following structure:
        {
            "id": Int,
            "total_duration"
            "base_duration"
            "
        }
        """