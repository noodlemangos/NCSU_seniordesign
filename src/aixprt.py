"""

#############
aixprt.py
#############

******
About
******

aixprt.py is the program that drives the backend of this program.
It runs workloads using tensorflow.
It creates/stores/retrieves workloads and suites via .json files.
It calculates the runtimes of each workload and outputs
that data to an output file and a database

**Authors:**
    Jane Hiltz

    Will James

*******************
Class Documentation
*******************

"""

import json
import time
import datetime
import subprocess
import platform
import psutil
import os
import shutil
from workload import Workload
from pathlib import Path


def record_data(file_path, start_time, runtime_data):
    """
    Calculates workload runtime, records machine specifications, outputs runtime to a file, and posts recorded data to the specified webpage

    :param file_path: path to where the output file will be stored\n
    :param start_time: when the workload began running\n
    :param runtime_data: a list that contains information about the run\n
    """
    # initializing variables for runtime
    end_time = datetime.datetime.now()
    run_time = end_time - start_time
    run_time = run_time.total_seconds() * 1000000000
    run_time = int(run_time)

    # Records the workload being ran for the workload statistics
    record_workload(runtime_data[0], run_time, start_time)

    # URL where the recorded runtime data is sent to
    url = "http://127.0.0.1:8000/entries/"

    # Preparing/retrieving runtime data to be sent
    processor = platform.processor()
    memory = float(round((psutil.virtual_memory().total / (1024.0 ** 3)), 2))
    os_version = platform.platform()
    disk_storage = float(round((psutil.disk_usage('/').total / (1024.0 ** 3)), 2))

    # Writing all of the installed packages through Anaconda to a json file
    package_versions = ""
    try:
        subprocess.call("conda list --json > versions.json", shell=True)
    except:
        package_versions = "Not Available"

    json_path = Path("versions.json")
    if (not json_path.is_file()):
        versions = "Not Available"

    # Reads the data from the newly created json file, and deletes the file
    if (not (package_versions == "Not Available")):
        data = {}
        with open('versions.json') as json_file:
            data = json.load(json_file)
            json_file.close()
        os.remove("versions.json")

        # Formats the data to be sent to the database
        for x in data:
            package_versions += f"{x['name']} {x['version']}, "

        if package_versions.endswith(', '):
            package_versions = package_versions[:-2]

    file_name = (
        f"{start_time.year}-{start_time.month}-{start_time.day}_{start_time.hour}-{start_time.minute}-{start_time.second}")
    # outputting metric data to output.txt
    output_file = open(f"{file_path}{file_name}", "w")
    output_file.write(f"Ran at: {str(start_time)}\n")
    output_file.write(f"Runtime (in nanoseconds): {run_time}\n")
    output_file.write(f"Start Time: {start_time.hour}:{start_time.minute}:{start_time.second}\n")
    output_file.write(f"End Time: {end_time.hour}:{end_time.minute}:{end_time.second}\n")
    output_file.write(f"Processor: {processor}\n")
    output_file.write(f"Memory (GB): {memory}\n")
    output_file.write(f"OS Version: {os_version}\n")
    output_file.write(f"Disk Storage (GB): {disk_storage}\n")
    output_file.write(f"Package Versions: {package_versions}\n")
    output_file.write(f"Workload Name: {runtime_data[0]}\n")
    output_file.write(f"Comments: {runtime_data[1]}\n")
    output_file.write(f"Command Line: {runtime_data[2]}\n")
    output_file.write("\n")  # blank new line for easier reading
    output_file.close()

    # Uses the "curl" command to make a POST to the Django webpage, which is then stored in the Postgresql database
    subprocess.call(
        ["curl", "-d",
         f"workload_model={runtime_data[3]}&command={runtime_data[2]}&runtime={run_time}&processor={processor}&memory={memory}&os_version={os_version}&disk_storage={disk_storage}&package_versions={package_versions}",
         "-X", "POST", url])


def record_workload(workload_name, runtime, start_time):
    """
    Creates or adds to a statistics json file that keeps statistics on workloads that have been run

    :param workload_name: workload whose run metrics will be added to the statistics\n
    :param runtime: amount of time in nanoseconds that it took the workload to run\n
    :param start_time: time when the workload was initially run\n
    """
    # Checks if a statistics file has been created/started
    json_path = Path("statistics.json")
    data = {}
    if json_path.is_file():
        with open('statistics.json') as json_file:
            data = json.load(json_file)
            json_file.close()
    # If a statistics file doesn't exists, a new dictionary for one is started
    else:
        data['workload_count'] = 0
        data['total_workload_runtime'] = 0
        data['longest_workload_runtime'] = runtime
        data['shortest_workload_runtime'] = runtime
        data['recent_workloads'] = []

    data['workload_count'] += 1
    data['total_workload_runtime'] += runtime

    if runtime > data['longest_workload_runtime']:
        data['longest_workload_runtime'] = runtime
    if runtime < data['shortest_workload_runtime']:
        data['shortest_workload_runtime'] = runtime

    # Only the most recent ten workloads are displayed, if another workload is run the oldest of the most recent is replaced
    if len(data['recent_workloads']) >= 10:
        data['recent_workloads'].pop(0)

    data['recent_workloads'].append({
        'name': workload_name,
        'runtime': runtime,
        'date/time': f"{start_time.month}/{start_time.day}/{start_time.year} {start_time.hour}:{start_time.minute}:{start_time.second}"
    })

    with open('statistics.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
        json_file.close()


def get_statistics():
    """
    Returns A dictionary with all of the needed statistics for the GUI home screen

    :return: A dictionary with the keys average_workload_runtime (float), longest_workload_runtime (int),
    shortest_workload_runtime (int), and recent_workloads (list).  The recent_workloads key corresponds to a list of the most recent ten workloads run, in dictionary form. These workloads have the keys: name, runtime, and date/time
    """
    # The dictionary to be returned is created with default values incase a statistics file hasn't been started
    stats = {
        'average_workload_runtime': "Not Available",
        'longest_workload_runtime': "Not Available",
        'shortest_workload_runtime': "Not Available",
        'recent_workloads': []
    }

    json_path = Path("statistics.json")
    data = {}
    if json_path.is_file():
        with open('statistics.json') as json_file:
            data = json.load(json_file)
            json_file.close()
    else:
        return stats

    if not (data['workload_count'] == 0):
        stats['average_workload_runtime'] = data['total_workload_runtime'] / data['workload_count']
    stats['longest_workload_runtime'] = data['longest_workload_runtime']
    stats['shortest_workload_runtime'] = data['shortest_workload_runtime']
    stats['recent_workloads'] = data['recent_workloads']

    return stats


def run_workload(iterations, workload_name):
    """
    Runs a workload. It gets the workload object and then calls run on the workload

    :param iterations: how many times should the workload run\n
    :param workload_name: name of the workload to run\n
    :return: 1 if there was a failure, 0 if a workload run successfully\n
    """
    # Validate workload iterations
    try:
        iterations = int(iterations)
    except:
        print("invalid workload iterations")
        return 1

    if iterations <= 0:
        print("invalid workload iterations")
        return 1
    # If valid, set to count
    count = iterations

    workloads = get_workloads()
    wl = workloads.get(workload_name, None)
    if wl is None:
        print(f"No workload with the name {workload_name} exists")
        return 1

    while count > 0:
        start_time = datetime.datetime.now()

        wl.run()
        record_data("../results/", start_time,
                    [workload_name, wl.comment, wl.command, wl.tfhub_model])

        if (wl.command is None or wl.command == ""):
            shutil.rmtree("/tmp/bottleneck")

        count -= 1

    # Return sucess
    return 0


def get_workloads():
    """
    Retrieves the current workloads in the workloads.json file and returns them as a dictionary of paired
    workload names and Workload objects

    :return: A dictionary with each workload name being used as keys to access the related workload objects
    """
    data = {}
    json_path = Path("workloads.json")
    if (not json_path.is_file()):
        return data

    data = load_workloads()
    workloads_dict = {}

    for x in data['workloads']:
        wl = Workload(x['name'], x['comment'], x['tfhub model'], x['training steps'], x['learning rate'],
                      x['testing percentage'], x['validation percentage'], x['eval step interval'],
                      x['train batch size'], x['test batch size'], x['validation batch size'], x['flip left/right'],
                      x['random crop'], x['random scale'], x['random brightness'], x['command'])
        workloads_dict[x['name']] = wl

    return workloads_dict


def load_workloads():
    """
    Opens the workloads.json file and returns a dictionary containing the current workloads in the system

    :return: A dictionary containing the current workloads in the system
    """

    with open('workloads.json') as json_file:
        data = json.load(json_file)
        json_file.close()
        return data


def add_workload(name, comment, tfhub_model, training_steps, learning_rate, testing_percentage, validation_percentage,
                 eval_step_interval, train_batch_size, test_batch_size,
                 validation_batch_size, flip_left_right, random_crop, random_scale, random_brightness, command=None):
    """
    Adds a new workload entry to the workloads.json file

    :param name: Name of the new workload\n
    :param comment: Optional workload comment/description of the workload\n
    :param tfhub_model: URL pertaining to the machine learning model that is to be used from Tensorflow's github\n
    :param training_steps: The number of training steps that are run before ending\n
    :param learning_rate: Numerical rate pertaining to the rate of learning when training\n
    :param testing_percentage: Percentage of images to use as a test set\n
    :param validation_percentage: Percentage of images to use as a validation set\n
    :param eval_step_interval: Number of steps to evaluate the training results after\n
    :param train_batch_size: Number of images to train on at a time\n
    :param test_batch_size: Number of images to test on. "-1" causes  the entire test set to be used\n
    :param validation_batch_size: Number of images to use in the evaluation batch. "-1" causes the entire validation set to be used\n
    :param flip_left_right: True or False, whether to randomly flip half of the training images horizontally\n
    :param random_crop: Percentage determining how much of a margin to randomly crop off the training images\n
    :param random_scale: Percentage determining how much to randomly scale the size of the training images by\n
    :param random_brightness: Percentage determining how much to randomly multiply the training image input pixels up or down by\n
    :param command: Optional console command to be run upon running this workload\n
    :return: A list of invalid parameters if an error has occured. A 0 is returned on success\n
    """
    # Creating a new workload to validate parameters
    new_WL = Workload(name, comment, tfhub_model, training_steps, learning_rate, testing_percentage,
                      validation_percentage,
                      eval_step_interval, train_batch_size, test_batch_size,
                      validation_batch_size, flip_left_right, random_crop, random_scale, random_brightness, command)

    invalid_params = ""
    invalid_params = new_WL.validate_parameters()

    # If parameters are valid, then try to open workloads.json
    if len(invalid_params) == 0:
        json_path = Path("workloads.json")
        if json_path.is_file():
            data = load_workloads()
            for x in data['workloads']:
                # Check if a workload with the same name already exists; if so, don't add this new one
                if (x['name'] == name):
                    print(f"Workload {name} already exists.")
                    return 1
        # If workloads.json exists and the workload is acceptable, then add it to the workloads dictionary
        else:
            data = {}
            data['workloads'] = []
        data['workloads'].append({
            'name': new_WL.name,
            'comment': new_WL.comment,
            'tfhub model': new_WL.tfhub_model,
            'training steps': new_WL.training_steps,
            'learning rate': new_WL.learning_rate,
            'testing percentage': new_WL.testing_percentage,
            'validation percentage': new_WL.validation_percentage,
            'eval step interval': new_WL.eval_step_interval,
            'train batch size': new_WL.train_batch_size,
            'test batch size': new_WL.test_batch_size,
            'validation batch size': new_WL.validation_batch_size,
            'flip left/right': new_WL.flip_left_right,
            'random crop': new_WL.random_crop,
            'random scale': new_WL.random_scale,
            'random brightness': new_WL.random_brightness,
            'command': new_WL.command
        })
        # Put updated dictionary into workloads.json 
        with open('workloads.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.close()
        # Success
        return 0
    else:
        return invalid_params


def edit_workload(original_name, new_name, comment, tfhub_model, training_steps, learning_rate, testing_percentage,
                  validation_percentage, eval_step_interval, train_batch_size, test_batch_size,
                  validation_batch_size, flip_left_right, random_crop, random_scale, random_brightness, command=None):
    """
    Edits an existing workload in the workloads.json file

    :param original_name: Name of the workload to be edited\n
    :param new_name: Name of the new workload\n
    :param comment: Optional workload comment/description of the workload\n
    :param tfhub_model: URL pertaining to the machine learning model that is to be used from Tensorflow's github\n
    :param training_steps: The number of training steps that are run before ending\n
    :param learning_rate: Numerical rate pertaining to the rate of learning when training\n
    :param testing_percentage: Percentage of images to use as a test set\n
    :param validation_percentage: Percentage of images to use as a validation set\n
    :param eval_step_interval: Number of steps to evaluate the training results after\n
    :param train_batch_size: Number of images to train on at a time\n
    :param test_batch_size: Number of images to test on. "-1" causes  the entire test set to be used\n
    :param validation_batch_size: Number of images to use in the evaluation batch. "-1" causes the entire validation set to be used\n
    :param flip_left_right: True or False, whether to randomly flip half of the training images horizontally\n
    :param random_crop: Percentage determining how much of a margin to randomly crop off the training images\n
    :param random_scale: Percentage determining how much to randomly scale the size of the training images by\n
    :param random_brightness: Percentage determining how much to randomly multiply the training image input pixels up or down by\n
    :param command: Optional console command to be run upon running this workload\n
    :return: A list of invalid parameters if an error has occured\n
    """
    # Creating a updated workload to validate parameters
    new_WL = Workload(new_name, comment, tfhub_model, training_steps, learning_rate, testing_percentage,
                      validation_percentage,
                      eval_step_interval, train_batch_size, test_batch_size,
                      validation_batch_size, flip_left_right, random_crop, random_scale, random_brightness, command)

    invalid_params = ""
    invalid_params = new_WL.validate_parameters()

    # If parameters are valid, then try to open workloads.json
    if len(invalid_params) == 0:
        data = {}
        json_path = Path("workloads.json")
        # Check if the workloads file exists in order to edit it
        if (not json_path.is_file()):
            print("There are currently no workloads to edit.")
            return
        # If it exists, then load the workloads from it    
        data = load_workloads()
        # Edit the parameters of the workload corresponding to the original name
        for x in data['workloads']:
            if x['name'] == original_name:
                x['name'] = new_WL.name
                x['comment'] = new_WL.comment
                x['tfhub model'] = new_WL.tfhub_model
                x['training steps'] = new_WL.training_steps
                x['learning rate'] = new_WL.learning_rate
                x['testing percentage'] = new_WL.testing_percentage
                x['validation percentage'] = new_WL.validation_percentage
                x['eval step interval'] = new_WL.eval_step_interval
                x['train batch size'] = new_WL.train_batch_size
                x['test batch size'] = new_WL.test_batch_size
                x['validation batch size'] = new_WL.validation_batch_size
                x['flip left/right'] = new_WL.flip_left_right
                x['random crop'] = new_WL.random_crop
                x['random scale'] = new_WL.random_scale
                x['random brightness'] = new_WL.random_brightness
                x['command'] = new_WL.command
        # Put updated dictionary into workloads.json
        with open('workloads.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.close()

        return 0
    else:
        return invalid_params


def remove_workload(workload_name):
    """
    Removes a workload from the workloads.json

    :param workload_name: name of the workload being removed\n
    :return: the removed workload, if it was sucessfuly removed from the list; else, it returns 0\n
    """
    # Opening workloads.json into data
    data = {}
    json_path = Path("workloads.json")
    if (not json_path.is_file()):
        return data
    data = load_workloads()

    removed_WL = {}
    index = 0
    # Traverses through the list of workloads until it finds a matching name,
    # then it removes the workload from the list and saves it to removed_WL
    for x in data['workloads']:
        if x['name'] == workload_name:
            removed_WL = data['workloads'].pop(index)
        index += 1
        # If a workload was removed, then update the json and return the removed workload
    if removed_WL:
        with open('workloads.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.close()

        # Check if that workload was in any suites
        suite_appearances = is_workload_in_suites(workload_name)
        # If so, then remove them from the suites
        if not suite_appearances == 1:
            count = len(suite_appearances) - 1
            while count >= 0:
                remove_workload_from_suite(suite_appearances[count][1], suite_appearances[count][0])
                count -= 1

        # Create an actual workload object with removed_WL
        removed_WL = Workload(removed_WL['name'], removed_WL['comment'], removed_WL['tfhub model'],
                              removed_WL['training steps'], removed_WL['learning rate'],
                              removed_WL['testing percentage'], removed_WL['validation percentage'],
                              removed_WL['eval step interval'], removed_WL['train batch size'],
                              removed_WL['test batch size'], removed_WL['validation batch size'],
                              removed_WL['flip left/right'], removed_WL['random crop'], removed_WL['random scale'],
                              removed_WL['random brightness'], removed_WL['command'])
        return removed_WL
    # Else, return 0
    return 0


#######################################################
##################### SUITES CODE #####################
#######################################################

def run_suite(suite_name):
    """
    Runs a suite of workloads

    :param suite_name: name of suite to run\n
    :return: 1 if the suite specificed could not be found, 0 if the suite is ran successfully\n
    """
    # Check if the suite exists 
    if get_suite(suite_name) == 1:
        print("This suite does not exist")
        return 1

    # Loads the dictionary of suites in from the suites.json file
    suites_dict = load_suites()
    # Runs each workload in the suite
    for x in suites_dict[suite_name]:
        run_workload(int(x['iterations']), x['name'])

    return 0


def load_suites():
    """
    Opens the suites.json file and returns a dictionary containing the current suites in the system

    :return: a dictionary containing the suites or an empty dictionary if suites.json does not exist
    """
    # Checking to see if the suites.json file exists
    suites_dict = {}
    json_path = Path("suites.json")
    if (not json_path.is_file()):
        print("suites.json does not exist")
        return suites_dict
    # If it does exist, then open it and save its contents into a dictionary
    with open('suites.json') as json_file:
        suites_dict = json.load(json_file)
        json_file.close()
        return suites_dict


def get_suite(suite_name):
    """
    Gets a suite from the list of suites

    :param suite_name: name of suite being searched for\n
    :return: a list containing the workloads in the searched suite\n
    """
    suites_dict = load_suites()
    if suite_name in suites_dict:
        suite_contents = suites_dict[suite_name]
        return suite_contents
    print("no suite of this name exists")
    return 1


def add_suite(new_suite):
    """
    Adds a suite into the system through the suites.json

    :param new_suite: suite being added - this is a dictionary containing a name (key) and a list of workloads (pair)\n
    :return: 1 if an error occurs, 0 if the new suite is added successfully\n
    """
    # Gets the suite name
    new_suite_name = list(new_suite.keys())[0]

    # Checks the length of the new suite name
    if len(new_suite_name) > 25 or new_suite_name == "":
        print("Invalid suite name")
        return 1

    suites_dict = load_suites()
    # Checks to see if a suite of the same name already exists
    for x in suites_dict.keys():
        if x == new_suite_name:
            # A suite of this name already exists
            print("A suite of this name already exists")
            return 1
            # If not, then add it to the dictionary of suites
    suites_dict.update(new_suite)
    # Then update the suites.json
    with open('suites.json', "w") as json_file:
        json.dump(suites_dict, json_file, indent=4)
        json_file.close()
    # Successful add
    return 0


def edit_suite(original_name, updated_suite):
    """
    Edits a suite in the system through the suites.json

    :param original_name: name of suite being added (original if the name was changed)\n
    :param updated_suite: suite being edited - this is a dictionary containing a name (key) and a list of workloads (pair)\n
    :return: 1 if an error occurs, 0 if the suite is edited successfully\n
    """
    # Gets the suite name
    # suite_name = list(updated_suite.keys())[0]

    # Ensures there is a suite to edit
    if get_suite(original_name) == 1:
        print("No suite of this name exists to edit")
        return 1

    # Checks the length of the new suite name
    updated_suite_name = list(updated_suite.keys())[0]
    if len(updated_suite_name) > 25 or updated_suite_name == "":
        print("Invalid suite name")
        return 1

    suites_dict = load_suites()
    did_edit = False
    # Checks to see if that suite exists in the system
    for x in suites_dict.keys():
        if x == original_name:
            # A suite of this name exists so edit/update it 
            suites_dict.pop(x)
            suites_dict.update(updated_suite)
            did_edit = True
    if did_edit:
        # Then update the suites.json
        with open('suites.json', "w") as json_file:
            json.dump(suites_dict, json_file, indent=4)
            json_file.close()
            return 0
    else:
        print("No suite of this name exists to edit")
        return 1


def remove_suite(suite):
    """
    Removed a suite from the system through the suites.json

    :param suite: suite being removed\n
    :return: the suite removed from the system, this is null if no suite was removed\n
    """
    can_remove = False
    removed_suite = {}
    # Gets the suite name
    try:
        suite_name = list(suite.keys())[0]
    except:
        print("No suite of this name exists to remove")
        return 1

    suites_dict = load_suites()
    # If it can be removed, then remove it
    removed_suite = suites_dict.pop(suite_name)
    # Then update the suites.json
    with open('suites.json', "w") as json_file:
        json.dump(suites_dict, json_file, indent=4)
        json_file.close()
    # Return the removed suite
    return removed_suite


def edit_workload_in_suite(workload_index, workload_iterations, suite_name):
    """
    Edits a workload in a desired suite

    :param workload_index: index of the target workload in the suite's workload list\n
    :param workload_iterations: iterations the workload should run\n
    :param suite_name: name of suite that contains the workload to be removed\n
    :return: 1 if an error occured - the workload is not edited \n
    """
    suites_dict = load_suites()
    # Check to ensure the suite exists
    if get_suite(suite_name) == 1:
        print("No suite of this name exists to edit")
        return 1

    # Check to see if the suite has workloads to edit
    if len(suites_dict[suite_name]) <= 0:
        print("This suite is empty")
        return 1

        # Validate workload iterations
    if workload_iterations <= 0:
        print("invalid workload iterations")
        return 1

    # Check to ensure that the workload_index is within bounds
    if workload_index < len(suites_dict[suite_name]) and workload_index >= 0:
        suites_dict[suite_name][workload_index]['iterations'] = workload_iterations
        # int(SU_data["Small_Suite"][0]['iterations'])
        # Then update the suites.json
        with open('suites.json', "w") as json_file:
            json.dump(suites_dict, json_file, indent=4)
            json_file.close()
    else:
        print("Invalid workload index")
        return 1


def remove_workload_from_suite(workload_index, suite_name):
    """
    Removes a workload from a desired suite

    :param workload_index: index of the target workload in the suite's workload list\n
    :param suite_name: name of suite that contains the workload to be removed\n
    :return: the workload removed, if sucessful, or 1 if uncessful\n
    """
    suites_dict = load_suites()
    # Check to ensure the suite exists
    if get_suite(suite_name) == 1:
        print("No suite of this name exists to edit")
        return 1

    # Check to see if the suite has workloads to remove
    if len(suites_dict[suite_name]) <= 0:
        print("This suite is empty")
        return 1

        # Check to ensure that the workload_index is within bounds
    if workload_index < len(suites_dict[suite_name]) and workload_index >= 0:
        # Remove that workload from the suite
        removed_WL = suites_dict[suite_name].pop(workload_index)
        # Then update the suites.json
        with open('suites.json', "w") as json_file:
            json.dump(suites_dict, json_file, indent=4)
            json_file.close()
        # Return the removed workload
        return removed_WL

    # Else, return 1    
    print("Invalid workload index")
    return 1


def is_workload_in_suites(workload_name):
    """
    Checks to see if a workload is in suites

    :param workload_name: name of workload to search for\n
    :return: a list of the suites that contain the workload and the index in that suite where the workload occurs,
    or 1 if the workload is not in any suites.

     .. note::
        If a workload appears in the same suite multiple times, that suite will appear in the list multiple times but
        with the differet/respective indexes

    """
    suites_dict = load_suites()
    suites_list = []
    suite_index = 0
    workload_index = 0
    # Traverses the suites dictionary
    for suite in suites_dict:
        for workload in suites_dict[suite]:
            # Checking to see if the workload is in any of the suites
            if workload_name in workload['name']:
                # If so, then add it to the list at its index
                suite_name = list(suites_dict.keys())[suite_index]
                suites_list.append([suite_name, workload_index])
            workload_index += 1
        suite_index += 1
        workload_index = 0

        # If the suites list is empty, return 1
    if len(suites_list) <= 0:
        # print("This workload is not in any suites")
        return 1
    # Else, return the list     
    return suites_list
