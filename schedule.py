"""This file contain the class that structure a schedule for the solution and generate the execution line, time line and duration of jobs to do.
Created by: Edgar RP
Version: 1.2
"""

import numpy as np
import utils.jobs as uj

class Schedule():
    
    def __init__(self, project, job_params, initial_job = None, final_job = None, execution_line = None):
        """When you create a project schedule, it generates a schedule containing all the jobs in a sequential way executed in any mode and also add the random duration for risk and no risk duration.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as <jobs_id>_<job_mode> and values contain the risk and distribution parameters (mean and std) for that job.
            initial_job (Int): Integer indicating the id of the initial job of the project.
            final_job (Int): Integer indicating the id of the final job of the project.
            execution_line (List[Str]): A optional List parameter of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
        """
        if execution_line == None:
            if initial_job == None or final_job == None:
                raise ValueError('The initial and final job must not be empty when an execution line is not given')
            self.initial_job = initial_job
            self.final_job = final_job
        else:
            self.initial_job = int(execution_line[0].split(".")[0])
            self.final_job = int(execution_line[-1].split(".")[0])
        
        self.total_time = project["time_horizon"]
        self.total_jobs = project["nr_jobs"]
        self.renewable_resources_total = project["renewable_resources_total"]
        self.nonrenewable_resources_total = project["nonrenewable_resources_total"]
        self.doubly_constrained_total = project["doubly_constrained_total"]
        self.job_list = job_params

        #self.set_jobs_duration(project["jobs"], job_params)
        self.__build_schedule__(execution_line)

    def __build_schedule__(self, execution_line = None):
        """This function build the execution timeline for the schedule using the job_list in the object. This function is an intermediary between seeing when a job is finished, what job is started and how is the resources used. It returns nothing but set the timeline and execution line for the schedule where the execution line contain the order from beginning to end of every job with its mode formmated like <job_id>.<mode> in a list and the timeline is also a list in the same order as execution line containing the start time for every job.
        Args:
            execution_line (List[Tuples]): A optional List parameter of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed. If this parameter is given then the schedule only rebuilds the time_line variable.
        """
        #First it must be executed the initial job
        done = [(self.initial_job, 1, 0)] # (job_id, job_mode, start_tick)
        doing = [] # (job_id, job_mode, start_tick)
        to_do = self.__get_available_jobs__(done)
        time = 0
        if execution_line == None:
            for tick in range(self.total_time):
                if len(to_do) != 0:
                    job_id, job_mode = self.__select_best_job__(to_do)
                    doing += [(job_id, job_mode, time)]
                    to_do.pop(to_do.index((job_id, job_mode)))
                    # aqui estoy
                else:
                    break
            while time < self.total_time:
                if len(done) < self.total_jobs - 1:
                    job_id, job_mode = self.__select_best_job__(to_do)
                    job = uj.get_job(self.job_list, job_id, job_mode)
                    done += [(job_id, job_mode, time)]
                    to_do = self.__get_available_jobs__(done)
                    time += job["total_duration"]
                else:
                    done += [(self.final_job, 1, time)]
                    time = self.total_time
        else:
            dependencies_problem = []
            for job_string in execution_line[1:-1]:
                job_id, job_mode = [int(i) for i in job_string.split(".")]
                if (job_id, job_mode) in [(i, j) for i, j, k in to_do]:
                    job = uj.get_job(self.job_list, job_id, job_mode)
                    done += [(job_id, job_mode, time)]
                    to_do = self.__get_available_jobs__(done)
                    time += job["total_duration"]
                else:
                    dependencies_problem.append((job_id, job_mode))
            
            if len(done) < self.total_jobs - 1 and len(dependencies_problem) > 0:
                for job_id, job_mode in dependencies_problem:
                    job = uj.get_job(self.job_list, job_id, job_mode)
                    done += [(job_id, job_mode, time)]
                    time += job["total_duration"]
            
            done += [(self.final_job, 1, time)]
            time = self.total_time
            
        self.execution_line = []
        self.time_line = []
        for job_id, job_mode, start_time in done:
            self.execution_line.append("{}.{}".format(job_id, job_mode))
            self.time_line.append(start_time)

    def __get_available_jobs__(self, done_jobs):
        """This function is in charge to return a List witht jobs ids of all  available jobs given the jobs done.
        Args:
            done_jobs (List[Tuple]): A list of tuples with elements (job_id, job_mode, start_tick) to get the successors ids.
        """
        to_do = []
        done_ids = [i[0] for i in done_jobs]
        for job_id, job_mode , _ in done_jobs:
            job = self.job_list['{}.{}',format(job_id, job_mode)]
            candidates = job["successors"]
            dependencies = job["predecessors"]
            for can_id in candidates:
                is_feasible = True
                for dep_id in dependencies:
                    is_feasible = is_feasible and (dep_id in done_ids)
                if is_feasible:
                    to_do.append(can_id)
        return to_do

    def __get_finished_jobs__(self, doing_jobs, actual_time):
        pass

    def __selec_random_job__(self, to_do_jobs):
        pass
    
    def __select_best_mode__(self, job_id):
        """This function apply the optimization rules to select the best following mode of the job to do and return a List with [job_id, job_mode] to be executed in the project.
        Args:
            to_do_jobs (List[Tuples]): A list of tuples with elements (job_id, job_mode, predecessor_id) of all available jobs to be executed in that time.
        """
        jobs = []
        optimization_rules = (
            lambda job: job["total_duration"],
            lambda job: np.sum(job["nonrenewable_resources_use"]),
            lambda job: np.sum(job["renewable_resources_use"]),
        )
        for job_str in self.job_list:
            if job_str.startswith("{}.".format(job_id)):
                jobs.append(self.job_list[job_str])

        if len(jobs) > len(optimization_rules):
            divisor = int(np.ceil(len(jobs) / len(optimization_rules)) - 1)
            for rule in optimization_rules:
                jobs = sorted(jobs, key=rule)[:-divisor]
        else:
            for i in range(len(jobs) - 1):
                jobs = sorted(jobs, key=optimization_rules[i])[:-1]

        best_job = jobs[0]
        return best_job["id"], best_job["mode"]
