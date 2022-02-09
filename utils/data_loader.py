"""This file contains code to load the csv files for the MRCPSP problem
Created by: Edgar RP
Version: 1.0.1
"""

import os
import numpy as np
import pandas as pd

def load_project(example_path):
  """This function loads the csv files contained in the example path (must contain only 3 csv with names "project_params", 
  "jobs_precedences" and "jobs_durations-modes"). Also checks the data integrity of the files and returns a dictionary of 
  the project with all the information contained in the csv files.
  Args:
    example_path (String): A string with the folder path that contains only 3 csv files.
  """
  resources_key_acronim = [("renewable_resources", "R"), ("nonrenewable_resources", "N"), ("doubly_constrained", "D")]

  #Check for the 3 csv files in the path
  if sorted(os.listdir(example_path)) != ["jobs_durations-modes.csv", "jobs_precedences.csv", "project_params.csv"]:
    raise AssertionError("The given path ({}) doesn't follow the structure stablished or contains valid files.")

  #Load all the files
  params = pd.read_csv(os.path.join(example_path, "project_params.csv"))
  precedences = pd.read_csv(os.path.join(example_path, "jobs_precedences.csv"))
  duration_modes = pd.read_csv(os.path.join(example_path, "jobs_durations-modes.csv"))

  #Check params data integrity
  for key, acronim in resources_key_acronim:
    for index in range(1, params[key].to_numpy()[0] + 1):
      if "{}{}_available".format(acronim, index) not in params.columns:
        raise AssertionError("The quantity of {} doesn't math with the columns in the params csv file.".format(key))
    
  if params["time_horizon"].to_numpy()[0] < np.sum(params[["rel_date","duedate","tardcost","MPM-Time"]].to_numpy()):
    raise AssertionError("The time horizon stablished in the data is less that the sum of the dates for the project.")

  #Check precedences and duration modes data integrity
  for key, acronim in resources_key_acronim:
    for index in range(1, params[key].to_numpy()[0] + 1):
      if "{}{}".format(acronim, index) not in duration_modes.columns:
        raise AssertionError("The quantity of {} doesn't math with the columns in the duration-modes csv file.".format(key))

  if precedences.to_numpy(na_value="").shape[0] != params["#jobs"].to_numpy()[0]:
    raise AssertionError("The quantity of jobs declared in params csv differs from the quantity exposed in precedences csv")

  modes_checking = duration_modes.groupby("jobnr").sum()
  for row in precedences.to_numpy(na_value=""):
    if row[-2] != 0: 
      if len(row[-1].split(" ")) != row[-2]:
        raise AssertionError("The quantity of successors of job {} is wrong respect the successors mentioned in the csv".format(row[0]))
    else:
      if len(row[-1]) != 0:
        raise AssertionError("The quantity of successors at the final job ({}) is wrong respect the successors mentioned in the csv".format(row[0]))

    if sum(range(1, row[1]+1)) != modes_checking["mode"].loc[row[0]]:
      raise AssertionError("The modes specified in duration-modes csv is wrong respect to the quantity declared in precedences csv file for the job {}".format(row[0]))

  #Definition of project dictionary
  resources = {}
  for key, acronim in resources_key_acronim:
    resources[key] = []
    for index in range(1, params[key].to_numpy()[0] + 1):
      resources[key].append(params["{}{}_available".format(acronim, index)].to_numpy()[0])

  project = {
    "nr_jobs": params["#jobs"].to_numpy()[0],
    "time_horizon": params["time_horizon"].to_numpy()[0],
    "init_random_value": params["init_random_value"].to_numpy()[0],
    "rel_date": params["rel_date"].to_numpy()[0],
    "duedate": params["duedate"].to_numpy()[0],
    "tardcost": params["tardcost"].to_numpy()[0],
    "MPM-Time": params["MPM-Time"].to_numpy()[0],
    "renewable_resources_total": tuple(resources["renewable_resources"]),
    "nonrenewable_resources_total": tuple(resources["nonrenewable_resources"]),
    "doubly_constrained_total": tuple(resources["doubly_constrained"]),
    "jobs": []
  }

  for index in duration_modes.index:
    resources = {}
    for key, acronim in resources_key_acronim:
      resources[key] = []
      for i in range(1, params[key].to_numpy()[0] + 1):
        resources[key].append(
          duration_modes.loc[index, "{}{}".format(acronim, i)]
        )

    successors = precedences.loc[duration_modes.loc[index, "jobnr"] - 1, "successors"]
    if pd.isna(successors):
      successors = []
    else:
      successors = [int(i) for i in successors.split(" ")]

    job = {
      "id": duration_modes.loc[index, "jobnr"],
      "mode": duration_modes.loc[index, "mode"],
      "duration": duration_modes.loc[index, "duration"],
      "successors": successors,
      "renewable_resources_use": np.r_[resources["renewable_resources"]],
      "nonrenewable_resources_use": np.r_[resources["nonrenewable_resources"]],
      "doubly_constrained_use": np.r_[resources["doubly_constrained"]]
    }
    project["jobs"].append(job)

  return project