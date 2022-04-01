"""This file is the principal and only file that must be executed to run the program. This project contain the logic to solve with an Genetic Algorithm the MRCPSP problem. In this file is where you can edit all the hyperparameters to the algorithm to make the execution. Some other parameters as optimization rules can be edited in the schedule.py file.
Created by: Edgar RP
Version: 1.2
"""

import os
import time
import numpy as np
from tqdm import tqdm
import scipy.stats as stats
from gen_alg import Genetic_Algorithm
from utils.data_loader import load_project

random_seed = None
project = load_project("./data/j301_2")
experiment_name = "j301_2"
if not random_seed:
    np.random.seed(project["init_random_value"])
else:
    np.random.seed(random_seed)
random_generator = stats.norm(loc = 0, scale = 1)
n_jobs_with_risks = 10
risks_per_job = (0.5, 0.4, 0.3)
n_scenarios_per_solution = 10
n_scenarios_final = 100
tolerance_x_invalid_schedule = 10
poblation_size = 10
n_winners_x_generation = 4
parents_prob_range = (0.8, 0.2)
n_cross_points = 1
n_mutations = 1
n_generations = 10

if __name__ == "__main__":
    # Create the results folder where the experiments will be saved
    results_folder = "./results"
    if not os.path.isdir(results_folder):
        os.mkdir(results_folder)
    experiment_path = os.path.join(results_folder, experiment_name)
    if not os.path.isdir(experiment_path):
        os.mkdir(experiment_path)

    start = time.time()
    gen_alg = Genetic_Algorithm(
            project,
            random_generator,
            poblation_size,
            n_winners_x_generation,
            n_jobs_with_risks,
            risks_per_job,
            n_scenarios_per_solution,
            tolerance_x_invalid_schedule,
        )
    end = time.time()
    print("The time creating the first poblation use a total of {} seconds".format(end-start))
    
    progress_bar = tqdm(range(1, n_generations), desc = "Poblation makespan: {} +- {}".format(gen_alg.mean_makespan, gen_alg.std_makespan))
    for gi in progress_bar:
        gen_alg.evolve_poblation(parents_prob_range, n_cross_points, n_mutations, random_generator)
        progress_bar.set_description("Poblation makespan: {} +- {}".format(gen_alg.mean_makespan, gen_alg.std_makespan))

    best_solution = gen_alg.solutions[0] # Aqui cual consideramos la mejor solucion?
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