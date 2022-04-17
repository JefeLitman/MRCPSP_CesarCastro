"""This file contains code to export the Genetic Algorithm elements in JSON files containing important information of the experiment done for MRCPSP Problem.
Created by: Edgar RP
Version: 0.1
"""
import os
import json

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
        save_path (Str): String with the path of where will be saved the project params.
        project (Dict): Dictionary containing all the parameters for the project.
    """
    if not os.path.isdir(save_path):
        raise ValueError('Did you give a valid and created save path? Path given: {}'.format(save_path))

    json = {}
    for key in project:
        if key != "jobs":
            json[key] = project[key]
    # Here I will execute the code to save the json