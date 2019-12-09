"""
Tests the functionality of aixprt.py
"""
import os
import platform
import subprocess
import pytest
import datetime
import json
from pathlib import Path
import aixprt
from workload import Workload

# Setup and Teardown
def setup():
    # Setting up workloads.json for testing
    if platform.system() == "Windows": #TODO: REMOVE WINDOWS COMMANDS FOR FINAL PROJECT 
        print("im on windows")
        # For Workloads
        os.system('move workloads.json backup.json')
        os.system('copy tests\\test_workloads.json test_backup.json')
        os.system('move tests\\test_workloads.json workloads.json')
        # For Suites
        os.system('move suites.json backup_suites.json')
        os.system('copy tests\\test_suites.json test_backup_suites.json')
        os.system('move tests\\test_suites.json suites.json')
        # For Statistics
        os.system('move statistics.json backup_statistics.json')
        os.system('copy tests\\test_statistics.json test_backup_statistics.json')
        os.system('move tests\\test_statistics.json statistics.json')
    if platform.system() == "Linux":
        print("im on linux")
        # For Workloads
        os.system('mv workloads.json backup.json')
        os.system('cp tests/test_workloads.json test_backup.json')
        os.system('mv tests/test_workloads.json workloads.json')
        # For Suites
        os.system('mv suites.json backup_suites.json')
        os.system('cp tests/test_suites.json test_backup_suites.json')
        os.system('mv tests/test_suites.json suites.json')
        # For Statistics
        os.system('mv statistics.json backup_statistics.json')
        os.system('cp tests/test_statistics.json test_backup_statistics.json')
        os.system('mv tests/test_statistics.json statistics.json')
    
    print("Setup!")


def teardown():
    if platform.system() == "Windows": #TODO: REMOVE WINDOWS COMMANDS FOR FINAL PROJECT 
        print("im on windows")
        # For Workloads
        os.system('move test_backup.json tests\\test_workloads.json')
        os.system('move backup.json workloads.json')
        # For Suites
        os.system('move test_backup_suites.json tests\\test_suites.json')
        os.system('move backup_suites.json suites.json')   
        # For Statistics
        os.system('move test_backup_statistics.json tests\\test_statistics.json')
        os.system('move backup_statistics.json statistics.json')
        # For output files
        os.system('del tests\\test_results\\2009-10-13_3-2-1')
    if platform.system() == "Linux":
        print("im on linux")
        # For Workloads
        os.system('mv test_backup.json tests/test_workloads.json')
        os.system('mv backup.json workloads.json')
        # For Suites
        os.system('mv test_backup_suites.json tests/test_suites.json')
        os.system('mv backup_suites.json suites.json')
        # For Statistics
        os.system('mv test_backup_statistics.json tests/test_statistics.json')
        os.system('mv backup_statistics.json statistics.json')
        # For output files
        os.system('rm tests/test_results/2009-10-13_3-2-1')   
    print("Teardown!") 

###########################
###### Metric Tests #######
###########################

def test_record_data():
    # data for tests
    runtime_data_1 = ["Smallest_Workload", "This is a test", "python TensorFlow/retrain.py --image_dir ../../flower_photos --how_many_training_steps 10 --learning_rate 0.01 --testing_percentage 10 --validation_percentage 10 --eval_step_interval 10 --train_batch_size 100 --test_batch_size -1 --validation_batch_size 100 --tfhub_module https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", "Wl_model"]
    runtime_data_2 = ["Smaller_Workload", "This is a test", "python TensorFlow/retrain.py --image_dir ../../flower_photos --how_many_training_steps 100 --learning_rate 0.01 --testing_percentage 10 --validation_percentage 10 --eval_step_interval 10 --train_batch_size 100 --test_batch_size -1 --validation_batch_size 100 --tfhub_module https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", "WL_model"]
    start_time_1 = datetime.datetime(2009, 10, 13, 3, 2, 1)
    start_time_2 = datetime.datetime(1999, 12, 31, 23, 59, 59)

    # Create output
    aixprt.record_data("tests/test_results/", start_time_1, runtime_data_1)
    # Ensure file was created
    file_path = Path("tests/test_results/2009-10-13_3-2-1")
    assert file_path.is_file()
    # Open file and save it into a list, line by line, to be compared
    file_1 = open("tests/test_results/2009-10-13_3-2-1", "r")
    file_1_list = []
    for line in file_1.readlines():
        file_1_list.append(line)
    # Ensure the output is correct
    assert "Ran at:" in file_1_list[0] 
    assert "Runtime (in nanoseconds):" in file_1_list[1]
    assert file_1_list[2] == "Start Time: 3:2:1\n"
    assert "End Time:" in file_1_list[3] 
    assert "Processor:" in file_1_list[4]
    assert "Memory (GB):" in file_1_list[5]
    assert "OS Version:" in file_1_list[6]
    assert "Disk Storage (GB):" in file_1_list[7]
    assert "Package Versions:" in file_1_list[8]
    assert file_1_list[9] == "Workload Name: Smallest_Workload\n"
    assert file_1_list[10] == "Comments: This is a test\n"
    assert file_1_list[11] == "Command Line: python TensorFlow/retrain.py --image_dir ../../flower_photos --how_many_training_steps 10 --learning_rate 0.01 --testing_percentage 10 --validation_percentage 10 --eval_step_interval 10 --train_batch_size 100 --test_batch_size -1 --validation_batch_size 100 --tfhub_module https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1\n"

def test_record_workload():
    # data for tests
    workload_name = "test_workload1"
    runtime = 123456789
    start_time_1 = datetime.datetime(2009, 10, 13, 3, 2, 1)

    # Record the test workload
    aixprt.record_workload(workload_name, runtime, start_time_1)

    # Ensure Statistics file is created
    file_path = Path("statistics.json")
    assert file_path.is_file()

    # Read in statistics data
    test_data = {}
    if file_path.is_file():
        with open('statistics.json') as json_file:
            test_data = json.load(json_file)
            json_file.close()

    # Test Statistics data is accurate
    assert test_data['workload_count'] == 1
    assert test_data['total_workload_runtime'] == 123456790
    assert test_data['longest_workload_runtime'] == 123456789
    assert test_data['shortest_workload_runtime'] == 123456789
    assert len(test_data['recent_workloads']) == 1
    assert test_data['recent_workloads'][0]['name'] == workload_name
    assert test_data['recent_workloads'][0]['runtime'] == runtime
    assert test_data['recent_workloads'][0]['date/time'] == "10/13/2009 3:2:1"

    # Test no more than nine recent workloads are recorded at one time
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)
    aixprt.record_workload(workload_name, runtime, start_time_1)

    if file_path.is_file():
        with open('statistics.json') as json_file:
            test_data = json.load(json_file)
            json_file.close()

    assert len(test_data['recent_workloads']) == 10

def test_get_statistics():
    # data for tests
    workload_name = "test_workload1"
    runtime = 123456789
    start_time_1 = datetime.datetime(2009, 10, 13, 3, 2, 1)

    # Get home page statistics data
    test_stats = aixprt.get_statistics()

    # Test statistcs data is accurate when zero workloads have been recorded
    assert test_stats['average_workload_runtime'] == "Not Available"
    assert test_stats['longest_workload_runtime'] == 0
    assert test_stats['shortest_workload_runtime'] == 999999999999999
    assert len(test_stats['recent_workloads']) == 0

    # Record one test workload and get the new statistics data
    aixprt.record_workload(workload_name, runtime, start_time_1)
    test_stats = aixprt.get_statistics()

    # Test that the statistics data is accurate
    assert test_stats['average_workload_runtime'] == 123456790
    assert test_stats['longest_workload_runtime'] == 123456789
    assert test_stats['shortest_workload_runtime'] == 123456789
    assert len(test_stats['recent_workloads']) == 1
    assert test_stats['recent_workloads'][0]['name'] == workload_name
    assert test_stats['recent_workloads'][0]['runtime'] == runtime
    assert test_stats['recent_workloads'][0]['date/time'] == "10/13/2009 3:2:1"

###########################
##### Workload Tests ######
###########################

def test_run_workload():
    
    # Setup
    aixprt.add_workload("test_workload1", "test comment", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "10", "0.02", "10", "20", "10", "100", "-1", "100", "True", "0", "0", "0", "")
    aixprt.add_workload("test_workload2", "", '', "", "", "", "", "", "", "", "", "", "", "", "", "help dir")
    # Try running a workload with invalid iterations
    assert aixprt.run_workload('five', "Small_Workload") == 1
    assert aixprt.run_workload(-2, "Small_Workload") == 1
    # Try running a workload that is not in the system
    assert aixprt.run_workload(3, "Not_in_System") == 1
    # Sucessfully run a workload
    assert aixprt.run_workload(1, "test_workload1") == 0
    # Sucessfully run a command based workload
    assert aixprt.run_workload(1, "test_workload2") == 0
    
    pass


def test_load_workloads():
    # Workloads.json copy to test against 
    test_WL_dict = {
        "workloads": [
            {
                "name": "test_workload(I_v3)",
                "comment": "",
                "tfhub model": "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1",
                "training steps": 4000,
                "learning rate": 0.01,
                "testing percentage": 10,
                "validation percentage": 10,
                "eval step interval": 10,
                "train batch size": 100,
                "test batch size": -1,
                "validation batch size": 100,
                "flip left/right": False,
                "random crop": 0,
                "random scale": 0,
                "random brightness": 0,
                "command": ""
            },
            {
                "name": "Small_Workload",
                "comment": "",
                "tfhub model": "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1",
                "training steps": 200,
                "learning rate": 0.01,
                "testing percentage": 10,
                "validation percentage": 10,
                "eval step interval": 10,
                "train batch size": 100,
                "test batch size": -1,
                "validation batch size": 100,
                "flip left/right": False,
                "random crop": 0,
                "random scale": 0,
                "random brightness": 0,
                "command": ""
            }
        ]
    }    
    # Run load_workloads 
    WL_data = aixprt.load_workloads()
    assert test_WL_dict == WL_data

def test_get_workloads():
    workload1 = Workload("test_workload(I_v3)", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 4000, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    workload2 = Workload("Small_Workload", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 200, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    # Call get_workloads 
    WL_data = aixprt.get_workloads()
    # Check that there are only 2 workloads in the list and ensure both are correct
    assert len(WL_data) == 2
    assert "test_workload(I_v3)" in WL_data
    assert "Small_Workload" in WL_data
    assert compare_workloads(WL_data["test_workload(I_v3)"], workload1)
    assert compare_workloads(WL_data["Small_Workload"], workload2)
      

def test_add_workload():
    WL_data = aixprt.get_workloads()
    workload1 = Workload("test_workload1", "test comment", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', 4100, 0.02, 10, 20, 10, 100, -2, 100, True, 0, 0, 0, "")
    
    # Test to ensure that the workload to be added does not exist in the file
    assert not "test_workload1" in WL_data
    # Then add and assert that it does exist in it
    aixprt.add_workload("test_workload1", "test comment", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "4100", "0.02", "10", "20", "10", "100", "-2", "100", "True", "0", "0", "0", "")
    WL_data = aixprt.get_workloads()
    assert "test_workload1" in WL_data
    assert compare_workloads(WL_data["test_workload1"], workload1)

    # Try to add the same workload again and ensure it does not
    assert len(WL_data) == 3
    assert aixprt.add_workload("test_workload1", "test comment", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "4100", "0.02", "10", "20", "10", "100", "-2", "100", "True", "0", "0", "0", "") == 1
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 3

    # Try to add invalid workloads and ensure it does not
    # Workload with 1 thing wrong
    invalid_1 = aixprt.add_workload("wrong_workload", "test comment", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "4100", "0.02", "1.0", "20", "10", "100", "-2", "100", "True", "0", "0", "0", "")
    expected_invalid_1 = ["testing_percentage"]
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 3
    assert len(invalid_1) == 1
    assert invalid_1 == expected_invalid_1
    # Workload with everything wrong (except for the comment and command parameters, which can both be empty strings)
    invalid_2 = aixprt.add_workload("", "", '', "cat", "0..02", "1.0", "False", "1.0", "asdga100", "--2", "1%00", "FTrue", "z", "e", "ro", "")
    expected_invalid_2 = ["name", "tfhub_model", "training_steps", "learning_rate", "testing_percentage", "validation_percentage", "eval_step_interval", "train_batch_size", "test_batch_size", "validation_batch_size", "flip_left_right", "random_crop", "random_scale", "random_brightness"]
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 3
    assert len(invalid_2) == 14 #TODO fix after regex is corrected
    assert invalid_2 == expected_invalid_2

    # Add a workload with a command
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 3
    assert aixprt.add_workload("test_workload2", "", '', "", "", "", "", "", "", "", "", "", "", "", "", "help dir") == 0
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 4    

def test_edit_workload():
    # Workloads to compare against
    workload1 = Workload("test_workload(I_v3)", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 4000, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    workload2 = Workload("Small_Workload", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 200, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    # Call get_workloads 
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 2

    # Check that both workloads exist in the system
    assert compare_workloads(WL_data["test_workload(I_v3)"], workload1)
    assert compare_workloads(WL_data["Small_Workload"], workload2)

    # Now edit the first workload
    aixprt.edit_workload("test_workload(I_v3)", "workload_edited", "edited", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", "5000", "0.01", "10", "10", "20", "100", "-2", "100", "True", "0", "0", "0", "")
    workload1_edited = Workload("workload_edited", "edited", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 5000, 0.01, 10, 10, 20, 100, -2, 100, True, 0, 0, 0, "")
    
    # Enure it was edited properly
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 2
    assert not "test_workload(I_v3)" in WL_data
    assert "workload_edited" in WL_data
    assert compare_workloads(WL_data["workload_edited"], workload1_edited)
    
    # Now try to edit a workload to have all invalid parameters (with the exception of name, comment, and command)
    actual_invalid = aixprt.edit_workload("Small_Workload", "invalidWL", "", '', "cat", "0.0.0.0", "1.0", "False", "1.0", "asdga100", "--2", "1%00", "FTrue", "z", "e", "ro", "")
    expected_invalid = ["tfhub_model", "training_steps", "learning_rate", "testing_percentage", "validation_percentage", "eval_step_interval", "train_batch_size", "test_batch_size", "validation_batch_size", "flip_left_right", "random_crop", "random_scale", "random_brightness"]
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 2
    assert len(expected_invalid) == 13
    assert expected_invalid == actual_invalid
    
    # Ensure that the workload was not edited
    assert compare_workloads(WL_data["Small_Workload"], workload2)

def test_remove_workload():
    expected_workload1 = Workload("test_workload(I_v3)", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 4000, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    expected_workload2 = Workload("Small_Workload", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 200, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    expected_workload3 = Workload("Smaller_Workload", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 100, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")

    # Ensure file is setup properly
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 2
    assert "test_workload(I_v3)" in WL_data
    assert "Small_Workload" in WL_data
    
    # Try to remove a non-existent workload
    assert aixprt.remove_workload("Not_in_file") == 0
    assert len(WL_data) == 2
    assert "test_workload(I_v3)" in WL_data
    assert "Small_Workload" in WL_data
    
    # Remove an existing workload
    actual_workload1 = aixprt.remove_workload("test_workload(I_v3)")
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 1
    assert not "test_workload(I_v3)" in WL_data 
    assert compare_workloads(expected_workload1, actual_workload1)

    # Remove an existing workload that is used in a suite
    suite1 = aixprt.get_suite("Small_Suite")
    assert len(suite1) == 2
    actual_workload2 = aixprt.remove_workload("Small_Workload")
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 0
    assert not "Small_Workload" in WL_data 
    assert compare_workloads(expected_workload2, actual_workload2)
    suite1 = aixprt.get_suite("Small_Suite")
    assert len(suite1) == 1
    assert not "Small_Workload" in suite1 

    # Remove a workload that occurs multiple times in multiple suites
    # Setup for this particular test:
    aixprt.add_workload("test_workload(I_v3)", "", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "4100", "0.01", "10", "10", "10", "100", "-1", "100", "False", "0", "0", "0", "")
    aixprt.add_workload("Small_Workload", "", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "200", "0.01", "10", "10", "10", "100", "-1", "100", "False", "0", "0", "0", "")
    aixprt.add_workload("Smaller_Workload", "", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "100", "0.01", "10", "10", "10", "100", "-1", "100", "False", "0", "0", "0", "")
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 3
    suite2_A = aixprt.get_suite("Small_Suite")
    assert len(suite2_A) == 1
    suite2_B = aixprt.get_suite("Smaller_Suite")
    assert len(suite2_B) == 2
    # Now remove 
    actual_workload3 = aixprt.remove_workload("Smaller_Workload")
    WL_data = aixprt.get_workloads()
    assert len(WL_data) == 2
    assert not "Smaller_Workload" in WL_data
    assert compare_workloads(expected_workload3, actual_workload3)
    suite2_A = aixprt.get_suite("Small_Suite")
    assert len(suite2_A) == 0
    assert not "Smaller_Workload" in suite2_A
    suite2_B = aixprt.get_suite("Smaller_Suite")
    assert len(suite2_B) == 0
    assert not "Smaller_Workload" in suite2_B
    


###########################
###### Suites Tests #######
###########################

def test_run_suite():
    
    # Setup
    assert aixprt.add_workload("test_workload1", "test comment", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "10", "0.02", "10", "20", "10", "100", "-2", "100", "True", "0", "0", "0", "") == 0
    assert aixprt.add_workload("test_workload2", "", '', "", "", "", "", "", "", "", "", "", "", "", "", "help dir") == 0
    new_suite = {
        "new_suite": [
            {
                "name": "test_workload1",
                "iterations": "2"
            },
            {
                "name": "test_workload2",
                "iterations": "1"
            }
        ]
    }
    assert aixprt.add_suite(new_suite) == 0
    # Run a suite sucessfully
    assert aixprt.run_suite("new_suite") == 0
    # Try to run a suite that does not exist
    assert aixprt.run_suite("Not_in_system") == 1
    
    pass


def test_load_suites():
    # Suites.json copy to test against 
    test_SU_dict = {
        "Small_Suite": [
            {
                "name": "Small_Workload",
                "iterations": "1"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "2"
            }
        ],
        "Smaller_Suite": [
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            }
        ]
    }    
    # Run load_suites
    SU_data = aixprt.load_suites()
    assert test_SU_dict == SU_data

def test_get_suite():
    # Expected contents for "Smaller_Suite" to compare against
    expected_suite = [
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            }
        ]
    assert expected_suite == aixprt.get_suite("Smaller_Suite")
    # Try to get a suite that doesn't exist in the system
    assert aixprt.get_suite("Not_in_system") == 1

def test_add_suite():
    # Load Suites and ensure there are only two suites in the file
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2
    # Add a new suite sucessfully
    new_suite = {
        "new_suite": [
            {
                "name": "test_workload(I_v3)",
                "iterations": "3"
            },
            {
                "name": "Small_Workload",
                "iterations": "2"
            }
        ]
    }
    new_suite_list = [
            {
                "name": "test_workload(I_v3)",
                "iterations": "3"
            },
            {
                "name": "Small_Workload",
                "iterations": "2"
            }
        ]
    assert aixprt.add_suite(new_suite) == 0
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 3
    assert new_suite_list == aixprt.get_suite("new_suite")
    # Now try to add that same suite again and ensure it is not added
    assert aixprt.add_suite(new_suite) == 1
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 3
    # Try to add a suite with a name that exceeds the character limit (20)
    long_suite = {
        "this_name_is_wayyyyyyyyyyyyyyyyyyyyyyyyyyy_longer_than_twenty_characters": [
            {
                "name": "test_workload(I_v3)",
                "iterations": "2"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "2"
            }
        ]
    }   
    assert aixprt.add_suite(long_suite) == 1
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 3   

def test_edit_suite():
    # Load Suites and ensure there are only two suites in the file
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2

    # Edit a suite sucessfully
    edited_suite1 = {    
        "Smaller_Suite": [
            {
                "name": "Smaller_Workload",
                "iterations": "2"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            }
        ]
    }
    edited_suite_list1 = [
            {
                "name": "Smaller_Workload",
                "iterations": "2"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            }
        ]
    assert aixprt.edit_suite("Smaller_Suite", edited_suite1) == 0
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2
    assert edited_suite_list1 == aixprt.get_suite("Smaller_Suite")

    # Edit a suite with a new name sucessfully 
    edited_suite2 = {    
        "New_Suite": [
            {
                "name": "Small_Workload",
                "iterations": "3"
            },
            {
                "name": "Small_Workload",
                "iterations": "1"
            }
        ]
    }
    edited_suite_list2 = [
            {
                "name": "Small_Workload",
                "iterations": "3"
            },
            {
                "name": "Small_Workload",
                "iterations": "1"
            }
        ]
    assert aixprt.edit_suite("Small_Suite", edited_suite2) == 0
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2
    assert edited_suite_list2 == aixprt.get_suite("New_Suite")

    # Try to edit a suite that doesn't exist 
    edited_suite3 = {    
        "Not_exist": [
            {
                "name": "Small_Workload",
                "iterations": "3"
            },
            {
                "name": "Small_Workload",
                "iterations": "1"
            }
        ]
    }
    assert aixprt.edit_suite("Not_in_system", edited_suite3) == 1
    assert len(SU_data) == 2

    # Try to edit a suite with a new name that is too long    
    assert aixprt.edit_suite("this_name_is_wayyyyyyyyyyyyyyyyyyyy_longer_than_twenty_characters", edited_suite3) == 1
    assert len(SU_data) == 2    

def test_edit_workload_in_suite():
    # Load suites
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2   
    # Check original iterations for workloads
    assert int(SU_data["Small_Suite"][0]['iterations']) == 1
    assert int(SU_data["Small_Suite"][1]['iterations']) == 2
    # Edit iterations
    aixprt.edit_workload_in_suite(0, 5, "Small_Suite")
    aixprt.edit_workload_in_suite(1, 3, "Small_Suite")
    SU_data = aixprt.load_suites()
    assert int(SU_data["Small_Suite"][0]['iterations']) == 5
    assert int(SU_data["Small_Suite"][1]['iterations']) == 3
    # Try to edit with invalid iterations
    assert aixprt.edit_workload_in_suite(0, -5, "Small_Suite") == 1
    assert aixprt.edit_workload_in_suite(1, 0, "Small_Suite") == 1
    SU_data = aixprt.load_suites()
    assert int(SU_data["Small_Suite"][0]['iterations']) == 5
    assert int(SU_data["Small_Suite"][1]['iterations']) == 3
    # Try to edit from a suite that does not exist
    assert aixprt.edit_workload_in_suite(0, 4, "Not_in_system") == 1
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2  
    # Try to edit from a suite with no workloads
    aixprt.remove_workload_from_suite(0, "Small_Suite")
    aixprt.remove_workload_from_suite(0, "Small_Suite")
    SU_data = aixprt.load_suites()
    assert len(SU_data["Small_Suite"]) == 0
    assert aixprt.edit_workload_in_suite(0, 4, "Small_Suite") == 1
    assert aixprt.edit_workload_in_suite(1, 2, "Small_Suite") == 1


def test_remove_suite():
    # Expected suites removed 
    suite1 = {    
        "Small_Suite": [
            {
                "name": "Small_Workload",
                "iterations": "1"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "2"
            }
        ]
    }
    suite1_list = [
            {
                "name": "Small_Workload",
                "iterations": "1"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "2"
            }
        ]
    suite2 = {    
        "Smaller_Suite": [
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            }
        ]
    }
    suite2_list = [
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            },
            {
                "name": "Smaller_Workload",
                "iterations": "1"
            }
        ]
    # Load Suites and ensure there are two suites in the file
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2    
    # Try to remove a suite that does not exist
    assert aixprt.remove_suite("Not_in_system") == 1
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2  
    # Remove the two suites that do exist 
    assert suite1_list == aixprt.remove_suite(suite1)    
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 1
    assert suite2_list == aixprt.remove_suite(suite2)    
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 0           

def test_remove_workload_from_suite():
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2 
    # Check for target suite
    assert "Small_Suite" in SU_data
    assert len(SU_data["Small_Suite"]) == 2
    # Try to remove workloads from an index that is out of bounds
    assert aixprt.remove_workload_from_suite(-1, "Small_Suite") == 1
    assert len(SU_data["Small_Suite"]) == 2 
    assert aixprt.remove_workload_from_suite(2, "Small_Suite") == 1
    assert len(SU_data["Small_Suite"]) == 2 
    # Remove workloads from a suite sucessfully
    workload1 = {
            "name": "Small_Workload",
            "iterations": "1"
        }
    workload2 = {
            "name": "Smaller_Workload",
            "iterations": "2"
        }    
    assert workload2== aixprt.remove_workload_from_suite(1, "Small_Suite")
    SU_data = aixprt.load_suites()
    assert len(SU_data["Small_Suite"]) == 1
    assert workload1 == aixprt.remove_workload_from_suite(0, "Small_Suite")
    SU_data = aixprt.load_suites()
    assert len(SU_data["Small_Suite"]) == 0
    # Try to remove a workload from an empty suite 
    assert aixprt.remove_workload_from_suite(0, "Small_Suite") == 1
    SU_data = aixprt.load_suites()
    assert len(SU_data["Small_Suite"]) == 0
    # Try to remove from a suite that does not exist
    assert aixprt.remove_workload_from_suite(1, "Not_in_system") == 1

def test_is_workload_in_suites():
    SU_data = aixprt.load_suites()
    assert len(SU_data) == 2
    # Check for a workload not in any suites
    assert aixprt.is_workload_in_suites("test_workload(I_v3)") == 1    
    # Check for a workload in only 1 suite
    assert aixprt.is_workload_in_suites("Small_Workload") == [["Small_Suite", 0]]    
    # Check for a workload in multiple suites
    assert aixprt.is_workload_in_suites("Smaller_Workload") == [["Small_Suite", 1], ["Smaller_Suite", 0], ["Smaller_Suite", 1]] 


###########################
#### FOR TESTING ONLY #####
###########################

def compare_workloads(workloadA, workloadB):    
    """
    Compares two workloads
    :param workloadA: First workload being compared
    :param workloadB: Second workoad being compared
    :return: true if the workloads are equal and false if they are not
    """
    if not workloadA.name == workloadB.name:
        return False
    if not workloadA.comment == workloadB.comment:
        return False
    if not workloadA.tfhub_model == workloadB.tfhub_model:
        return False
    if not workloadA.training_steps == workloadB.training_steps:
        return False
    if not workloadA.learning_rate == workloadB.learning_rate:
        return False
    if not workloadA.testing_percentage == workloadB.testing_percentage:
        return False
    if not workloadA.validation_percentage == workloadB.validation_percentage:
        return False   
    if not workloadA.eval_step_interval == workloadB.eval_step_interval:
        return False   
    if not workloadA.train_batch_size == workloadB.train_batch_size:
        return False   
    if not workloadA.test_batch_size == workloadB.test_batch_size:
        return False   
    if not workloadA.validation_batch_size == workloadB.validation_batch_size:
        return False   
    if not workloadA.flip_left_right == workloadB.flip_left_right:
        return False   
    if not workloadA.random_crop == workloadB.random_crop:
        return False  
    if not workloadA.random_scale == workloadB.random_scale:
        return False
    if not workloadA.random_brightness == workloadB.random_brightness:
        return False
    if not workloadA.command == workloadB.command:
        return False        
    return True   

def test_compare_workloads():
    workloadA_1 = Workload("Small_Workload", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 200, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    workloadA_2 = Workload("Small_Workload", "", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 200, 0.01, 10, 10, 10, 100, -1, 100, False, 0, 0, 0, "")
    workloadB = Workload("test_workload(I_v3)", "comment", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", 4000, 0.02, 30, 10, 110, 100, -3, 100, True, 0, 0, 0, "")
    assert compare_workloads(workloadA_1, workloadA_2)
    assert not compare_workloads(workloadA_1, workloadB)
