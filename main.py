"""This file is the principal and only file that must be executed to run the program. This project contain the logic to solve with an Genetic Algorithm the MRCPSP problem. In this file is where you can edit all the hyperparameters to the algorithm to make the execution. Some other parameters as optimization rules can be edited in the schedule.py file.
Created by: Edgar RP
Version: 0.2
"""

import numpy as np
import scipy.stats as stats
from .gen_alg import Genetic_Algorithm
from .utils.data_loader import load_project

random_seed = None
project = load_project("./data/j3010_1/")
if not random_seed:
    np.random.seed(project["init_random_value"])
else:
    np.random.seed(random_seed)
random_generator = stats.norm(loc = 0, scale = 1)
n_jobs_with_risks = 10
risks_per_job = 3
n_scenarios_per_solution = 10
n_scenarios_final = 1000 
tolerance_x_invalid_schedule = 10
poblation_size = 20
n_winners_x_generation = 4
parents_prob_range = (0.8, 0.2)
n_cross_points = 1
n_mutations = 1


if __name__ == "main":
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