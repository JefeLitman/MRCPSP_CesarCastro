"""This file contain the class that structure a schedule for the solution and generate the execution line, time line and duration of jobs to do.
Created by: Edgar RP
Version: 1.6
"""

import numpy as np
import utils.jobs as uj

class Schedule():
    
    def __init__(self, project, job_params, random_generator = None, initial_job = None, final_job = None, base_line = None):
        """When you create a project schedule, it generates a schedule containing all the jobs in a sequential way executed in any mode and also add the random duration for risk and no risk duration.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (List[Dict]): A list of dictionaries containing all the jobs in all the modes formatted to be used as the job_list in the schedule object.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
            initial_job (Int): Integer indicating the id of the initial job of the project.
            final_job (Int): Integer indicating the id of the final job of the project.
            base_line (Schedule): An instance of a Schedule object, which is optional if the new schedule to create must be similar to the base line.
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
            if initial_job == None or final_job == None or random_generator == None:
                raise ValueError('The initial, final job and random_generator must not be empty when an base line is not given')
            self.initial_job = initial_job
            self.final_job = final_job
            self.__shuffle_jobs__(job_params, random_generator)
            self.build_schedule()
        else:
            self.initial_job = base_line.initial_job
            self.final_job = base_line.final_job
            self.job_order = base_line.job_order
            self.build_schedule(execution_line = base_line.execution_line)

    def __shuffle_jobs__(self, job_params, random_generator):
        """This function shuffle the available jobs excepting the initial and final job for schedules created without an base schedule given. It doesn't return nothing but instead set the variable job_order.
        Args:
            job_params (List[Dict]): A list of dictionaries containing all the jobs in all the modes formatted to be used as the job_list in the schedule object.
            random_generatorandom_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
        """
        self.job_order = ["{}.1".format(self.initial_job), "{}.1".format(self.final_job)]
        prob = lambda: random_generator.cdf(random_generator.rvs())
        while len(self.job_order) < len(job_params): 
            index = int(prob()*len(job_params))
            job = job_params[index]
            job_str = "{}.{}".format(job["id"], job["mode"])
            if job_str not in self.job_order:
                self.job_order.append(job_str)

    def build_schedule(self, execution_line = None, job_durations = None):
        """This function build the execution, timeline and job durations for the schedule using the job_order in the object. This function is a.k.a the sequentiator for the solution. It returns nothing but set the timeline, execution line and job durations for the schedule where the execution line contain the order from beginning to end of every job with its mode formmated like <job_id>.<mode> in a list, the timeline is also a list in the same order as execution line containing the start time for every job and job durations is a list in the same order containing the duration for that job.
        Args:
            execution_line (List[Tuples]): A optional List parameter of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed. If this parameter is given then the to_do jobs uses this list to rebuild the time_line and job duration variables.
            job_durations (List[Int]): A optional List parameter of Integers with the same order as execution_line containing the duration for every job. If this parameter is given then for every programmed job there won't be any new total duration calculation.
        """
        if job_durations != None:
            if execution_line == None:
                raise AssertionError("You can't build a schedule without an excution line given the job_durations, please be sure that you are given the two parameters")
            exec_4_duration_sorted =  np.r_[sorted(
                np.stack([execution_line, job_durations]).T,
                key = lambda x: int(x[0].split(".")[0])
            )][:,1].astype(np.int32)
        #First it must be executed the initial job
        done = [(self.initial_job, 1, 0, 0)] # (job_id, job_mode, start_tick, job_duration)
        doing = [] # (job_id, job_mode, start_tick, job_duration)
        for tick in range(self.total_time + 1):
            # Check for finished jobs
            to_delete = []
            for job_tuple in doing:
                if self.__is_finished__(job_tuple, tick):
                    to_delete.append(job_tuple)
                    done.append(job_tuple)
                    job = uj.get_job(self.job_list, job_tuple[0], job_tuple[1])
                    self.renewable_resources_use -= job["renewable_resources_use"]

            # Delete the finished jobs
            for i in to_delete:
                doing.remove(i)

            # Get all the available jobs with the finished jobs
            to_do = self.__get_available_jobs__(done, doing, execution_line)

            # Iterate over all available jobs until resources are busy
            to_delete = []
            for job in to_do:
                if job["id"] not in [i[0] for i in doing] or job["id"] not in [i["id"] for i in to_delete]:
                    if self.__is_feasible__(job):
                        to_delete.append(job)
                        if job_durations != None:
                            job_duration = exec_4_duration_sorted[job["id"] - 1]
                        else:
                            job_duration = uj.get_total_job_duration(job)
                        doing.append((job["id"], job["mode"], tick, job_duration))
                        self.renewable_resources_use += job["renewable_resources_use"]
                        self.nonrenewable_resources_use += job["nonrenewable_resources_use"]
            
            # Break the for if the done jobs is equal to total_jobs
            if len(done) == self.total_jobs:
                break
        
        if len(done) != self.total_jobs:
            raise AssertionError("The creation of a schedule was invalid due a problem selecting all the task that must be done.")

        self.execution_line = []
        self.time_line = []
        self.job_durations = []
        for job_tuple in done:
            self.execution_line.append("{}.{}".format(job_tuple[0], job_tuple[1]))
            self.time_line.append(job_tuple[2])
            self.job_durations.append(job_tuple[3])

    def __get_available_jobs__(self, done_jobs, doing_jobs, execution_line = None):
        """This function is in charge to return an ordered List with job Dicts with the structure in utils/jobs.py following the order of job_order attribute given the jobs done.
        Args:
            done_jobs (List[Tuple]): A list of tuples with elements (job_id, job_mode, start_tick, job_duration) to get the successors ids.
            doing_jobs (List[Tuple]): A list of tuples with elements (job_id, job_mode, start_tick, job_duration) to get the actual doing jobs.
            execution_line (List[Tuples]): A optional List parameter of strings in the format "<job_id>.<job_mode>" that contain the order to consider for obtaining the future jobs to do.
        """
        to_do_ids = []
        done_ids = [i[0] for i in done_jobs]
        for job_id, job_mode , st, jd in done_jobs:
            candidates = uj.get_job(self.job_list, job_id, job_mode)["successors"]
            for can_id in candidates:
                if can_id not in done_ids + [i[0] for i in doing_jobs]:
                    is_feasible = True
                    dependencies = uj.get_job(self.job_list, can_id, 1)["predecessors"] #Every job have at least one mode to be developed
                    for dep_id in dependencies:
                        is_feasible = is_feasible and (dep_id in done_ids)
                    if is_feasible:
                        to_do_ids.append(can_id)
        
        to_do = []
        order = self.job_order if execution_line == None else execution_line
        for job_str in order:
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
        available_r_resources = self.renewable_resources_total - self.renewable_resources_use
        available_nr_resources = self.nonrenewable_resources_total - self.nonrenewable_resources_use
        
        needed_r_resources = job["renewable_resources_use"]
        needed_nr_resources = job["nonrenewable_resources_use"]
        for i in range(len(self.renewable_resources_use)):
            valid = valid and needed_r_resources[i] <= available_r_resources[i]
        # for i in range(len(self.nonrenewable_resources_use)):
        #     valid = valid and needed_nr_resources[i] <= available_nr_resources[i]
        return valid

    def __is_finished__(self, job_tuple, time_tick):
        """This function check if a job have finished given the time tick where the job is. It return True or False and the job_tuple must contain the following structure (job_id, job_mode, start_tick, job_duration).
        Args:
            job_tuple (Tuple): A tuple with elements (job_id, job_mode, start_tick, job_duration) to determine if the job have already finished.
            time_tick (Int): An integer indicating in what time tick the job is currently.
        """
        job_duration = range(job_tuple[2], time_tick)
        if len(job_duration) >= job_tuple[3]:
            return True
        else:
            return False
