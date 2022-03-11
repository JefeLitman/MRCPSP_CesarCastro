"""This file contains code to process the jobs dictionary in the project and schedule objects.
Created by: Edgar RP
Version: 1.4
Job Dict Structure:
    {
        "id": Integer
        "mode": Integer
        "base_duration": Integer
        "successors": List[Int]
        "renewable_resources_use": np.Array[Int]
        "nonrenewable_resources_use": np.Array[Int]
        "doubly_constrained_use": np.Array[Int],
        "normal_dist_mean": Float,
        "normal_dist_std": Float,
        "init_random_duration": Integer,
        "total_duration": Integer,
        "risk_1": Float,
        "risk_2": Float,
        ...
        "risk_n": Float
    }
"""

import numpy as np
import scipy.stats as stats

def __check_zero_params__(job):
    """This function check the duration, use of renewable, non renewable and doubly constraint resources to be zero, returns True if that's the case and False otherwise.
    Args:
        job (Dict): A dictionary of a job with the structure showed in jobs.py.
    """
    zero_value = 0
    zero_params = [
        "base_duration", 
        "renewable_resources_use", 
        "nonrenewable_resources_use", 
        "doubly_constrained_use"
    ]
    for key in zero_params:
        zero_value += np.sum(job[key])

    return zero_value == 0 and job["mode"] == 1

def __get_dist_prob__(mean, std):
    """This function return the function callback to generate random probabilities from the normal distribution with mean and std given.
    Args:
        mean (Float): The mean of the normal distribution to use for the probabilities callback.
        std (Float): The std of the normal distribution to use for the probabilities callback.
    """
    dist = stats.norm(loc=mean, scale=std)
    return lambda: dist.cdf(dist.rvs())

def get_job_modes_duration(jobs, job_id):
    """This function return all the duration for all modes of given job id and return a dictionary with keys as modes and values its durations.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
        job_id (Integer): A number of which job will return its modes.
    """
    modes = {}
    for job in jobs:
        if job["id"] == job_id:
            modes[job["mode"]] = job["base_duration"]
    if len(modes) == 0:
        raise AssertionError("The job with id ({}) doesn't exist \
            in the loaded project.".format(job_id))
    else:        
        return modes

def get_job(jobs, job_id, mode):
    """This function return the dict structure of the given job_id and mode.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
        job_id (Integer): A number of which job will return its modes.
    """
    for job in jobs:
        if job["id"] == job_id and job["mode"] == mode:
            return job
    raise AssertionError("The job with id ({}) and mode ({}) doesn't exist \
        in the loaded project.".format(job_id, mode))

def get_initial_job(jobs):
    """This function find the initial job in the list of job's dictionary and return its id.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
    """
    for job in jobs:
        if __check_zero_params__(job) and len(job["successors"]) != 0:
            return job["id"]
    raise ValueError("The project have an initial job?")
        
def get_final_job(jobs):
    """This function find the initial job in the list of job's dictionary and return its id.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
    """
    for job in jobs:
        if __check_zero_params__(job) and len(job["successors"]) == 0:
            return job["id"]
    raise ValueError("The project have a final job?")

def get_job_dist_params(duration, random_generator):
    """This function return the mean and std randomly selected from the duration given using the random_generator passed. These params are required to obtain a new base duration or the job risks.
    Args:
        duration (Integer): A value specifying the duration to change.
        random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
    """ 
    mean = random_generator.rvs() * duration
    std = abs(random_generator.rvs() * duration)
    return mean, std

def get_new_job_base_duration(duration, mean, std):
    """This function return a new randomly duration for the duration given using the mean and std. If the duration is 1 it will add always more time.
    Args:
        duration (Integer): A value specifying the duration to change.
        mean (Float): The mean of the normal distribution to use for the probabilities callback.
        std (Float): The std of the normal distribution to use for the probabilities callback.
    """ 
    probability = __get_dist_prob__(mean, std)
    new_duration = duration
    if probability() >= 0.5: # Duration modified
        if probability() > 0.5:
            new_duration *= 1 + probability() # Duration increased
        else:
            new_duration *= probability() # Duration decreased
    if duration == 1 and new_duration < 1.:
        return 1 + np.ceil(new_duration)
    else:
        return np.ceil(new_duration), mean, std

def get_job_risks(risks_per_job, mean, std):
    """This function will return a dictionary with the risk percentages and the new duration of the task with the risk applied. The dict will have the following structure:
    {
        "risk_1": Float,
        "risk_2": Float,
        ...
    }
    Args:
        base_duration (Integer): A value specifying the duration to apply risks.
        risks_per_job (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
        mean (Float): The mean of the normal distribution to use for the probabilities callback.
        std (Float): The std of the normal distribution to use for the probabilities callback.
    """
    risks = {}
    prob = __get_dist_prob__(mean, std)
    for i, p in enumerate(risks_per_job):
        risk = "risk_{}".format(i+1)
        if prob() < p:
            risks[risk] = prob()
        else:
            risks[risk] = None
    return risks