"""This file contains code to export the Genetic Algorithm elements in JSON files containing important information of the experiment done for MRCPSP Problem.
Created by: Edgar RP
Version: 1.0
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

def __format_index__(index, max_digits = 4):
    """This function format the index integer into a string with the maximun quantity of digits geivn.
    Args:
        index (Int): Integer to be formatted.
        max_digits (Int): How many digits must the number contain, e.g: if 4 then the range is from 0000 to 9999.
    """
    value = str(index)
    while len(value) < max_digits:
        value = '0' + value
    return value

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

def save_solution(save_path, filename, solution):
    """This function generate a folder called generations and inside create another folder with the generation_index as name and then save an excel for solution given containing the base_line and scenearios.
    Args:
        save_path (Str): String with the folder path of where will be saved the solution.
        filename (Str): String telling which name will have the solution to be saved.
        solution (Solution): An instances of Solution object.
    """
    __check_folder_path__(save_path)
    n_cols = len(solution.base_line.execution_line) + 1
    data_table = [[None]*n_cols]

    # Saving metrics
    data_table.append(["Solution Makespan", solution.makespan] + [None]*(n_cols - 2))
    data_table.append(["Solution Mean Makespan", solution.mean_makespan] + [None]*(n_cols - 2))
    data_table.append(["Solution Std Makespan", solution.std_makespan] + [None]*(n_cols - 2))
    data_table.append(["Solution Robustness", solution.solution] + [None]*(n_cols - 2))
    data_table.append(["Quality Robustness", solution.quality] + [None]*(n_cols - 2))
    data_table.append([None]*n_cols)

    # Saving base line and scenarios
    for i, schedule in enumerate([solution.base_line] + solution.scenarios):
        if i == 0:
            data_table.append(["Base Line"] + [None]*(n_cols - 1))
        else:
            data_table.append(["Scenario {}".format(i)] + [None]*(n_cols - 1))
        data_table.append(["Activities"] + schedule.execution_line)
        data_table.append(["Start Times"] + schedule.time_line)
        data_table.append(["Durations"] + schedule.job_durations)
        data_table.append([None]*n_cols)

    pd.DataFrame(data_table).to_excel(os.path.join(save_path, filename + ".xlsx"), index=False)

def save_generation(save_path, generation_index, solutions):
    """This function generate a folder called generations and inside create another folder with the generation_index as name and then save an excel for solution given containing the base_line and scenearios.
    Args:
        save_path (Str): String with the folder path of where will be saved the generation.
        generation_index (Int): An integer indicating what generation will be saved.
        solutions (List[Solution]): A list containing instances of Solutions objects.
    """
    __check_folder_path__(save_path)

    generations_folder = os.path.join(save_path, "generations")
    if not os.path.isdir(generations_folder):
        os.mkdir(generations_folder)
    generation_path = os.path.join(generations_folder, __format_index__(generation_index, 6))
    os.mkdir(generation_path)

    for i, sol in enumerate(solutions):
        save_solution(generation_path, "Solution_{}".format(i + 1), sol)