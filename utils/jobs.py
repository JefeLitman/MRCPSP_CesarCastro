"""This file contains code to process the jobs dictionary in the project
and schedule objects.
Created by: Edgar RP
Version: 1.2
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
        "total_duration": Integer,
        "risk_1": Float,
        "risk_2": Float,
        ...
        "risk_n": Float
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
        "base_duration", 
        "renewable_resources_use", 
        "nonrenewable_resources_use", 
        "doubly_constrained_use"
    ]
    for key in zero_params:
        zero_value += np.sum(job[key])

    return zero_value == 0 and job["mode"] == 1

def get_job_modes(jobs, job_id):
    """This function return all the modes for the given job id
    and return a list with the modes.
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
    """This function return the dict structure of the given 
    job_id and mode.
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
    """This function find the initial job in the list of job's 
    dictionary and return its id.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
    """
    for job in jobs:
        if __check_zero_params__(job) and len(job["successors"]) != 0:
            return job["id"]
    raise ValueError("The project have an initial job?")
        
def get_final_job(jobs):
    """This function find the initial job in the list of job's 
    dictionary and return its id.
    Args:
        jobs (List[Dict]): A list of dictionary of each job.
    """
    for job in jobs:
        if __check_zero_params__(job) and len(job["successors"]) == 0:
            return job["id"]
    raise ValueError("The project have a final job?")

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
        if beta_generator() > 0.5:
            #Duration increased
            new_duration *= 1 + beta_generator()
        else:
            #Duration decreased
            new_duration *= beta_generator()
    if duration == 1 and new_duration < 1.:
        return 1 + np.ceil(new_duration)
    else:
        return np.ceil(new_duration)

def get_job_risks(base_duration, risks_per_job, beta_generator):
    """This function will return a dictionary with the risk percentages 
    and the new duration of the task with the risk applied. The dict will
    have the following structure:
    {
        "risk_1": Float,
        "risk_2": Float,
        ...
        "total_duration": Integer
    }
    Args:
        base_duration (Integer): A value specifying the duration to apply risks.
        risks_per_job (Tuple): Tuple of the percentages of happening that risk and
        its length is the quantity of risks.
        beta_generator (np.random.beta): Instance of numpy beta random value 
        generator to get random values.
    """
    new_duration = base_duration
    risks = {}
    percentages = []
    for i, p in enumerate(risks_per_job):
        risk = "risk_{}".format(i+1)
        if beta_generator() < p:
            percentage = beta_generator()
            risks[risk] = percentage
            percentages.append(percentage)
        else:
            risks[risk] = None
    new_duration *= 1 + np.sum(percentages)
    risks["total_duration"] = np.ceil(new_duration)
    return risks