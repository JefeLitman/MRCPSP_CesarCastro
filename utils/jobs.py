"""This file contains code to process the jobs dictionary in the project and schedule objects.
Created by: Edgar RP
Version: 1.8
Job Dict Structure:
    {
        "id": Integer
        "mode": Integer
        "base_duration": Integer
        "successors": List[Int]
        "renewable_resources_use": List[Int]
        "nonrenewable_resources_use": List[Int]
        "doubly_constrained_use": List[Int],
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

def get_total_job_duration(job):
    """This function return the new total duration when it adds the new base duration and sum every risk of the given job dict. It will return the duration approximated to the nearest integer.
    Args:
        job (Dict): A dictionary of a job with the structure showed in jobs.py.
    """ 
    duration = job["base_duration"]
    new_base_duration = stats.norm.rvs(loc=duration, scale=duration * 0.3)
    risks = 0
    for key in job:
        if key.startswith("risk_"):
            if job[key] != None:
                risks += job[key]
    return int(np.rint(new_base_duration + risks))

def get_job_risk_dist(base_duration, mean_percentage, std_percentage):
    """This funtion will return the distribution instance of the risk for the job given the base duration.
    Args:
        base_duration (Integer): A value specifying the duration to calculate the distribution risk.
        mean_percentage (Float): The percentange value between 0 and 1 that tells how much percentage of the base duration will be used as mean for the normal distribution.
        std_percentage (Float): The percentange value between 0 and 1 that tells how much percentage of the base duration will be used as standard deviation for the normal distribution.
    """
    return stats.norm(loc=base_duration*mean_percentage, scale=base_duration*std_percentage)

def get_job_risks(risks_per_job, base_duration, random_generator):
    """This function will return a dictionary with the risk percentages and the new duration of the task with the risk applied. The dict will have the following structure:
    {
        "risk_1": Float,
        "risk_2": Float,
        ...
    }
    Args:
        risks_per_job (List[Tuple]): A list with Tuples with elements: (Probability of ocurring the risk, Percentage of the duration to use as mean of distribution, Percentage of the duration to use as standard deviation of distribution) and its length is the quantity of risks.
        base_duration (Integer): A value specifying the duration to apply risks.
        random_generator (scipy.stats.<distribution>): Instance of scipy.stats.<distribution> object to generate random values of the normal distribution.
    """
    risks = {}
    prob = lambda: random_generator.cdf(random_generator.rvs())
    for i, p in enumerate(risks_per_job):
        dist = get_job_risk_dist(base_duration, p[1], p[2])
        risk = "risk_{}".format(i+1)
        if prob() < p[0]:
            risks[risk] = dist.rvs()
        else:
            risks[risk] = None
    return risks