import gettext

locale_path = "../locales"
supported_languages = ["de", "fr", "es"]
translation = gettext.translation(
    "NextcloudTalkBot",
    localedir=locale_path,
    languages=supported_languages,
    fallback=True)
_ = translation.gettext


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
                return False
            elif user_input.lower() == _("yes"):
                return True
            else:
                print(_("Invalid input. Please enter 'yes' or 'no'."))
