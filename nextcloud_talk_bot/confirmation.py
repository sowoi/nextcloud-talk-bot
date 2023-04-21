import logging
from .i18n import _


class Confirmation:
    """
    A class used to confirm user actions with irreversible consequences.
    """

    def __init__(self, object, entity, input_func=input):
        """
        :param object: str
            The action to be confirmed (e.g., "delete", "overwrite").
        :param entity: str
            The name of the item the action will be applied to (e.g., "file", "record").
        :param input_func: Callable
            A function used to get user input. Defaults to the built-in `input()` function.
        """
        self.object = object
        self.entity = entity
        self.input_func = input_func
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def are_you_sure(self):
        """
        Asks the user for confirmation to proceed with the action on the given entity.

        :return: bool
            True if the user confirms the action, False otherwise.
        """
        while True:
            user_input = self.input_func(
                f"{_('Are you sure you want to ')}{self.object} '{self.entity}'? {_('This process is irrevocable! (yes/no): ')}"
            )
            if user_input.lower() == _("no"):
                self.logger.info(
                    f"Action '{self.object}' on '{self.entity}' was cancelled.")
                return False
            elif user_input.lower() == _("yes"):
                self.logger.info(
                    f"Action '{self.object}' on '{self.entity}' was confirmed.")
                return True
            else:
                self.logger.warning(
                    "Invalid input. Please enter 'yes' or 'no'.")
                print(_("Invalid input. Please enter 'yes' or 'no'."))
