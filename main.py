"""This file is the principal and only file that must be executed to run the program. This project contain the logic to solve with an Genetic Algorithm the MRCPSP problem. In this file is where you can edit all the hyperparameters to the algorithm to make the execution. Some other parameters as optimization rules can be edited in the schedule.py file.
Created by: Edgar RP
Version: 1.2.4
"""

import time
import numpy as np
from tqdm import tqdm
import scipy.stats as stats
from utils import savers as us
from gen_alg import Genetic_Algorithm
from utils.data_loader import load_project

random_seed = None
results_folder = "./results"
experiment_name = "test"
project = load_project("./data/j301_2")
if not random_seed:
    np.random.seed(project["init_random_value"])
else:
    np.random.seed(random_seed)
random_generator = stats.uniform(loc = 0, scale = 1)
n_jobs_with_risks = 10
risks_per_job = (0.05, 0.02, 0.08)
n_scenarios_per_solution = 10
n_scenarios_final = 100
poblation_size = 10
n_winners_x_generation = 4
parents_prob_range = (0.8, 0.2)
n_cross_points = 1
n_mutations = 1
n_generations = 10

if __name__ == "__main__":
    exp_path = us.create_experiment_folder(results_folder, experiment_name)
    
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
        else:
            gen_alg.evolve_poblation(parents_prob_range, n_cross_points, n_mutations, random_generator)
        progress_bar.set_description("Poblation makespan: {} +- {}".format(gen_alg.mean_makespan, gen_alg.std_makespan))

    best_solution = gen_alg.solutions[0] 
    start = time.time()
    best_solution.make_scenarios(project, gen_alg.jobs, n_scenarios_final)
    end = time.time()
    print("The time creating the final scenarios use a total of {} seconds".format(end-start))
    print("""The metrics for the best solution after all iterations was of:
    Makespan: {m}
    Mean makespan: {mm}
    Std makespan: {sm}
    Solution Robustness: {sr}
    Quality Robustness: {qr}
    Execution Line: {el}
    Time Line: {tl}""".format(
        m = best_solution.makespan,
        mm = best_solution.mean_makespan,
        sm = best_solution.std_makespan,
        sr = best_solution.robustness,
        qr = best_solution.quality,
        el = best_solution.base_line.execution_line,
        tl = best_solution.base_line.time_line
    ))