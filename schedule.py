"""This file contain the class that structure a schedule for the solution and generate the execution line and time line of jobs to do.
Created by: Edgar RP
Version: 1.1.1
"""

import numpy as np
import utils.jobs as uj

class Schedule():
    
    def __init__(self, project, job_params, execution_line = None):
        """When you create a project schedule, it generates a schedule containing all the jobs in a sequential way executed in any mode and also add the random duration for risk and no risk duration.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
            execution_line (List[Str]): A optional List parameter of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
        """
        self.total_time = project["time_horizon"]
        self.total_jobs = project["nr_jobs"]
        if execution_line == None:
            self.initial_job = uj.get_initial_job(project["jobs"])
            self.final_job = uj.get_final_job(project["jobs"])
        else:
            self.initial_job = int(execution_line[0].split(".")[0])
            self.final_job = int(execution_line[-1].split(".")[0])
        
        self.set_jobs_duration(project["jobs"], job_params)
        self.build_schedule(execution_line)
        
    def set_jobs_duration(self, jobs, jobs_params):
        """This function stablish the new base duration and total duration for all the jobs excluding the initial and final jobs. Return nothing
        Args:
            jobs (List[Dict]): A list of dictionary of each job.
            job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
        """
        dependencies = {}
        for i in range(self.initial_job, self.final_job + 1):
            dependencies[i] = []
        self.job_list = []
        for job in jobs:
            job_id = job["id"]

            for ji in job["successors"]:
                if job_id not in dependencies[ji]:
                    dependencies[ji].append(job_id)

            if job_id not in [self.initial_job, self.final_job]:
                mean = jobs_params[job_id]["normal_dist_mean"]
                std = jobs_params[job_id]["normal_dist_std"]
                risks = []
                for param in jobs_params[job_id]:
                    if str(param).startswith("risk_") and jobs_params[job_id][param] != None:
                        risks.append(jobs_params[job_id][param])
                new_duration = uj.get_new_job_base_duration(job["base_duration"], mean, std)
                total_duration = np.ceil(new_duration * (1 + np.sum(risks)))
                self.job_list.append({
                    "id": job_id,
                    "mode": job["mode"],
                    "successors": job["successors"],
                    "renewable_resources_use": job["renewable_resources_use"],
                    "nonrenewable_resources_use": job["nonrenewable_resources_use"],
                    "doubly_constrained_use": job["doubly_constrained_use"],
                    "base_duration": job["base_duration"],
                    "init_random_duration": new_duration,
                    "total_duration": total_duration
                })
            else:
                self.job_list.append({
                    "id": job_id,
                    "mode": job["mode"],
                    "successors": job["successors"]
                })

        for i in range(len(self.job_list)):
            self.job_list[i]["dependencies"] = dependencies[self.job_list[i]["id"]]

    def build_schedule(self, execution_line = None):
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
        """This function is in charge to return a List of tuples with elements formmatted as (job_id, job_mode, predecessor_id) to get all the available jobs given the jobs given.
        Args:
            done_jobs (List[Tuple]): A list of tuples with elements (job_id, job_mode, start_tick) to get the successor in all its modes to be available to be executed.
        """
        to_do = []
        done_ids = [i[0] for i in done_jobs]
        for job_id, job_mode , _ in done_jobs:
            job = uj.get_job(self.job_list, job_id, job_mode)
            candidates = job["successors"]
            dependencies = job["dependencies"]
            for can_id in candidates:
                is_feasible = True
                for dep_id in dependencies:
                    is_feasible = is_feasible and (dep_id in done_ids)
                if is_feasible:
                    modes = uj.get_job_modes_duration(self.job_list, can_id).keys()
                    to_do += [(can_id, i) for i in modes]
        return to_do

    def __get_finished_jobs__(self, doing_jobs, actual_time):
        pass

    def __select_best_job__(self, to_do_jobs):
        """This function apply the optimization rules to select the best following job to do and return a List with [job_id, job_mode] to be executed in the project.
        Args:
            to_do_jobs (List[Tuples]): A list of tuples with elements (job_id, job_mode, predecessor_id) of all available jobs to be executed in that time.
        """
        jobs = []
        optimization_rules = (
            lambda job: job["total_duration"],
            lambda job: np.sum(job["nonrenewable_resources_use"]),
            lambda job: np.sum(job["renewable_resources_use"]),
        )
        for job_id, job_mode in to_do_jobs:
            if job_id != self.final_job:
                jobs.append(uj.get_job(self.job_list, job_id, job_mode))

        if len(jobs) > len(optimization_rules):
            divisor = int(np.ceil(len(jobs) / len(optimization_rules)) - 1)
            for rule in optimization_rules:
                jobs = sorted(jobs, key=rule)[:-divisor]
        else:
            for i in range(len(jobs) - 1):
                jobs = sorted(jobs, key=optimization_rules[i])[:-1]

        best_job = jobs[0]
        return best_job["id"], best_job["mode"]
