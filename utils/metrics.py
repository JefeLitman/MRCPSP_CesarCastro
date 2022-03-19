"""This file contains code to calculate the metrics for solutions in the MRCPSP problem.
Created by: Edgar RP
Version: 1.0
"""

import numpy as np

def get_solution_robustness(base_line, scenarios):
    """This function return the solution robustenss value (SR) given the base line and simulated scenarios from that solution, each sceneario must have the same execution_line but different time lines.
    Args:
        base_line (Schedule): Instance of the class schedule that contains and execution_line and a time_line.
        scenarios (List[Schedule]): A list of instances of the class schedule that must contain the exact same execution_line but different time_line of the base_line.
    """
    for sc in scenarios:
        if sc.execution_line != base_line.execution_line:
            raise AssertionError("A scenario from the base line given is different in the execution line, this means that a scenario is for another solution than the given.")

    SR_jobs = np.zeros_like(base_line.time_line)
    base_times = np.r_[base_line.time_line]
    for sc in scenarios:
        SR_jobs = SR_jobs + np.abs(base_times -  sc.time_line)

    return np.sum(SR_jobs / len(scenarios))