class Confirmation:
    """
    A class used to confirm user actions with irreversible consequences.
    """

    def __init__(self, object, entity):
        """
        :param object: str
            The action to be confirmed (e.g., "delete", "overwrite").
        :param entity: str
            The name of the item the action will be applied to (e.g., "file", "record").
        """
        self.object = object
        self.entity = entity

    def are_you_sure(self):
        """
        Asks the user for confirmation to proceed with the action on the given entity.

        :return: bool
            True if the user confirms the action, False otherwise.
        """
        while True:
            user_input = input(
                f"Are you sure you want to {self.object} '{self.entity}'? This process is irrevocable! (yes/no): "
            )
            if user_input.lower() == "no":
                return False
            elif user_input.lower() == "yes":
                return True
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")