"""This file contain the class that structure a scenario for the solution and also can create a base line for the solution.
Created by: Edgar RP
Version: 0.0.1
"""

import numpy as np
import utils.jobs as uj

class Scenario():
    
    def __init__(self, random_generator, jobs, renew_res, norenew_res, dou_res):
        """When you create a Scenario for a Solution, it generate a list of activities to solve in time, calculate it own makespan and alter the base_duration for jobs. 
        Args:
            
        """
        
        