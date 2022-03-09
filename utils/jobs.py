"""This file contains code to process the jobs dictionary in the project and schedule objects.
Created by: Edgar RP
Version: 1.3
Job Dict Structure:
    {
        "id": Integer
        "mode": Integer
        "base_duration": Integer
        "successors": List[Int]
        "renewable_resources_use": np.Array[Int]
        "nonrenewable_resources_use": np.Array[Int]
        "doubly_constrained_use": np.Array[Int],
        "init_random_duration": Integer,
        "normal_dist_mean": Float,
        "normal_dist_std": Float,
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

def __get_job_distribution__(duration, random_generator):
    """This function generate the mean, std and the function callback to generate random probabilities from this distribution.
    Args:
        duration (Integer): A value specifying the duration to change.
        random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
    Returns:
        mean (Float): The mean of the normal distribution.
        std (Float): The std of the normal distribution.
        probability (Callback): A python callback that return a value between 0 and 1 for probability.
    """
    mean = random_generator.rvs() * duration
    std = random_generator.rvs() * duration
    return mean, std, __get_dist_prob__(mean, std)

def get_job_modes(jobs, job_id):
    """This function return all the modes for the given job id and return a list with the modes.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
        job_id (Integer): A number of which job will return its modes.
    """
    modes = []
    for job in jobs:
        if job["id"] == job_id:
            modes.append(job["mode"])
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

def get_new_job_base_duration(duration, random_generator):
    """This function return a new randomly duration for the duration given using the random_generator and return the mean and std for the normal distribution of random in this job. If the duration is 1 it will add always more time.
    Args:
        duration (Integer): A value specifying the duration to change.
        random_generator (scipy.stats.norm): Instance of scipy.stats.norm object to generate random values of the normal distribution.
    Returns:
        new_duration (Integer): The new duration for the job.
        mean (Float): The random value for the mean of the normal distribution for this job.
        std (Float): The random value for the std of the normal distribution for this job.
    """
    mean, std, probability = __get_job_distribution__(duration, random_generator)
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

def get_job_risks(base_duration, risks_per_job, mean, std):
    """This function will return a dictionary with the risk percentages and the new duration of the task with the risk applied. The dict will have the following structure:
    {
        "risk_1": Float,
        "risk_2": Float,
        ...
        "total_duration": Integer
    }
    Args:
        base_duration (Integer): A value specifying the duration to apply risks.
        risks_per_job (Tuple): Tuple of the percentages of happening that risk and its length is the quantity of risks.
        mean (Float): The mean of the normal distribution to use for the probabilities callback.
        std (Float): The std of the normal distribution to use for the probabilities callback.
    """
    new_duration = base_duration
    risks = {}
    prob = __get_dist_prob__(mean, std)
    percentages = []
    for i, p in enumerate(risks_per_job):
        risk = "risk_{}".format(i+1)
        if prob() < p:
            percentage = prob()
            risks[risk] = percentage
            percentages.append(percentage)
        else:
            risks[risk] = None
    new_duration *= 1 + np.sum(percentages)
    risks["total_duration"] = np.ceil(new_duration)
    return risks