"""This file contains code to process the jobs dictionary in the project
and schedule objects.
Created by: Edgar RP
Version: 1.0
Job Dict Structure:
    {
        "id": Integer
        "mode": Integer
        "duration": Integer
        "successors": List[Int]
        "renewable_resources_use": np.Array[Int]
        "nonrenewable_resources_use": np.Array[Int]
        "doubly_constrained_use": np.Array[Int]
    }
"""

import numpy as np

def __check_zero_params__(job):
    """This function check the duration, use of renewable, non renewable and doubly
    constraint resources to be zero, returns True if that's the case and False 
    otherwise.
    Args:
        job (Dict): A dictionary of a job with the structure showed in jobs.py.
    """
    zero_value = 0
    zero_params = [
        "duration", 
        "renewable_resources_use", 
        "nonrenewable_resources_use", 
        "doubly_constrained_use"
    ]
    for key in zero_params:
        zero_value += np.sum(job[key])

    return zero_value == 0

def get_initial_job(jobs):
    """This function find the initial job in the list of job's 
    dictionary and return its id.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
    """
    for job in jobs:
        if __check_zero_params__(job) and len(job["successors"]) != 0:
            return job["id"]
        
def get_final_job(jobs):
    """This function find the initial job in the list of job's 
    dictionary and return its id.
    Args:
        jobs (List[Dict]): A list of dictionary of each job."""
    for job in jobs:
        if __check_zero_params__(job) and len(job["successors"]) == 0:
            return job["id"]

def get_new_job_base_duration(duration, beta_generator):
    """This function return a new randomly duration for the duration given 
    using the beta_generator. If the duration is 1 it will add always more 
    time.
    Args:
        duration (Integer): A value specifying the duration to change.
        beta_generator (np.random.beta): Instance of numpy beta random value 
        generator to get random values.
    """
    new_duration = duration
    if beta_generator() >= 0.5:
        #Duration modified
        if beta_generator() > 0.5 or duration == 1:
            #Duration increased
            new_duration *= 1 + beta_generator()
        else:
            #Duration decreased
            new_duration *= beta_generator()
    if duration == 1 and new_duration < 1.:
        return 1 + np.ceil(new_duration)
    else:
        return np.ceil(new_duration)