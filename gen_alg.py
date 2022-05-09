"""This file contain the class that execute and do the genetic algorithm of the given project with mutation, crossover and other methods neccessary.
Created by: Edgar RP
Version: 1.3.4
"""

import numpy as np
import utils.jobs as uj
from copy import copy
from solution import Solution

class Genetic_Algorithm():
    
    def __init__(self, project, random_generator, poblation_size, n_winners, n_jobs_risks, risks_per_job, n_scenarios_sol, tol_invalid_sch):
        """This class is the main class, it creates the quantity of solutons given, make crossover, mutation and select the best samples. This class contain important classes as to create a new generation and stablish the risks in the jobs.
        Args:
            project (Dict): Dictionary containing all the parameters for the project.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
            poblation_size (Int): Quantity of solutions to have for generation.
            n_winners (Int): Quantity of solutions that will be taken into account as parents to generate the new sons. It can not be greater than poblation_size.
            n_jobs_risks (Int): Quantity of jobs which will have risks.
            risks_per_job (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
            n_scenearios_job (Int): Number of scenarios per solution, an integer indicating how many scenarios must be created using the base line to obtain the mean makespan.
            tol_invalid_sch (Int): Tolerance of invalid schedules created, an integer indicating how many retries it can until to get a valid schedule solution.
        """
        if poblation_size <= n_winners:
            raise AssertionError("The size of the poblation must be greater than the quantity of winners for generation. Values given {} <= {}".format(
                poblation_size,
                n_winners
            ))
        self.n_total_sol = poblation_size
        self.n_winners = n_winners

        self.project = project
        self.initial_job = uj.get_initial_job(project["jobs"])
        self.final_job = uj.get_final_job(project["jobs"])
        self.__set_jobs_params__(project["jobs"], n_jobs_risks, risks_per_job, random_generator)
        
        # self.solutions = []
        # for _ in range(poblation_size):
        #     self.solutions.append(
        #         Solution(project, self.jobs, n_scenarios_sol, tol_invalid_sch)
        #     )
        # self.__sort_poblation__()

    def __sort_poblation__(self):
        """This function set the metrics first in the poblation like mean and std makespan, order from lower to higher the difference in the makespan and the mean makespan and finally compute the metrics for every solution in the poblation. It doesn't return nothing."""
        makespans = [i.mean_makespan for i in self.solutions]
        self.mean_makespan = np.mean(makespans)
        self.std_makespan = np.std(makespans)
        self.solutions = sorted(self.solutions, key = lambda s: np.abs(s.mean_makespan - self.mean_makespan))

    def __min_max_scaler__(self, X, new_min, new_max):
        """This function transform the values of X to the new range given by new_min and new_max and return the transformed values. This function is the same as scalate the values without altering its distribution.
        Args:
            X (List or np.Array): A list or numpy array with the values to be changed in the new range.
            new_min (Float): The new min value that the data X will have after the transformation.
            new_max (Float): The new max value that the data X will have after the transformation.
        """
        X_std = (X - np.min(X)) / (np.max(X) - np.min(X))
        X_scaled = X_std * (new_max - new_min) + new_min
        return X_scaled

    def __set_jobs_params__(self, jobs, n_jobs, risks_per, random_generator):
        """This function set the params, predecessor and risks for every job in the solution given the n_jobs with risks and risk_per job.
        Args:
            jobs (List[Dict]): A list of dictionary of each job.
            n_jobs (Integer): Quantity of jobs which will have risks.
            risks_per (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
        """
        dependencies = {}
        for i in range(self.initial_job, self.final_job + 1):
            dependencies[i] = []

        self.jobs = {}
        for job in jobs:
            job_id = job["id"]
            job_mode = job["mode"]
            job_key = "{}.{}".format(job_id, job_mode)

            if job_id == self.initial_job:
                self.jobs[job_key] = {"initial": True}
            elif job_id == self.final_job:
                self.jobs[job_key] = {"final": True}
            else:
                self.jobs[job_key] = {
                    "base_duration": job["base_duration"],
                    "normal_dist_mean": job["base_duration"],
                    "normal_dist_std": job["base_duration"] * 0.3,
                    "renewable_resources_use": job["renewable_resources_use"],
                    "nonrenewable_resources_use": job["nonrenewable_resources_use"],
                    "doubly_constrained_use": job["doubly_constrained_use"]
                }

            for ji in job["successors"]:
                if job_id not in dependencies[ji]:
                    dependencies[ji].append(job_id)
        
        for job in jobs:
            job_id = job["id"]
            job_mode = job["mode"]
            job_key = "{}.{}".format(job_id, job_mode)
            self.jobs[job_key]["predecessors"] = dependencies[job_id]
            self.jobs[job_key]["successors"] = job["successors"]

        jobs_modified = []
        prob = lambda: random_generator.cdf(random_generator.rvs())
        while len(jobs_modified) < n_jobs:
            index = int(prob()*len(self.jobs))
            job_str = list(self.jobs.keys())[index]
            job_id = int(job_str.split(".")[0])
            if job_id not in [self.initial_job, self.final_job] + jobs_modified:
                risks = uj.get_job_risks(risks_per, self.jobs[job_str]["base_duration"], random_generator)
                is_none = True
                for r in risks:
                    is_none = is_none and risks[r] == None
                    for job_mode in uj.get_job_modes_duration(jobs, job_id):
                        job_key = "{}.{}".format(job_id, job_mode)
                        if is_none:
                            self.jobs[job_key][r] = None 
                        else:
                            if job_key == job_str:
                                self.jobs[job_key][r] = risks[r]
                            else:
                                self.jobs[job_key][r] = uj.get_job_risk_dist(
                                    self.jobs[job_key]["base_duration"]
                                ).rvs()

                if not is_none:
                    jobs_modified.append(job_id)

        # Let the remaining jobs with risks as None value
        for job_str in self.jobs:
            job_id = int(job_str.split(".")[0])
            if job_id not in [self.initial_job, self.final_job] + jobs_modified:
                risks = uj.get_job_risks(np.zeros_like(risks_per), 0)
                for r in risks:
                    #self.jobs[job_str]["used_for_risks"] = False
                    self.jobs[job_str][r] = risks[r]

    def evolve_poblation(self, prob_ranges, n_cross_points, n_mutations, random_generator):
        """This function updates or make advance the initial poblation to the following generation, this method execute the crossover, mutation and sort solutions from best to worst to select who solutions will stay and which will be deleted.
        Args:
            prob_ranges (Tuple[Float]): A tuple with two elements, the first one is the lowest probability for the last parent and the last element is the higher probability for the first parent sorted from best to worst.
            n_cross_points (Int): An integer indicating how many points will be taking to crossover two parents randomly selected.
            n_mutations (Int): An integer indicating how many mutation tries must be executed by every job per solution. The mutations will be only to change the mode of the job.
        """
        for i in prob_ranges:
            if i <= 0 or i >=1:
                raise AssertionError("The range of probabilities must be between 0 and 1 (not included) to let all the winners participate in the tournament to be selected as father. Prob range given: {}".format(prob_ranges))
        # The poblation is already ordered and will be ordered at the last moment
        winners = self.solutions[:self.n_winners]
        prob = lambda: random_generator.cdf(random_generator.rvs())
        probabilities = self.__min_max_scaler__(
            [np.abs(s.mean_makespan - self.mean_makespan) for s in winners], 
            min(prob_ranges), 
            max(prob_ranges)
        )
        for index in range(self.n_winners, self.n_total_sol):
            # Select which parents will be used to make the crossover
            parents = []
            while len(parents) < 2:
                random_value = prob()
                for i in range(len(winners)-1,  -1, -1):
                    if random_value >= probabilities[i]:                        
                        parents.append(winners[i])
                        break
            exec_line_son = self.crossover_solutions(
                parents[0].base_line.execution_line, 
                parents[1].base_line.execution_line, 
                n_cross_points, 
                random_generator
            )

            exec_line_son = self.mutate_solution(exec_line_son, n_mutations, random_generator)

            self.solutions[index].set_baseline(self.project, self.jobs, exec_line_son)

        # After all children were created, then re sort the poblation
        self.__sort_poblation__()

    def crossover_solutions(self, exec_line_0, exec_line_1, n_points, random_generator):
        """This function is in order to create a new execution line based on the two execution lines given. It return the new execution line.
        Args:
            exec_line_0 (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
            exec_line_1 (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
            n_points (Int): An integer indicating how many points will be taking to make the crossover operation.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
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
        return exec_line

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

    def mutate_solution(self, exec_line, mutations, random_generator):
        """This function alters each job in the execution line (ignoring the first and last) changing its modes by a random probabilitie in each job. It return the new mutated execution line.
        Args:
            exec_line (List[Str]): A List of strings in the format "<job_id>.<job_mode>" that contain the order in which every job will be executed.
            mutations (Int): An integer indicating how many mutation tries must be executed by every job per solution. The mutations will be only to change the mode of the job.
            random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
        """
        mutated_exec_line = copy(exec_line)
        prob = lambda: random_generator.cdf(random_generator.rvs())
        for i, job_string in enumerate(exec_line):
            job_id, _ = [int(i) for i in job_string.split('.')]
            if job_id not in [self.initial_job, self.final_job]:
                mutation_ratio = prob()
                modes = list(uj.get_job_modes_duration(self.project["jobs"], job_id).keys())
                for _ in range(mutations):
                    if prob() < mutation_ratio:
                        index = int(prob()*len(modes))
                        mutated_exec_line[i] = "{}.{}".format(job_id, modes[index])
        return mutated_exec_line
