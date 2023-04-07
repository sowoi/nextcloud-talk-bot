import os
import re
import subprocess
import random

class Iobroker:
    """
    A class to represent an Iobroker instance manager.
    
    Attributes
    ----------
    instance_list : list
        A list of available instances.
    selected_instances : list
        A list of user-selected instances.
    
    Methods
    -------
    get_instances():
        Retrieves the list of available instances and prints them.
    select_instances():
        Prompts the user to select instances they want to control and stores them in a list.
    count_objects():
        Counts and prints the number of unique objects in the selected instances.
    """

    def __init__(self):
        self.instance_list = []
        self.selected_instances = []

    def get_instances(self):
        """Retrieves the list of available instances and prints them."""
        command = "iobroker list instances"
        output = subprocess.getoutput(command)
        instances = re.findall(r'system.adapter.(\S+)', output)
        self.instance_list = instances
        print("Instances:")
        for instance in instances:
            print(instance)

    def select_instances(self):
        """
        Prompts the user to select instances they want to control and stores them in a list.
        """
        print("Enter the instance(s) you want to control (separated by commas):")
        user_input = input()
        user_instances = user_input.split(',')
        for instance in user_instances:
            instance = instance.strip()
            if instance in self.instance_list:
                self.selected_instances.append(instance)
            else:
                print(f"{instance} is not a valid instance.")
        print("Selected instances:")
        for instance in self.selected_instances:
            print(instance)

    def count_objects(self):
        """
        Counts and prints the number of unique objects in the selected instances.
        """
        unique_objects = set()
        for instance in self.selected_instances:
            command = f"iobroker list objects {instance}.*"
            output = subprocess.getoutput(command)
            objects = re.findall(rf'{instance}\.(\w+)', output)
            unique_objects.update(objects)
        print("Number of unique objects:", len(unique_objects))
        
    def get_random_state_attributes(self, num_samples=3):
        """
        Retrieves and prints random state attributes from the selected instances.

        Parameters
        ----------
        num_samples : int, optional
            The number of random state attributes to sample, by default 3.
        """
        
        print("Suggesting nextcloud talk commands for the Bot.") 
        all_state_attributes = []

        for instance in self.selected_instances:
            command = f"iobroker list objects {instance}.*"
            output = subprocess.getoutput(command)
            state_attributes = re.findall(rf'({instance}\.\w+\.\w+)', output)
            all_state_attributes.extend(state_attributes)

        if len(all_state_attributes) < num_samples:
            num_samples = len(all_state_attributes)

        random_samples = random.sample(all_state_attributes, num_samples)

        print("Random Iobroker commands:")
        for sample in random_samples:
            commands = [f"iobroker state getvalue {sample}", f"iobroker state set {sample} 'YourState'"]
            random_commands = random.choice(commands)
            print(f"{random_commands}")
            print("will then become Nextcloud Talk command")
            if "getvalue" in random_commands:
                print(f"/iob get {sample}")
            else:
                print(f"/iob set {sample}_'YourState'")
                
                
        print("""
In the following step two bash scripts will be created to configure the nextcloud commands. 
You need to run the script on your nextcloud server via CLI as user www-data. 
The second script is an uninstall script which will remove the nextcloud command. 
              """)
                
        
            

if __name__ == "__main__":
    iobroker = Iobroker()
    iobroker.get_instances()
    iobroker.select_instances()
    iobroker.count_objects()
    iobroker.get_random_state_attributes()
