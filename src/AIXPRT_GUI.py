"""
#############
AIXPRT_GUI.PY
#############

******
About
******

This file is the main GUI file.  It takes advantage of aixprt.kv, which is the kivy file for this project.

**Authors:**
    Alex Phelps

    Claire Christopher

*******************
Class Documentation
*******************

"""

# This import MUST be first
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Makes the window unable to be resized.  This MUST be at the top of the file.
Config.set('graphics', 'resizable', 0)

# Disable multi-touch emulation
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

# backend imports
import aixprt

# Sets initial size of our Window
Window.size = (1200, 750)

# The left of where our Window spawns.  200 pixels from the left of the screen.
Window.left = 200

# The top of where our Window spawns.  40 pixels from top of screen.
Window.top = 40


class HomeScreen(Screen):
    """
    The home screen.  Layout is defined in the aixprt.kv file.
    """
    my_stats = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_interval(self.calc_stats, 0.5)

    def calc_stats(self, dt):
        self.my_stats = aixprt.get_statistics()
        self.ids.average_workload_runtime.text = str(round(self.my_stats['average_workload_runtime'], 2))
        self.ids.longest_workload_runtime.text = str(self.my_stats['longest_workload_runtime'])
        self.ids.shortest_workload_runtime.text = str(self.my_stats['shortest_workload_runtime'])
        for i, y in zip(reversed(self.my_stats['recent_workloads']), range(10)):
            self.ids["recent" + str(y + 1)].text = i['name']
            self.ids["date" + str(y + 1)].text = i['date/time']


class NavBar(FloatLayout):
    """
    The navigation bar.  Layout is defined in the aixprt.kv file.
    """

    pass


class WorkloadScreen(Screen):
    """
    The workload screen.  Layout is defined in the aixprt.kv file.  Used to run workloads.
    """
    num_iterations = 1
    active_workload = None

    def refresh_page(self):
        """
        Refreshes widgets on the page.
        """
        self.ids.spin_workload.values = App.get_running_app().workloads
        self.ids.spin_workload.text = 'Choose...'
        self.active_workload = None

    def delete_workload(self):
        """
        Deletes the workload currently selected in the spin_workload Spinner.
        """
        if self.ids.spin_workload.text != 'Choose...':
            aixprt.remove_workload(str(self.ids.spin_workload.text))


class WorkloadEditScreen(Screen):
    """
    The screen to edit a workload.  Layout is defined in the aixprt.kv file.
    """
    active_workload = None

    def refresh_page(self):
        """
        Refreshes widgets on the page.
        """
        self.ids.spin_edit.values = App.get_running_app().workloads
        self.ids.edit_status.text = ''
        self.ids.spin_edit.text = 'Choose...'
        self.active_workload = None
        self.reset_fields()

    def update_fields(self):
        """
        Auto-fills TextInput boxes with data from the selected workload.
        """
        # Update active workload with our selected.
        if self.ids.spin_edit.text != 'Choose...':
            self.active_workload = aixprt.get_workloads()[self.ids.spin_edit.text]
            self.ids.name.text = self.active_workload.name
            self.ids.tfhub_model.text = self.active_workload.tfhub_model
            self.ids.training_steps.text = str(self.active_workload.training_steps)
            self.ids.learning_rate.text = str(self.active_workload.learning_rate)
            self.ids.testing_percentage.text = str(self.active_workload.testing_percentage)
            self.ids.validation_percentage.text = str(self.active_workload.validation_percentage)
            self.ids.eval_step_interval.text = str(self.active_workload.eval_step_interval)
            self.ids.train_batch_size.text = str(self.active_workload.train_batch_size)
            self.ids.test_batch_size.text = str(self.active_workload.test_batch_size)
            self.ids.validation_batch_size.text = str(self.active_workload.validation_batch_size)
            self.ids.flip_left_right.text = str(self.active_workload.flip_left_right)
            self.ids.random_crop.text = str(self.active_workload.random_crop)
            self.ids.random_scale.text = str(self.active_workload.random_scale)
            self.ids.random_brightness.text = str(self.active_workload.random_brightness)
            self.ids.comment.text = str(self.active_workload.comment)
            self.ids.command.text = str(self.active_workload.command)

            # Status should be initially blank
            self.ids.edit_status.text = ''

    def command_touched(self):
        """
        Helper method to determine behavior for when the command line is touched.
        """
        if self.ids.name.text != "":
            self.ids.save_edit_btn.disabled = False
        if self.ids.command.text == "":
            # Enable/Re-enable all text input boxes
            self.ids.tfhub_model.disabled = False
            self.ids.training_steps.disabled = False
            self.ids.learning_rate.disabled = False
            self.ids.testing_percentage.disabled = False
            self.ids.validation_percentage.disabled = False
            self.ids.eval_step_interval.disabled = False
            self.ids.train_batch_size.disabled = False
            self.ids.test_batch_size.disabled = False
            self.ids.validation_batch_size.disabled = False
            self.ids.flip_left_right.disabled = False
            self.ids.random_crop.disabled = False
            self.ids.random_scale.disabled = False
            self.ids.random_brightness.disabled = False
        else:
            # If the command is touched, disable all boxes except name and comment
            self.ids.tfhub_model.disabled = True
            self.ids.training_steps.disabled = True
            self.ids.learning_rate.disabled = True
            self.ids.testing_percentage.disabled = True
            self.ids.validation_percentage.disabled = True
            self.ids.eval_step_interval.disabled = True
            self.ids.train_batch_size.disabled = True
            self.ids.test_batch_size.disabled = True
            self.ids.validation_batch_size.disabled = True
            self.ids.flip_left_right.disabled = True
            self.ids.random_crop.disabled = True
            self.ids.random_scale.disabled = True
            self.ids.random_brightness.disabled = True

    def name_touched(self):
        """
        Helper method to determine behavior for when the name is touched.
        """
        if self.ids.command.text != "":
            self.ids.save_edit_btn.disabled = False
        if self.ids.name.text == "":
            self.ids.save_edit_btn.disabled = True
        else:
            self.ids.save_edit_btn.disabled = False

    def edit_workload(self):
        """
        Actual method call to edit a workload.  Passes in values from the TextInput boxes.
        """
        valid = aixprt.edit_workload(self.active_workload.name, self.ids.name.text, self.ids.comment.text,
                             self.ids.tfhub_model.text, self.ids.training_steps.text, self.ids.learning_rate.text,
                             self.ids.testing_percentage.text, self.ids.validation_percentage.text,
                             self.ids.eval_step_interval.text, self.ids.train_batch_size.text,
                             self.ids.test_batch_size.text, self.ids.validation_batch_size.text,
                             self.ids.flip_left_right.text, self.ids.random_crop.text, self.ids.random_scale.text,
                             self.ids.random_brightness.text, self.ids.command.text)

        if valid != 0:
            App.get_running_app().message_text = 'Failed To Edit Workload\nSee console for details.'
        else:
            App.get_running_app().message_text = 'Workload Edited.'

    def reset_fields(self):
        """
        Clears all fields on the page.
        """
        self.ids.name.text = ''
        self.ids.tfhub_model.text = ''
        self.ids.training_steps.text = ''
        self.ids.learning_rate.text = ''
        self.ids.testing_percentage.text = ''
        self.ids.validation_percentage.text = ''
        self.ids.eval_step_interval.text = ''
        self.ids.train_batch_size.text = ''
        self.ids.test_batch_size.text = ''
        self.ids.validation_batch_size.text = ''
        self.ids.flip_left_right.text = ''
        self.ids.random_crop.text = ''
        self.ids.random_scale.text = ''
        self.ids.random_brightness.text = ''
        self.ids.comment.text = ''
        self.ids.command.text = ''

    def reset_status(self):
        """
        Resets the status message on the page.
        """
        if self.ids.spin_edit.text != 'Choose...':
            self.ids.edit_status.text = 'Changes Not Saved!'


class WLPopup(Popup):
    """
    Custom Popup for editing a workload
    """
    new_iterations = 0
    wl_to_edit = None

    def save_iterations(self):
        """
        Save the number of iterations in edit_popup_it.
        """
        self.new_iterations = self.ids.edit_popup_it.text
        App.get_running_app().suite_status_list[int(App.get_running_app().wl_to_edit['wl_id'])] = self.new_iterations

    def remove_workload(self):
        """
        Remove the workload from the Suite.
        """
        App.get_running_app().suite_status_list[int(App.get_running_app().wl_to_edit['wl_id'])] = 'x'

    def decrement_wl(self):
        """
        Decrement the number of Workloads in the Suite.
        """
        App.get_running_app().wl_counter -= 1


class WorkloadAddScreen(Screen):
    """
    The workload add screen.  Layout is defined in the aixprt.kv file.
    """
    active_workload = None

    def refresh_page(self):
        """
        Refreshes widgets on the page.
        """
        self.ids.spin_add.values = App.get_running_app().workloads
        self.ids.spin_add.text = 'Choose...'
        self.active_workload = None
        self.reset_fields()

    def command_touched(self):
        """
        Helper method to determine behavior for when the command line is touched.
        """
        if self.ids.name.text != "":
            self.ids.save_add_btn.disabled = False
        if self.ids.command.text == "":
            # Enable/Re-enable all text input boxes
            self.ids.tfhub_model.disabled = False
            self.ids.training_steps.disabled = False
            self.ids.learning_rate.disabled = False
            self.ids.testing_percentage.disabled = False
            self.ids.validation_percentage.disabled = False
            self.ids.eval_step_interval.disabled = False
            self.ids.train_batch_size.disabled = False
            self.ids.test_batch_size.disabled = False
            self.ids.validation_batch_size.disabled = False
            self.ids.flip_left_right.disabled = False
            self.ids.random_crop.disabled = False
            self.ids.random_scale.disabled = False
            self.ids.random_brightness.disabled = False
        else:
            # If the command is touched, disable all boxes except name and comment
            self.ids.tfhub_model.disabled = True
            self.ids.training_steps.disabled = True
            self.ids.learning_rate.disabled = True
            self.ids.testing_percentage.disabled = True
            self.ids.validation_percentage.disabled = True
            self.ids.eval_step_interval.disabled = True
            self.ids.train_batch_size.disabled = True
            self.ids.test_batch_size.disabled = True
            self.ids.validation_batch_size.disabled = True
            self.ids.flip_left_right.disabled = True
            self.ids.random_crop.disabled = True
            self.ids.random_scale.disabled = True
            self.ids.random_brightness.disabled = True

    def name_touched(self):
        """
        Helper method to determine behavior for when the name is touched.
        """
        if self.ids.command.text != "":
            self.ids.save_add_btn.disabled = False
        if self.ids.name.text == "":
            self.ids.save_add_btn.disabled = True
        else:
            self.ids.save_add_btn.disabled = False

    def update_fields(self):
        """
        Auto-fills TextInput boxes with data from the selected workload.
        """
        # Update active workload with our selected. Probably needs to be
        # changed to use the workload list in AIXPRT class.
        if self.ids.spin_add.text != 'Choose...':
            self.active_workload = aixprt.get_workloads()[self.ids.spin_add.text]
            self.ids.name.text = self.active_workload.name
            self.ids.tfhub_model.text = self.active_workload.tfhub_model
            self.ids.training_steps.text = str(self.active_workload.training_steps)
            self.ids.learning_rate.text = str(self.active_workload.learning_rate)
            self.ids.testing_percentage.text = str(self.active_workload.testing_percentage)
            self.ids.validation_percentage.text = str(self.active_workload.validation_percentage)
            self.ids.eval_step_interval.text = str(self.active_workload.eval_step_interval)
            self.ids.train_batch_size.text = str(self.active_workload.train_batch_size)
            self.ids.test_batch_size.text = str(self.active_workload.test_batch_size)
            self.ids.validation_batch_size.text = str(self.active_workload.validation_batch_size)
            self.ids.flip_left_right.text = str(self.active_workload.flip_left_right)
            self.ids.random_crop.text = str(self.active_workload.random_crop)
            self.ids.random_scale.text = str(self.active_workload.random_scale)
            self.ids.random_brightness.text = str(self.active_workload.random_brightness)
            self.ids.comment.text = str(self.active_workload.comment)
            self.ids.command.text = str(self.active_workload.command)

    def add_workload(self):
        """
        Actual method call to add a workload.  Passes in values from the TextInput boxes.
        """
        valid = aixprt.add_workload(self.ids.name.text, self.ids.comment.text,
                                    self.ids.tfhub_model.text, self.ids.training_steps.text,
                                    self.ids.learning_rate.text,
                                    self.ids.testing_percentage.text, self.ids.validation_percentage.text,
                                    self.ids.eval_step_interval.text, self.ids.train_batch_size.text,
                                    self.ids.test_batch_size.text, self.ids.validation_batch_size.text,
                                    self.ids.flip_left_right.text, self.ids.random_crop.text,
                                    self.ids.random_scale.text,
                                    self.ids.random_brightness.text, self.ids.command.text)

        # Check if the workload was added successfully
        if valid != 0:
            if valid == 1:
                App.get_running_app().message_text = 'Workload Already Exists'
            else:
                App.get_running_app().message_text = 'Failed To Add Workload\nSee console for details.'
        else:
            App.get_running_app().message_text = 'Workload Added'

    def reset_fields(self):
        """
        Clears all fields on the page.
        """
        self.ids.name.text = ''
        self.ids.tfhub_model.text = ''
        self.ids.training_steps.text = ''
        self.ids.learning_rate.text = ''
        self.ids.testing_percentage.text = ''
        self.ids.validation_percentage.text = ''
        self.ids.eval_step_interval.text = ''
        self.ids.train_batch_size.text = ''
        self.ids.test_batch_size.text = ''
        self.ids.validation_batch_size.text = ''
        self.ids.flip_left_right.text = ''
        self.ids.random_crop.text = ''
        self.ids.random_scale.text = ''
        self.ids.random_brightness.text = ''
        self.ids.comment.text = ''
        self.ids.command.text = ''

    def reset_status(self):
        """
        Resets the status message
        """
        if self.ids.spin_edit.text != 'Choose...':
            self.ids.edit_status.text = 'Changes Not Saved!'


class MessageScreen(Screen):
    """
    Screen to display confirmation messages.  Will have a message and a button that takes you back home.
    """

    def update_message(self, message):
        """
        Populate the Label with the message stored in the App.

        :param message: The message to display.\n
        """
        self.ids.message.text = message


class ProgressScreen(Screen):
    """
    Screen to display progress.
    """

    num_iterations = 1

    def update_message(self, message):
        self.ids.message.text = message

    def run(self, source):
        """
        Runs either the workload or the suite depending on the source page.

        :param source: The page where the ProgressScreen was launched from.\n
        """
        self.num_iterations = App.get_running_app().workload_iterations
        if source == "WorkloadScreen":
            self.run_workload()
        else:
            self.run_suite()

    def run_suite(self):
        """
        Runs the Suite saved in the App.
        """
        valid = aixprt.run_suite(App.get_running_app().suite_to_run)
        self.ids.OK_btn.disabled = False
        if valid == 1:
            self.ids.message.text = 'Failed To Run Suite\nSee console for details.'
        else:
            self.ids.message.text = "Complete!"

    def run_workload(self):
        """
        Runs the Workload saved in the App.
        """
        valid = aixprt.run_workload(self.num_iterations, App.get_running_app().workload_to_run)
        self.ids.OK_btn.disabled = False
        if valid == 1:
            self.ids.message.text = 'Failed To Run Workload\nSee console for details.'
        else:
            self.ids.message.text = "Complete!"



class SuiteScreen(Screen):
    """
    The Suite screen.  Used to run Suites.  Layout is defined in the aixprt.kv file.
    """

    active_suite = None
    active_suite_name = ""

    def refresh_page(self):
        """
        Refreshes widgets on the page.
        """
        self.ids.spin_suite.values = App.get_running_app().suites
        self.ids.spin_suite.text = 'Choose...'
        self.active_suite = None

    def delete_suite(self):
        """
        Deletes the selected Suite from the system.
        :return:
        """
        if self.ids.spin_suite.text != 'Choose...':
            suite_to_delete = {self.ids.spin_suite.text: aixprt.get_suite(self.ids.spin_suite.text), }
            aixprt.remove_suite(suite_to_delete)

    def display_wl_labels(self, instance=None):
        """
        Display workload labels on the screen.

        :param instance: Kivy requires a second attribute to be passed so it is callable by a Clock.  Does nothing.\n
        """
        # Before showing the new workloads, clear the old ones:
        for i in range(10):
            self.ids["wl_" + str(i)].text = ''
        # Show workloads in labels and enable checkboxes for existing workloads
        for i in range(len(self.active_suite)):  ##once label id fixed, while loop with counter.
            if App.get_running_app().suite_status_list[i] == 'x':
                break  # everything after is an x too, no need to display.
            self.ids["wl_" + str(i)].text = self.active_suite[i]['name'] + ", Iterations: " + str(
                App.get_running_app().suite_status_list[i])

    def update_fields(self):
        """
        Auto-fills the labels on the screen with the Workloads in the Suite.
        """
        # Update active workload with our selected.
        if self.ids.spin_suite.text != 'Choose...':
            self.active_suite = aixprt.get_suite(self.ids.spin_suite.text)
            self.active_suite_name = self.ids.spin_suite.text
            App.get_running_app().wl_counter = len(self.active_suite)
            # Before showing the new workloads, clear the old ones:
            self.clear_labels()
            # Show workloads in labels and enable checkboxes for existing workloads
            for i in range(len(self.active_suite)):
                self.ids[
                    "wl_" + str(i)].text = self.active_suite[i]['name'] + ", Iterations: " + str(
                    self.active_suite[i]['iterations'])

    def clear_labels(self):
        """
        Clears all the workload labels on the page.
        """
        for i in range(10):
            self.ids["wl_" + str(i)].text = ''


class SuiteAddScreen(Screen):
    """
    The SuiteAddScreen.  Used to add new Suites to the system.  Layout is defined in the aixprt.kv file.
    """
    active_workload = None
    suite_to_add = []
    active_wl_iterations = 1

    # For checking if there's a suite name and at least one workload.
    added_name = False
    added_wl = False

    def refresh_page(self):
        """
        Refreshes widgets on the page.
        """
        self.ids.spin_suite_add.values = App.get_running_app().workloads
        self.ids.spin_suite_add.text = 'Choose...'
        self.ids.suite_add_btn.disabled = True
        self.active_workload = None
        self.active_wl_iterations = 1  # default iterations
        self.ids.suite_it_add.text = "1"
        # Check if button needs to be enabled, if there is at least one workload in the suite and a name entered
        if App.get_running_app().wl_counter > 0 and self.added_name:
            self.ids.suite_run_btn.disabled = False
        else:
            self.ids.suite_run_btn.disabled = True

    def add_workload(self):
        """
        Adds the selected Workload to the Suite you are creating.
        """
        if self.ids.spin_suite_add.text != 'Choose...' and App.get_running_app().wl_counter <= 10:
            self.ids.suite_add_btn.disabled = False
            # get wl
            self.active_workload = aixprt.get_workloads()[self.ids.spin_suite_add.text]
            # get iterations
            self.active_wl_iterations = self.ids.suite_it_add.text
            # add to list of suites
            wl_to_add = {"name": self.active_workload.name, "iterations": self.active_wl_iterations}
            self.suite_to_add.append(wl_to_add)
            # display workload on label
            self.ids["add_wl_" + str(
                App.get_running_app().wl_counter)].text = self.active_workload.name + ", Iterations: " + self.active_wl_iterations
            App.get_running_app().wl_counter += 1
            if App.get_running_app().wl_counter >= 10:
                self.ids.suite_add_btn.disabled = True
                self.ids.spin_suite_add.disabled = True
                self.ids.suite_max_add.text = "Max workloads added!"

            self.refresh_page()

    def clear_labels(self):
        """
        Clears all the workload labels on the page.
        """
        for i in range(10):
            self.ids["add_wl_" + str(i)].text = ''
        App.get_running_app().wl_counter = 0

    def add_suite(self):
        """
        Officially adds the Suite to the system.
        """
        suite_dict = {self.ids.suite_name_add.text: self.suite_to_add, }
        valid = aixprt.add_suite(suite_dict)
        self.suite_to_add = []

        if valid != 0:
            App.get_running_app().message_text = 'Failed To Add Suite\nSee console for details.'
        else:
            App.get_running_app().message_text = 'Suite Added'

    def name_added(self):
        """
        Helper method to determine behavior for when the name is touched.
        """
        if self.ids.suite_name_add.text != "":
            self.added_name = True
        else:
            self.added_name = False

        self.refresh_page()


class SuiteEditScreen(Screen):
    """
    The SuiteEditScreen.  Used to edit an already existing Suite in the system.  Layout is defined in the aixprt.kv file.
    """
    active_suite = None
    active_suite_name = None
    suite_to_add = []
    active_wl = None
    active_wl_iterations = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_interval(self.check_workloads, 0.01)

    # For checking if there's a suite name and at least one workload.
    added_name = False
    added_wl = False

    def check_workloads(self, dt=None):
        """
        Helper method to check the number of active Workloads

        :param dt: Kivy requires a second attribute to be passed so it is callable by a Clock.  Does nothing.\n
        """
        if App.get_running_app().wl_counter >= 10:
            self.ids.spin_wls_to_add.disabled = True
            self.ids.edit_suite_add_btn.disabled = True
            self.ids.suite_max_edit.text = "Max workloads added!"
        elif App.get_running_app().wl_counter >= 1:
            self.ids.spin_wls_to_add.disabled = False
            self.ids.suite_max_edit.text = ""
        else:
            self.ids.suite_max_edit.text = ""

    def refresh_page(self):
        """
        Refreshes widgets on the page.
        """
        self.ids.spin_suite_edit.values = App.get_running_app().suites
        self.ids.spin_wls_to_add.values = App.get_running_app().workloads
        self.ids.spin_suite_edit.text = 'Choose...'
        self.active_suite = None
        self.active_suite_name = None
        self.ids.spin_wls_to_add.disabled = True
        self.ids.edit_suite_name.text = ''
        self.ids.suite_max_edit.text = ""
        App.get_running_app().suite_status_list = []
        App.get_running_app().wl_counter = 0

    # So we don't reload the suite stuff after a WL is added.
    def get_suite_wl_status(self):
        """
        Get list of Workload statuses in the Suite.
        """
        App.get_running_app().suite_status_list = []
        for it in range(len(self.active_suite)):
            App.get_running_app().suite_status_list.append(str(self.active_suite[it]['iterations']))

    def refresh_wls(self):
        """
        Refresh workloads on the page.
        """
        self.active_wl = None
        self.active_wl_iterations = 1
        self.ids.spin_wls_to_add.text = "Choose..."
        self.ids.edit_suite_add_btn.disabled = True

    def update_fields(self):
        """
        Auto-fills the labels on the screen with the Workloads in the Suite.
        """
        # Update active workload with our selected.
        if self.ids.spin_suite_edit.text != 'Choose...':

            self.active_suite = aixprt.get_suite(self.ids.spin_suite_edit.text)
            self.active_suite_name = self.ids.spin_suite_edit.text
            self.ids.edit_suite_name.text = self.active_suite_name
            App.get_running_app().wl_counter = len(self.active_suite)
            self.clear_labels()
            # Show workloads in labels and enable checkboxes for existing workloads
            for i in range(len(self.active_suite)):
                self.ids[
                    "edit_wl_" + str(i)].text = self.active_suite[i]['name'] + ", Iterations: " + str(
                    self.active_suite[i][
                        'iterations']) + "  |  [u][size=20][color=#0000ff][ref=edit]Edit[/ref][/u][/size][/color]"

            # Status should be initially blank
            self.ids.edit_suite_status.text = ''
        if App.get_running_app().wl_counter >= 10:
            self.ids.suite_max_edit.text = "Max workloads added!"
        else:
            self.ids.suite_max_edit.text = ""

    def clear_labels(self):
        """
        Clears all the workload labels on the page
        """
        for i in range(10):
            self.ids["edit_wl_" + str(i)].text = ''
        self.ids.edit_suite_status.text = ''

    def count_workloads(self):
        """
        Counts number of valid Workloads in the Suite.
        """
        App.get_running_app().wl_counter = 0
        for i in range(len(App.get_running_app().suite_status_list)):
            if App.get_running_app().suite_status_list[i] != 'x':
                App.get_running_app().wl_counter += 1

    def display_wl_labels(self, instance=None):
        """
        Display workload labels on the screen.

        :param instance: Kivy requires a second attribute to be passed so it is callable by a Clock.  Does nothing.\n
        """
        # Before showing the new workloads, clear the old ones:
        self.clear_labels()
        self.order_list()
        self.count_workloads()
        # Show workloads in labels and enable checkboxes for existing workloads
        for i in range(len(App.get_running_app().suite_status_list)):  # changed from active_suite to suite_status_list
            if App.get_running_app().suite_status_list[i] == 'x':
                break  # everything after is an x too, no need to display.
            if App.get_running_app().suite_status_list[i] == 't':  ##if t, was just added. Not editable.
                self.ids["edit_wl_" + str(i)].text = self.active_suite[i]['name'] + ", Iterations: " + str(
                    self.active_suite[i]['iterations'])
            else:  ##editable. Changed
                self.ids["edit_wl_" + str(i)].text = self.active_suite[i]['name'] + ", Iterations: " + str(
                    App.get_running_app().suite_status_list[
                        i]) + "  |  [u][size=20][color=#0000ff][ref=edit]Edit[/ref][/u][/size][/color]"

    def add_workload(self):
        """
        Add's a workload to the suite
        """
        if self.ids.spin_wls_to_add.text != 'Choose...':
            self.ids.edit_suite_add_btn.disabled = False
            self.active_wl = aixprt.get_workloads()[self.ids.spin_wls_to_add.text]
            self.order_list()
            # get iterations
            self.active_wl_iterations = self.ids.edit_suite_wl_it
            # add to list of suites
            wl_to_add = {"name": self.active_wl.name, "iterations": self.active_wl_iterations.text}

            self.active_suite.append(wl_to_add)
            App.get_running_app().suite_status_list.append(
                't')  # t means uneditable. Don't remember why I picked t. Might change it.

            # display workload on label -- changed
            self.display_wl_labels()

            self.count_workloads()
            self.refresh_wls()

    def update_suite(self):
        """
        Officially updates the Suite in the system.
        """
        suite_original_name = self.ids.spin_suite_edit.text
        updated_suite = []
        for i in range(len(App.get_running_app().suite_status_list)):
            if App.get_running_app().suite_status_list[i] == 'x':
                continue  # don't add to our suite
            elif App.get_running_app().suite_status_list[i] == 't':
                updated_suite.append(
                    {'name': self.active_suite[i]['name'], 'iterations': self.active_suite[i]['iterations']})
            else:
                updated_suite.append(
                    {'name': self.active_suite[i]['name'], 'iterations': App.get_running_app().suite_status_list[i]})
        suite_dict = {self.ids.edit_suite_name.text: updated_suite}

        valid = aixprt.edit_suite(suite_original_name, suite_dict)
        if valid == 1:
            App.get_running_app().message_text = 'Failed To Save Suite\nSee console for details.'
        else:
            App.get_running_app().message_text = 'Suite Saved'

    def set_wl_clicked(self, label_id):
        """
        Helper method to properly show the popup.

        :param label_id: The label that was clicked, the workload to edit.\n
        """
        # get the whole workload (and iterations) as a dictionary
        # order is the whole workload, the index in the workload list, the name
        clicked_wl = {'wl': self.active_suite[int(label_id)], 'wl_id': label_id, "suite_name": self.active_suite_name}
        App.get_running_app().wl_to_edit = clicked_wl
        # Create the popup
        edit_popup = WLPopup()
        edit_popup.bind(on_dismiss=self.display_wl_labels)
        edit_popup.open()

    def order_list(self):
        """
        Order the workloads.
        """
        for i in range(len(App.get_running_app().suite_status_list)):
            if App.get_running_app().suite_status_list[i] == 'x':
                # if its an x we need to move it to the end.
                temp_wl = self.active_suite.pop(i)
                temp_status = App.get_running_app().suite_status_list.pop(i)
                # add to end
                self.active_suite.append(temp_wl)
                App.get_running_app().suite_status_list.append(temp_status)


class AixprtApp(App):
    """
    Main application, the central part of a kivy application.
    """
    # List of Workload objects
    workloads_obj = aixprt.get_workloads()

    # Names of all the workloads in the system
    workloads = aixprt.get_workloads().keys()

    # List of suites objects
    suites_obj = aixprt.load_suites()

    # Names of all the suites in the system
    suites = aixprt.load_suites().keys()

    # wl to edit on edit suite page
    wl_to_edit = None

    # List of suite statuses
    suite_status_list = []

    # Text to display on the message page
    message_text = ''

    # Passed to ProgressScreen to run
    suite_to_run = ''

    # Passed to ProgressScreen to run
    workload_to_run = ''

    # Number of workload iterations
    workload_iterations = 1

    # Count of workloads on the page
    wl_counter = 0

    # Page you just came from.  ScreenManager has a previous() function, but it only works based
    # on the order of the screens in the ScreenManager.  Thus, for dynamic screen returning we need to store
    # the name ourselves.
    source_page = ''

    # Need to manually refresh the workload list.  This does that every half-a-second
    def refresh_workloads(self):
        """
        Refresh the workloads in the App.
        """
        App.get_running_app().workloads_obj = aixprt.get_workloads()
        App.get_running_app().workloads = aixprt.get_workloads().keys()

    # Need to manually refresh the suites list.  This does that every half-a-second
    def refresh_suites(self):
        """
        Refresh the suites in the App.
        """
        App.get_running_app().suites_obj = aixprt.load_suites()
        App.get_running_app().suites = aixprt.load_suites().keys()

    Clock.schedule_interval(refresh_workloads, 0.5)
    Clock.schedule_interval(refresh_suites, 0.5)


# Starts the application at launch
if __name__ == '__main__':
    AixprtApp().run()
