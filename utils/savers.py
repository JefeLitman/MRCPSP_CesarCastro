"""This file contains code to export the Genetic Algorithm elements in JSON files containing important information of the experiment done for MRCPSP Problem.
Created by: Edgar RP
Version: 0.2
"""
import os
import json
import pandas as pd

def __check_folder_path__(path):
    """This function is to check is the path given exist as folder or otherwise will raise an exception due to the inexsistent path.
    Args:
        path (Str): String with the path to be checked if its exist. It must be a folder.
    """
    if not os.path.isdir(path):
        raise ValueError('Did you give a valid and created save path? Path given: {}'.format(path))

def create_experiment_folder(base_path, experiment_name):
    """This function create the experiment folder in the base path and return the experiment folder path. In the case the experiment name exist, it will return an error.
    Args:
        base_path (Str): String of the absolute or relative path of experiments
        experiment_name (Str): String with the name of the folder that will contain the experiment.
    """
    if not os.path.isdir(base_path):
        os.mkdir(base_path)

    experiment_path = os.path.join(base_path, experiment_name)
    if not os.path.isdir(experiment_path):
        os.mkdir(experiment_path)
    else:
        raise AssertionError("The experiment name already exist, delete this folder or uses another name to save the results of this experiment.")
    
    return experiment_path
 
def save_project_params(save_path, project):
    """This function saves a json with the project params without including the jobs of the project to know the main attributes of it. It doesn't return nothing.
    Args:
        save_path (Str): String with the folder path of where will be saved the project params.
        project (Dict): Dictionary containing all the parameters for the project.
    """
    __check_folder_path__(save_path)

    json_dict = {}
    for key in project:
        if key != "jobs":
            json_dict[key] = project[key]
    
    with open(os.path.join(save_path, "project_params.json"), "w") as file_2_save:
        json.dump(json_dict, file_2_save, indent=2)

def save_job_params(save_path, job_params, num_risks):
    """This function saves an excel file with the job params suchs as risk, means and standard deviations. It doesn't return nothing.
    Args:
        save_path (Str): String with the folder path of where will be saved the job params.
        job_params (Dict): A dictionary with keys as jobs_ids and values contain the risk and distribution parameters (mean and std) for that job.
        num_risks (Int): An integer indicating how many risk every job will have.
    """
    __check_folder_path__(save_path)

    data_table = []
    for job_str in job_params:
        job_id, job_mode = [int(i) for i in job_str.split(".")]
        data_table.append([
            job_id,
            job_mode,
            job_params[job_str]["base_duration"],
            job_params[job_str]["normal_dist_mean"],
            job_params[job_str]["normal_dist_std"]
        ] + [
            job_params[job_str]["risk_{}".format(i)] for i in range(1, num_risks + 1)
        ])
    
    columns_names = ["Activity", "Mode", "Base Duration", "Mean", "Std"] + [
        "Risk {}".format(i) for i in range(1, num_risks + 1)
    ]

    pd.DataFrame(data_table, columns=columns_names).to_excel(os.path.join(save_path, "job_params.xlsx"), index=False)