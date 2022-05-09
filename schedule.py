"""This file contain the class that structure a schedule for the solution and generate the execution line, time line and duration of jobs to do.
Created by: Edgar RP
Version: 1.3.1
"""

import numpy as np
import utils.jobs as uj

class Schedule():
    
    def __init__(self, project, random_generator, job_params, initial_job = None, final_job = None, base_line = None):
        """When you create a project schedule, it generates a schedule containing all the jobs in a sequential way executed in any mode and also add the random duration for risk and no risk duration.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
            job_params (List[Dict]): A list of dictionaries containing all the jobs in all the modes formatted to be used as the job_list in the schedule object.
            initial_job (Int): Integer indicating the id of the initial job of the project.
            final_job (Int): Integer indicating the id of the final job of the project.
            execution_line (Schedule): An instance of a Schedule object, which is optional if the new schedule to create must be similar to the base line.
        """
        self.total_time = project["time_horizon"]
        self.total_jobs = project["nr_jobs"]
        self.renewable_resources_total = project["renewable_resources_total"]
        self.nonrenewable_resources_total = project["nonrenewable_resources_total"]
        self.doubly_constrained_total = project["doubly_constrained_total"]
        self.renewable_resources_use = np.zeros_like(self.renewable_resources_total)
        self.nonrenewable_resources_use = np.zeros_like(self.nonrenewable_resources_total)
        self.doubly_constrained_use = np.zeros_like(self.doubly_constrained_total)
        self.job_list = job_params
        if base_line == None:
            if initial_job == None or final_job == None:
                raise ValueError('The initial and final job must not be empty when an execution line is not given')
            self.initial_job = initial_job
            self.final_job = final_job
            self.__shuffle_jobs__(job_params, random_generator)
            #self.__build_schedule__()
        else:
            self.initial_job = base_line.initial_job
            self.final_job = base_line.final_job
            self.job_order = base_line.job_order

    def __shuffle_jobs__(self, job_params, random_generator):
        """This function shuffle the available jobs excepting the initial and final job for schedules created without an base schedule given. It doesn't return nothing but instead set the variable job_order.
        Args:
            job_params (List[Dict]): A list of dictionaries containing all the jobs in all the modes formatted to be used as the job_list in the schedule object.
            random_generatorandom_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
        """
        self.job_order = ["{}.1".format(self.initial_job), "{}.1".format(self.final_job)]
        prob = lambda: random_generator.cdf(random_generator.rvs())
        while len(self.job_order) < self.total_jobs: 
            index = int(prob()*len(job_params))
            job = job_params[index]
            job_str = "{}.{}".format(job["id"], job["mode"])
            if job_str not in self.job_order:
                self.job_order.append(job_str)

    def __build_schedule__(self, execution_line = None):
        """This function build the execution timeline for the schedule using the job_list in the object. This function is an intermediary between seeing when a job is finished, what job is started and how is the resources used. It returns nothing but set the timeline and execution line for the schedule where the execution line contain the order from beginning to end of every job with its mode formmated like <job_id>.<mode> in a list and the timeline is also a list in the same order as execution line containing the start time for every job.
        Args:
            execution_line (List[Tuples]): A optional List parameter of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed. If this parameter is given then the schedule only rebuilds the time_line variable.
        """
        #First it must be executed the initial job
        done = [(self.initial_job, 1, 0, 0)] # (job_id, job_mode, start_tick, job_duration)
        doing = [] # (job_id, job_mode, start_tick, job_duration)
        time = 0
        for tick in range(self.total_time):
            # Check for finished jobs
            for i in range(len(doing)):
                if self.__is_finished__(doing[i]):
                    job_tuple = doing.pop(i)
                    done.append(job_tuple)
            # Get all the available jobs with the finished jobs
            to_do = self.__get_available_jobs__(done)

            # Iterate over all available jobs until resources are busy
            while len(to_do) > 0:
                pass

    def __get_available_jobs__(self, done_jobs):
        """This function is in charge to return an ordered List with job Dicts with the structure in utils/jobs.py following the order of job_order attribute given the jobs done.
        Args:
            done_jobs (List[Tuple]): A list of tuples with elements (job_id, job_mode, start_tick, job_duration) to get the successors ids.
        """
        to_do_ids = []
        done_ids = [i[0] for i in done_jobs]
        for job_id, job_mode , st, jd in done_jobs:
            job = uj.get_job(self.job_list, job_id, job_mode)
            candidates = job["successors"]
            dependencies = job["predecessors"]
            for can_id in candidates:
                is_feasible = True
                for dep_id in dependencies:
                    is_feasible = is_feasible and (dep_id in done_ids)
                if is_feasible:
                    to_do_ids.append(can_id)
        
        to_do = []
        for job_str in self.job_order:
            job_id, job_mode = [int(i) for i in job_str.split(".")]
            if job_id in to_do_ids:
                job = uj.get_job(self.job_list, job_id, job_mode)
                to_do.append(job)
        return to_do

    def __is_feasible__(self, job):
        """This function check the use of availability of resources taking into account the total and used resourced. It returns True or False if the given job can not be done at the moment.
        Args:
            job (Dict): A dictionary of a job with the structure showed in utils/jobs.py.
        """
        valid = True
        available_r_resources = np.abs(self.renewable_resources_total - self.renewable_resources_use)
        available_nr_resources = np.abs(self.nonrenewable_resources_total - self.nonrenewable_resources_use)
        
        needed_r_resources = job["renewable_resources_use"]
        needed_nr_resources = job["nonrenewable_resources_use"]
        # Disabling the validation of non renewable resources, but the code will be stay available
        for i in range(len(self.nonrenewable_resources_use)):
            valid = valid and needed_nr_resources[i] <= available_nr_resources[i]
        for i in range(len(self.renewable_resources_use)):
            valid = valid and needed_r_resources[i] <= available_r_resources[i]
        return valid

    def __is_finished__(self, job_tuple, time_tick):
        """This function check if a job have finished given the time tick where the job is. It return True or False and the job_tuple must contain the following structure (job_id, job_mode, start_tick, job_duration).
        Args:
            job_tuple (Tuple): A tuple with elements (job_id, job_mode, start_tick, job_duration) to determine if the job have already finished.
            time_tick (Int): An integer indicating in what time tick the job is currently.
        """
        job_duration = range(job_tuple[3], time_tick)
        if len(job_duration) >= job_tuple[4]:
            return True
        else:
            return False

    def __can_use_more_resources__(self, to_do_jobs):
        """This function check for every possible job if its possible to be programmed taking into account the actual use of resources. It returns True if its possible to program at least one job of the to_do_jobs list Dicts or False is there is no any job.
        Args:
            to_do_jobs (List[Dict]): A list of dictionaries of each job following the order of job_order attribute.
        """
        for job in to_do_jobs:
            if self.__is_feasible__(job):
                return True
        return False

    def __update_states__(self, time_tick, doing_jobs, done_jobs):
        """This function is in construction"""

