"""
#############
workload.py
#############

******
About
******

workload.py is a class representation of a workload. A workload object
will contain all of its customizable parameters, be able to validate its
parameters, and be able to run themselves using Tensorflow

**Authors:**
    Jane Hiltz

    Will James

"""

import subprocess
import re


class Workload(object):
    """
    Workload Class.

    :param name: Name of the new workload\n
    :param comment: Comment to be associated with the Workload\n
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
    """

    def __init__(self, name, comment, tfhub_model, training_steps, learning_rate, testing_percentage,
                 validation_percentage, eval_step_interval, train_batch_size, test_batch_size, validation_batch_size,
                 flip_left_right, random_crop, random_scale, random_brightness, command):
        """
        Documented above.
        """

        self.name = name
        self.comment = comment
        self.tfhub_model = tfhub_model
        self.training_steps = training_steps
        self.learning_rate = learning_rate
        self.testing_percentage = testing_percentage
        self.validation_percentage = validation_percentage
        self.eval_step_interval = eval_step_interval
        self.train_batch_size = train_batch_size
        self.test_batch_size = test_batch_size
        self.validation_batch_size = validation_batch_size
        self.flip_left_right = flip_left_right
        self.random_crop = random_crop
        self.random_scale = random_scale
        self.random_brightness = random_brightness
        self.command = command

    def validate_parameters(self):
        """
        Retrieves the current workloads in the workloads.json file and returns them as a list of Workload objects
        :return: a list of the invalid parameters; if all are valid, the list is empty
        """
        invalid = []
        # Regex validators
        pattern_string = re.compile(r".[^ \t]+")
        pattern_comment = re.compile(r"(.*\n*)+")
        pattern_float = re.compile(r"\d*\.\d+|\d+")
        pattern_int = re.compile(r"^\d+$") 
        pattern_int_signed = re.compile(r"^-?\d+$") 
        pattern_bool = re.compile(r"true|True|false|False")
        # Name should be a string no greater than 30 characters
        if re.match(pattern_string, self.name) and not (self.name == "" or self.name is None or len(self.name) > 25):
            self.name = str(self.name)
        else:
            invalid.append("name")
        # Comment should be strings that also allow for new lines
        if re.match(pattern_comment, self.comment):
            self.comment = str(self.comment)
        else:
            invalid.append("comment")

        if (self.command == "" or self.command is None): 
            # URL should be a string
            if re.match(pattern_string, self.tfhub_model):
                self.tfhub_model = str(self.tfhub_model)
            else:
                invalid.append("tfhub_model")
            # Training Steps should be a int
            if re.match(pattern_int, self.training_steps):
                self.training_steps = int(self.training_steps)
            else:
                invalid.append("training_steps")
            # Learning Rate should be a float
            if re.match(pattern_float, self.learning_rate) and self.learning_rate.count('.') <= 1:
                self.learning_rate = float(self.learning_rate)
            else:
                invalid.append("learning_rate")
            # Testing Percentage should be an int
            if re.match(pattern_int, self.testing_percentage):
                self.testing_percentage = int(self.testing_percentage)
            else:
                invalid.append("testing_percentage")
            # Validation Percentage should be an int
            if re.match(pattern_int, self.validation_percentage):
                self.validation_percentage = int(self.validation_percentage)
            else:
                invalid.append("validation_percentage")
            # Eval Steps Interval should be an int
            if re.match(pattern_int, self.eval_step_interval):
                self.eval_step_interval = int(self.eval_step_interval)
            else:
                invalid.append("eval_step_interval")
            # Train Batch Size should be an int
            if re.match(pattern_int, self.train_batch_size):
                self.train_batch_size = int(self.train_batch_size)
            else:
                invalid.append("train_batch_size")
            # Test Batch Size should be a signed int
            if re.match(pattern_int_signed, self.test_batch_size):
                self.test_batch_size = int(self.test_batch_size)
            else:
                invalid.append("test_batch_size")
            # Validation Batch Size should be an int
            if re.match(pattern_int, self.validation_batch_size):
                self.validation_batch_size = int(self.validation_batch_size)
            else:
                invalid.append("validation_batch_size")
            # Flip Left Right should be a boolean
            if self.flip_left_right == "true" or self.flip_left_right == "True":
                self.flip_left_right = True
            elif self.flip_left_right == "false" or self.flip_left_right == "False":
                self.flip_left_right = False
            else:
                invalid.append("flip_left_right")
            # Random Crop should be an int
            if re.match(pattern_int, self.random_crop):
                self.random_crop = int(self.random_crop)
            else:
                invalid.append("random_crop")
            # Random Scale should be an int
            if re.match(pattern_int, self.random_scale):
                self.random_scale = int(self.random_scale)
            else:
                invalid.append("random_scale")
            # Random Brightness should be an int
            if re.match(pattern_int, self.random_brightness):
                self.random_brightness = int(self.random_brightness)
            else:
                invalid.append("random_brightness")

        #Printing for testing
        if len(invalid) > 0:
            print("Invalid Parameters:")
            print(*invalid, sep=", ")

        return invalid

    def run(self):
        """
        Runs the workload by calling Tensorflow's retrain.py script or by calling the workload's custom command argument
        """
        if self.command == "" or self.command is None:
            # Checking if the variables that drastically increase runtime have been changed from the default values
            if self.flip_left_right or self.random_brightness != 0 or self.random_crop != 0 or self.random_scale != 0:
                self.command = f"python TensorFlow/retrain.py --image_dir ../../flower_photos --how_many_training_steps {self.training_steps} --learning_rate " +\
                f"{self.learning_rate} --testing_percentage {self.testing_percentage} --validation_percentage {self.validation_percentage} --eval_step_interval " +\
                f"{self.eval_step_interval} --train_batch_size {self.train_batch_size} --test_batch_size {self.test_batch_size} --validation_batch_size " +\
                f"{self.validation_batch_size} --flip_left_right {self.flip_left_right} --random_crop {self.random_crop} --random_scale {self.random_scale} --random_brightness " +\
                f"{self.random_brightness} --tfhub_module {self.tfhub_model}"
                
                subprocess.call(["python", "TensorFlow/retrain.py", "--image_dir", "../../flower_photos", "--how_many_training_steps",
                     f"{self.training_steps}", "--learning_rate",
                     f"{self.learning_rate}", "--testing_percentage", f"{self.testing_percentage}",
                     "--validation_percentage", f"{self.validation_percentage}", "--eval_step_interval",
                     f"{self.eval_step_interval}", "--train_batch_size", f"{self.train_batch_size}", "--test_batch_size",
                     f"{self.test_batch_size}", "--validation_batch_size",
                     f"{self.validation_batch_size}", "--flip_left_right", f"{self.flip_left_right}", "--random_crop",
                     f"{self.random_crop}", "--random_scale", f"{self.random_scale}",
                     "--random_brightness", f"{self.random_brightness}", "--tfhub_module", f"{self.tfhub_model}"])
            # If the previously checked variables are the same as the default values, exludes them from the subprocess call to avoid bogging down performance
            else:
                self.command = (f"python TensorFlow/retrain.py --image_dir ../../flower_photos --how_many_training_steps {self.training_steps} --learning_rate " +\
                f"{self.learning_rate} --testing_percentage {self.testing_percentage} --validation_percentage {self.validation_percentage} --eval_step_interval " +\
                f"{self.eval_step_interval} --train_batch_size {self.train_batch_size} --test_batch_size {self.test_batch_size} --validation_batch_size " +\
                f"{self.validation_batch_size} --tfhub_module {self.tfhub_model}")

                subprocess.call(
                    ["python", "TensorFlow/retrain.py", "--image_dir", "../../flower_photos", "--how_many_training_steps",
                     f"{self.training_steps}", "--learning_rate",
                     f"{self.learning_rate}", "--testing_percentage", f"{self.testing_percentage}",
                     "--validation_percentage", f"{self.validation_percentage}", "--eval_step_interval",
                     f"{self.eval_step_interval}", "--train_batch_size", f"{self.train_batch_size}", "--test_batch_size",
                     f"{self.test_batch_size}", "--validation_batch_size",
                     f"{self.validation_batch_size}", "--tfhub_module", f"{self.tfhub_model}"])
        else:
            subprocess.call(self.command, shell=True)
        
