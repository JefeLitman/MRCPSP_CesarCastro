"""This file is for run the Final Simulations for a MRCPSP solution of the problem. In this file is where you can edit all the hyperparameters to the algorithm to make the execution. Some other parameters as optimization rules can be edited in the schedule.py file.
Created by: Edgar RP
Version: 1.0
"""

import time
import numpy as np
import scipy.stats as stats
from utils import savers as us
from gen_alg import Genetic_Algorithm
from utils.data_loader import load_project

random_seed = None
results_folder = "./results"
experiment_name = "final_simulations_test_ag_2_j301_2"
project = load_project("./data/j301_2")
if not random_seed:
    np.random.seed(project["init_random_value"])
else:
    np.random.seed(random_seed)
random_generator = stats.uniform(loc = 0, scale = 1)
n_jobs_with_risks = 10
risks_per_job = [(0.05, 0.5, 0.1), (0.02, 0.6, 0.15), (0.08, 0.3, 0.09)] # (Prob of risk, Percentage of duration for the mean, Percentage of duration for the deviation)
n_scenarios_final = 5000
execution_line = ["1.1","2.3","4.3","19.3","3.1","7.1","11.1","9.1","17.2","15.2","5.3","12.1","21.1","6.1","23.3","8.1","10.3","16.3","20.2","25.3","13.2","18.2","14.1","24.3","28.2","22.1","26.1","29.3","27.3","30.2","31.1","32.1"]
time_line = [0,0,0,5,12,16,17,19,23,23,16,32,31,33,32,39,39,43,39,41,43,52,47,52,52,50,62,61,62,74,74,78]

if __name__ == "__main__":
    exp_path = us.create_experiment_folder(results_folder, experiment_name)
    us.save_project_params(exp_path, project)
    gen_alg = Genetic_Algorithm(project, random_generator, 2, 1, n_jobs_with_risks, risks_per_job, 1)
    us.save_job_params(exp_path, gen_alg.jobs, len(risks_per_job))
    
    solution = gen_alg.solutions[0]
    solution.base_line.execution_line = execution_line
    solution.base_line.time_line = time_line

    start = time.time()
    solution.make_scenarios(project, solution.job_params, n_scenarios_final)
    end = time.time()
    solution.set_metrics()
    us.save_solution(exp_path, "Solution", solution)

    print("The time creating the final scenarios use a total of {} seconds".format(end-start))
    print("""The metrics for the solution after {sim} simulations was of:
    Makespan: {m}
    Mean makespan: {mm}
    Std makespan: {sm}
    Solution Robustness: {sr}
    Quality Robustness: {qr}
    """.format(
        sim = n_scenarios_final,
        m = solution.makespan,
        mm = solution.mean_makespan,
        sm = solution.std_makespan,
        sr = solution.solution,
        qr = solution.quality
    ))