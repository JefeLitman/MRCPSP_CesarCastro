"""This file is for run the Genetic Algorithm for MRCPSP problem. In this file is where you can edit all the hyperparameters to the algorithm to make the execution. Some other parameters as optimization rules can be edited in the schedule.py file.
Created by: Edgar RP
Version: 1.0
"""

import numpy as np
from tqdm import tqdm
import scipy.stats as stats
from utils import savers as us
from gen_alg import Genetic_Algorithm
from utils.data_loader import load_project

random_seed = None
results_folder = "./results"
experiment_name = "gen_alg_test_2_j301_2"
project = load_project("./data/j301_2")
if not random_seed:
    np.random.seed(project["init_random_value"])
else:
    np.random.seed(random_seed)
random_generator = stats.uniform(loc = 0, scale = 1)
n_jobs_with_risks = 10
risks_per_job = [(0.05, 0.5, 0.1), (0.02, 0.6, 0.15), (0.08, 0.3, 0.09)] # (Prob of risk, Percentage of duration for the mean, Percentage of duration for the deviation)
n_scenarios_per_solution = 10
poblation_size = 10
n_winners_x_generation = 4
parents_prob_range = (0.8, 0.2)
n_cross_points = 1
n_mutations = 1
n_generations = 10

if __name__ == "__main__":
    exp_path = us.create_experiment_folder(results_folder, experiment_name)
    us.save_project_params(exp_path, project)
    
    progress_bar = tqdm(range(n_generations))
    for gi in progress_bar:
        if gi == 0:
            gen_alg = Genetic_Algorithm(
                project,
                random_generator,
                poblation_size,
                n_winners_x_generation,
                n_jobs_with_risks,
                risks_per_job,
                n_scenarios_per_solution
            )
            us.save_job_params(exp_path, gen_alg.jobs, len(risks_per_job))
        else:
            gen_alg.evolve_poblation(parents_prob_range, n_cross_points, n_mutations, random_generator)
        progress_bar.set_description("Poblation mean makespan: {} +- {}".format(gen_alg.mean_makespan, gen_alg.std_makespan))
        us.save_generation(exp_path, gi + 1, gen_alg.solutions)

    # Select the best individual by the lower makespan and pass it again in the sequentiator
    best_solution = sorted(gen_alg.solutions, key = lambda sol: sol.makespan)[0]
    best_solution.base_line.build_schedule(
        best_solution.base_line.execution_line, 
        best_solution.base_line.job_durations
    )
    best_solution.make_scenarios(project, best_solution.job_params)
    best_solution.set_metrics()
    us.save_solution(exp_path, "Best solution", best_solution)