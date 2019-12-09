"""
Tests the functionality of workload.py
"""

import pytest
import workload
import aixprt

def test___init__():
    # Create a workload
    workloadA = workload.Workload("Test_Workload", "this is a test", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", "200", "0.01", "10", "10", "10", "100", "-1", "100", "False", "0", "0", "0", "")
    # Check to ensure it was created corectly
    assert workloadA.name == "Test_Workload"
    assert workloadA.comment == "this is a test"
    assert workloadA.tfhub_model == "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1"
    assert workloadA.training_steps == "200"
    assert workloadA.learning_rate == "0.01"
    assert workloadA.testing_percentage == "10"
    assert workloadA.validation_percentage == "10"
    assert workloadA.eval_step_interval == "10"
    assert workloadA.train_batch_size == "100"
    assert workloadA.test_batch_size == "-1"
    assert workloadA.validation_batch_size == "100"
    assert workloadA.flip_left_right == "False"
    assert workloadA.random_crop == "0"
    assert workloadA.random_scale == "0"
    assert workloadA.random_brightness == "0"
    assert workloadA.command == "" 

    # Create a workload with a command
    workloadB = workload.Workload("Test_Command_Workload", "", '', "", "", "", "", "", "", "", "", "", "", "", "", "help dir")
    # Check to ensure it was created corectly
    assert workloadB.name == "Test_Command_Workload"
    assert workloadB.comment == ""
    assert workloadB.tfhub_model == ""
    assert workloadB.training_steps == ""
    assert workloadB.learning_rate == ""
    assert workloadB.testing_percentage == ""
    assert workloadB.validation_percentage == ""
    assert workloadB.eval_step_interval == ""
    assert workloadB.train_batch_size == ""
    assert workloadB.test_batch_size == ""
    assert workloadB.validation_batch_size == ""
    assert workloadB.flip_left_right == ""
    assert workloadB.random_crop == ""
    assert workloadB.random_scale == ""
    assert workloadB.random_brightness == ""
    assert workloadB.command == "help dir"

def test_validate_parameters():
    # Test casting with a valid workload
    # Create a workload and validate it
    workloadA = workload.Workload("Test_Workload", "this is a test", "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1", "200", "0.01", "10", "10", "10", "100", "-1", "100", "False", "0", "0", "0", "")
    valid = workloadA.validate_parameters()
    expected_vavlid = []
    assert expected_vavlid == valid
    # Check to ensure the parameters were cast correctly
    assert workloadA.name == "Test_Workload" and type(workloadA.name) == str
    assert workloadA.comment == "this is a test" and type(workloadA.comment) == str
    assert workloadA.tfhub_model == "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1" and type(workloadA.tfhub_model) == str
    assert workloadA.training_steps == 200 and type(workloadA.training_steps) == int
    assert workloadA.learning_rate == 0.01 and type(workloadA.learning_rate) == float
    assert workloadA.testing_percentage == 10 and type(workloadA.testing_percentage) == int
    assert workloadA.validation_percentage == 10 and type(workloadA.validation_percentage) == int
    assert workloadA.eval_step_interval == 10 and type(workloadA.eval_step_interval) == int
    assert workloadA.train_batch_size == 100 and type(workloadA.train_batch_size) == int
    assert workloadA.test_batch_size == -1 and type(workloadA.test_batch_size) == int
    assert workloadA.validation_batch_size == 100 and type(workloadA.validation_batch_size) == int
    assert workloadA.flip_left_right == False and type(workloadA.flip_left_right) == bool
    assert workloadA.random_crop == 0 and type(workloadA.random_crop) == int
    assert workloadA.random_scale == 0 and type(workloadA.random_scale) == int
    assert workloadA.random_brightness == 0 and type(workloadA.random_brightness) == int
    assert workloadA.command == ""  and type(workloadA.command) == str

    # Test a workload with 1 invalid parameter
    invalid_WL_1 = workload.Workload("wrong_workload", "test comment", 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1', "4100", "0.02", "1.0", "20", "10", "100", "-2", "100", "True", "0", "0", "0", "")
    invalid_1 = invalid_WL_1.validate_parameters()
    expected_invalid_1 = ["testing_percentage"]
    assert invalid_1 == expected_invalid_1

    # Test a workload with everything wrong (except for the comment and command parameters, which can both be empty strings)
    invalid_WL_2 = workload.Workload("", "", '', "cat", "0..02", "1.0", "False", "-10", "asdga100", "--2", "1%00", "FTrue", "z", "e", "ro", "")
    invalid_2 = invalid_WL_2.validate_parameters()
    expected_invalid_2 = ["name", "tfhub_model", "training_steps", "learning_rate", "testing_percentage", "validation_percentage", "eval_step_interval", "train_batch_size", "test_batch_size", "validation_batch_size", "flip_left_right", "random_crop", "random_scale", "random_brightness"]
    assert invalid_2 == expected_invalid_2    
