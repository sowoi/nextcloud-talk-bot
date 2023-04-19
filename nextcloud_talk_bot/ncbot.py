import argparse
import importlib
import inspect
import ast
import spacy

import nextcloud_talk_bot
from nextcloud_talk_bot.first_run_setup import FirstRunSetup


class FirstSetup:
    @staticmethod
    def start_setup():
        FirstRunSetup.first_run()


class NLPCommands:
    def __init__(self):
        """
        Initializes the NLPCommands class and loads the 'en_core_web_sm' model using spaCy.
        """
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("The model 'en_core_web_sm' model could not be found. "
                  "Please run the following command to download the model:\n\n"
                  "python -m spacy download en_core_web_sm\n")
            raise

    def classify_poll_method(self, doc):
        """
        Classifies the poll-related method based on the given spaCy document.

        :param doc: A spaCy Doc object representing the user's input.
        :type doc: spacy.tokens.doc.Doc

        :return: A string representing the classified method.
        :rtype: str
        """
        close_poll_keywords = ["close", "end", "finish", "stop"]
        create_poll_keywords = ["create", "make", "new", "start"]
        get_poll_result_keywords = ["result", "outcome", "summary"]

        close_poll_count = 0
        create_poll_count = 0
        get_poll_result_count = 0

        for token in doc:
            if token.lemma_.lower() in close_poll_keywords:
                close_poll_count += 1
            elif token.lemma_.lower() in create_poll_keywords:
                create_poll_count += 1
            elif token.lemma_.lower() in get_poll_result_keywords:
                get_poll_result_count += 1

        if close_poll_count > create_poll_count and close_poll_count > get_poll_result_count:
            return "close_poll"
        elif create_poll_count > close_poll_count and create_poll_count > get_poll_result_count:
            return "create_poll"
        elif get_poll_result_count > close_poll_count and get_poll_result_count > create_poll_count:
            return "get_poll_result"
        else:
            return "unknown"

    def classify_user_method(self, doc):
        """
        Classifies the user-related method based on the given spaCy document.

        :param doc: A spaCy Doc object representing the user's input.
        :type doc: spacy.tokens.doc.Doc

        :return: A string representing the classified method.
        :rtype: str
        """
        get_preferred_language_keywords = [
            "language", "preferred", "preference"]
        get_quota_keywords = ["quota", "limit", "storage", "space"]
        test_user_login_keywords = ["login", "authenticate", "sign in", "test"]

        get_preferred_language_count = 0
        get_quota_count = 0
        test_user_login_count = 0

        for token in doc:
            if token.lemma_.lower() in get_preferred_language_keywords:
                get_preferred_language_count += 1
            elif token.lemma_.lower() in get_quota_keywords:
                get_quota_count += 1
            elif token.lemma_.lower() in test_user_login_keywords:
                test_user_login_count += 1

        if get_preferred_language_count > get_quota_count and get_preferred_language_count > test_user_login_count:
            return "get_preferred_language"
        elif get_quota_count > get_preferred_language_count and get_quota_count > test_user_login_count:
            return "get_quota"
        elif test_user_login_count > get_preferred_language_count and test_user_login_count > get_quota_count:
            return "test_user_login"
        else:
            return "unknown"

    def classify_message_method(self, doc):
        """
        Classifies the message-related method based on the given spaCy document.

        :param doc: A spaCy Doc object representing the user's input.
        :type doc: spacy.tokens.doc.Doc

        :return: A string representing the classified method.
        :rtype: str
        """
        delete_message_keywords = ["delete", "remove", "erase", "clear"]
        receive_messages_keywords = ["receive", "get", "read"]
        send_message_keywords = ["send", "post", "write", "create"]

        delete_message_count = 0
        receive_messages_count = 0
        send_message_count = 0

        for token in doc:
            if token.lemma_.lower() in delete_message_keywords:
                delete_message_count += 1
            elif token.lemma_.lower() in receive_messages_keywords:
                receive_messages_count += 1
            elif token.lemma_.lower() in send_message_keywords:
                send_message_count += 1

        if delete_message_count > receive_messages_count and delete_message_count > send_message_count:
            return "delete_message_in_nextcloud_talk_group"
        elif receive_messages_count > delete_message_count and receive_messages_count > send_message_count:
            return "receive_messages_of_nextcloud_talk_group"
        elif send_message_count > delete_message_count and send_message_count > receive_messages_count:
            return "send_message_to_nextcloud_talk_group"
        else:
            return "unknown"

    def classify_activity_method(self, doc):
        """
        Classifies user input related to activity by identifying whether the user wants to see the last activities or search for a specific activity.

        :param doc: A spacy Doc object containing the user input
        :type doc: spacy.tokens.doc.Doc

        :return: Returns a tuple containing a string that represents the user intent and the search query (if applicable), or "unknown" if the user intent cannot be determined.
        :rtype: tuple(str, str) or str
        """
        get_last_activities_keywords = [
            "last", "recent", "latest", "show", "get", "see"]
        search_last_activities_keywords = [
            "search", "find", "lookup", "seek", "where"]

        search_query = None
        for token in doc:
            if token.pos_ == "NOUN":
                search_query = token.text
                break
        get_last_activities_count = 0
        search_last_activities_count = 0

        for token in doc:
            if token.lemma_.lower() in get_last_activities_keywords:
                get_last_activities_count += 1
            elif token.lemma_.lower() in search_last_activities_keywords:
                search_last_activities_count += 1

        if get_last_activities_count > search_last_activities_count:
            return "get_last_activities"
        elif search_last_activities_count > get_last_activities_count:
            return "search_last_activities", search_query
        else:
            return "unknown"

    def classify_file_method(self, doc):
        """
        Classifies user input related to files by identifying whether the user wants to delete a remote file, list files in a Nextcloud folder, or send a local file to a Nextcloud folder.

        :param doc: A spacy Doc object containing the user input
        :type doc: spacy.tokens.doc.Doc

        :return: Returns a string that represents the user intent, or "unknown" if the user intent cannot be determined.
        :rtype: str
        """
        delete_remote_file_in_nextcloud_keywords = [
            "delete", "remove", "remote", "file", "files"]
        list_files_in_nextcloud_folder_keywords = [
            "list", "show", "files", "file", "folders", "folder"]
        send_local_file_to_nextcloud_folder_keywords = [
            "create", "send", "upload", "local", "file", "files", "folder"]
        delete_remote_file_in_nextcloud_count = 0
        list_files_in_nextcloud_folder_count = 0
        send_local_file_to_nextcloud_folder_count = 0

        for token in doc:
            if token.lemma_.lower() in delete_remote_file_in_nextcloud_keywords:
                delete_remote_file_in_nextcloud_count += 1
            elif token.lemma_.lower() in list_files_in_nextcloud_folder_keywords:
                list_files_in_nextcloud_folder_count += 1
            elif token.lemma_.lower() in send_local_file_to_nextcloud_folder_keywords:
                send_local_file_to_nextcloud_folder_count += 1

        if delete_remote_file_in_nextcloud_count > list_files_in_nextcloud_folder_count and delete_remote_file_in_nextcloud_count > send_local_file_to_nextcloud_folder_count:
            return "delete_remote_file_in_nextcloud"
        elif list_files_in_nextcloud_folder_count > delete_remote_file_in_nextcloud_count and list_files_in_nextcloud_folder_count > send_local_file_to_nextcloud_folder_count:
            return "list_files_in_nextcloud_folder"
        elif send_local_file_to_nextcloud_folder_count > delete_remote_file_in_nextcloud_count and send_local_file_to_nextcloud_folder_count > list_files_in_nextcloud_folder_count:
            return "send_local_file_to_nextcloud_folder"
        else:
            return "unknown"

    def classify_meeting_method(self, doc):
        """
        Classifies user input related to meetings by identifying whether the user wants to create a new room or delete an existing room.

        :param doc: A spacy Doc object containing the user input
        :type doc: spacy.tokens.doc.Doc

        :return: Returns a string that represents the user intent, or "unknown" if the user intent cannot be determined.
        :rtype: str
        """
        create_room_keywords = ["create", "set up", "start"]
        delete_room_keywords = ["delete", "remove", "end", "stop"]
        create_room_count = 0
        delete_room_count = 0

        for token in doc:
            if token.lemma_.lower() in create_room_keywords:
                create_room_count += 1
            elif token.lemma_.lower() in delete_room_keywords:
                delete_room_count += 1

        if create_room_count > delete_room_count:
            return "create_room"
        elif delete_room_count > create_room_count:
            return "delete_room"
        else:
            return "unknown"

    def classify_search_method(self, doc):
        """
        Classifies user input related to search by identifying the search category based on keywords present in the input.

        :param doc: A spacy Doc object containing the user input
        :type doc: spacy.tokens.doc.Doc

        :return: Returns a tuple containing a string that represents the search category and the search query (if applicable), or "unknown" if the search category cannot be determined.
        :rtype: tuple(str, str) or str
        """
        search_settings = ["settings_apps", "setting", "settings"]
        search_fulltext = ["fulltextsearch"]
        search_files = ["file", "files"]
        search_systemtags = ["systemtags", "tags", "tag"]
        search_comments = ["comments", "comment"]
        search_contacts = ["contact", "contacts"]
        search_talk = [
            "chat",
            "messages",
            "talk",
            "talk-message",
            "talk-conversations",
            "talk-message-current"]
        search_mail = ["mail", "mails", "e-mail", "e-mails"]
        search_calendar = ["calendar"]
        search_task = ["task", "tasks"]
        settings_score = 0
        fulltext_score = 0
        files_score = 0
        systemtags_score = 0
        comments_score = 0
        contacts_score = 0
        talk_score = 0
        mail_score = 0
        calendar_score = 0
        task_score = 0
        for token in doc:
            if token.text.lower() in search_settings:
                settings_score += 1
            if token.text.lower() in search_fulltext:
                fulltext_score += 1
            if token.text.lower() in search_files:
                files_score += 1
            if token.text.lower() in search_systemtags:
                systemtags_score += 1
            if token.text.lower() in search_comments:
                comments_score += 1
            if token.text.lower() in search_contacts:
                contacts_score += 1
            if token.text.lower() in search_talk:
                talk_score += 1
            if token.text.lower() in search_mail:
                mail_score += 1
            if token.text.lower() in search_calendar:
                calendar_score += 1
            if token.text.lower() in search_task:
                task_score += 1

        search_query = None
        for token in doc:
            if token.pos_ == "NOUN":
                search_query = token.text
                break

        max_score = max(
            settings_score,
            fulltext_score,
            files_score,
            systemtags_score,
            comments_score,
            contacts_score,
            talk_score,
            mail_score,
            calendar_score,
            task_score)

        if max_score == settings_score:
            return "settings", search_query
        elif max_score == fulltext_score:
            return "fulltext", search_query
        elif max_score == files_score:
            return "files", search_query
        elif max_score == systemtags_score:
            return "systemtags", search_query
        elif max_score == comments_score:
            return "comments", search_query
        elif max_score == contacts_score:
            return "contacts", search_query
        elif max_score == talk_score:
            return "talk", search_query
        elif max_score == mail_score:
            return "mail", search_query
        elif max_score == calendar_score:
            return "calendar", search_query
        elif max_score == task_score:
            return "task", search_query
        else:
            return "unknown"

    def classify_calendar_method(self, doc):
        """
        Classifies the user's intention related to the calendar module based on the input text.
        :param doc: A processed text using SpaCy library.
        :return: A tuple with two elements: the first is a string indicating the method name and the second is either None or a
                search query, depending on the method.
        """
        add_event_keywords = ["add", "create", "schedule"]
        get_calendars_keywords = ["get", "list", "view", "show"]
        list_events_keywords = ["list", "view", "show", "display"]
        search_event_keywords = ["search", "find", "look for", "locate"]

        verbs = [token.text.lower() for token in doc if token.pos_ == "VERB"]
        search_query = None
        for token in doc:
            if token.pos_ == "NOUN":
                search_query = token.text
                break

        if any(keyword in verbs for keyword in add_event_keywords):
            return "add_event", None
        elif any(keyword in verbs for keyword in get_calendars_keywords):
            return "get_calendars", None
        elif any(keyword in verbs for keyword in list_events_keywords):
            return "list_events", None
        elif any(keyword in verbs for keyword in search_event_keywords):
            return "search_event", search_query
        else:
            return None

    def nlpcheck(self, user_input):
        """
        Checks the user's input text and classifies their intention based on the keywords and syntax used.
        :param user_input: The user's input text to be processed.
        :return: A tuple with three elements: the first is a string indicating the module name, the second is a string
                indicating the method name, and the third is either None or a search query, depending on the method.
        """
        doc = self.nlp(user_input)

        contains_poll_keyword = any(
            token.lemma_.lower() in [
                "poll", "polls"] for token in doc)
        contains_user_keyword = any(
            token.lemma_.lower() in [
                "user", "users"] for token in doc)
        contains_message_keyword = any(
            token.lemma_.lower() in [
                "message", "messages"] for token in doc)
        contains_activity_keyword = any(
            token.lemma_.lower() in [
                "activity", "activities"] for token in doc)
        contains_meeting_keyword = any(
            token.lemma_.lower() in [
                "meeting", "meetings"] for token in doc)
        contains_file_keyword = any(
            token.lemma_.lower() in [
                "file", "files"] for token in doc)
        contains_search_keyword = any(
            token.lemma_.lower() in [
                "search for",
                "find",
                "seek"] for token in doc)
        contains_calendar_keyword = any(
            token.lemma_.lower() in [
                "calendar", "calendars"] for token in doc)

        if contains_poll_keyword:
            poll_method = self.classify_poll_method(doc)
            if poll_method == "close_poll":
                print("User intends to close a poll.")
                return ("poll", "close_poll", None)
            elif poll_method == "create_poll":
                print("User intends to create a poll.")
            elif poll_method == "get_poll_result":
                print("User intends to get poll results.")
            else:
                print("Unable to determine the user's intention.")
        elif contains_user_keyword:
            user_method = self.classify_user_method(doc)
            if user_method == "get_preferred_language":
                print("User intends to get preferred language.")
                return ("user", "get_preferred_language", None)
            elif user_method == "get_quota":
                print("User intends to get quota.")
                return ("user", "get_quota", None)
            elif user_method == "test_user_login":
                print("User intends to test user login.")
                return ("user", "test_user_login", None)
            else:
                print("Unable to determine the user's intention.")
        elif contains_message_keyword:
            message_method = self.classify_message_method(doc)
            if message_method == "delete_message_in_nextcloud_talk_group":
                print("User intends to delete a message in Nextcloud Talk group.")
                return (
                    "messages",
                    "delete_message_in_nextcloud_talk_group",
                    None)
            elif message_method == "receive_messages_of_nextcloud_talk_group":
                print("User intends to receive messages from Nextcloud Talk group.")
                return (
                    "messages",
                    "receive_messages_of_nextcloud_talk_group",
                    None)
            elif message_method == "send_message_to_nextcloud_talk_group":
                print("User intends to send a message to Nextcloud Talk group.")
                return (
                    "messages",
                    "send_message_to_nextcloud_talk_group",
                    None)
            else:
                print("Unable to determine the user's intention.")
        elif contains_activity_keyword:
            activity_method, search_query = self.classify_activity_method(doc)
            if activity_method == "get_last_activities":
                print("User intends to get last activities.")
                return ("activities", "get_last_activities", None)
            elif activity_method == "search_last_activities":
                print("User intends to search for last activities.")
                return ("activities", "get_last_activities", search_query)
            else:
                print("Unable to determine the user's intention.")
        elif contains_file_keyword:
            file_method = self.classify_file_method(doc)
            if file_method == "delete_remote_file_in_nextcloud":
                print("User intends to delete a remote file in Nextcloud.")
            elif file_method == "list_files_in_nextcloud_folder":
                print("User intends to list files in a Nextcloud folder.")
            elif file_method == "send_local_file_to_nextcloud_folder":
                print("User intends to send a local file to a Nextcloud folder.")
            else:
                print("Unable to determine the user's intention.")
        elif contains_meeting_keyword:
            meeting_method = self.classify_meeting_method(doc)
            if meeting_method == "create_room":
                print("User intends to create a meeting room.")
                return ("meeting", "create_room", None)
            elif meeting_method == "delete_room":
                print("User intends to delete a meeting room.")
                return ("meeting", "delete_room", None)
            else:
                print("Unable to determine the user's intention.")
        elif contains_search_keyword:
            search_provider, search_query = self.classify_search_method(doc)
            if search_provider == "settings":
                print(
                    "User intends to search for settings with the query: ",
                    search_query)
                return ("search", "search", "settings " + search_query)
            elif search_provider == "fulltext":
                print(
                    "User intends to perform a fulltext search with the query: ",
                    search_query)
                return ("search", "search", "fulltext " + search_query)
            elif search_provider == "files":
                print(
                    "User intends to search for files with the query: ",
                    search_query)
                return ("search", "search", "files " + search_query)
            elif search_provider == "systemtags":
                print(
                    "User intends to search for system tags with the query: ",
                    search_query)
                return ("search", "search", "systemtags " + search_query)
            elif search_provider == "comments":
                print(
                    "User intends to search for comments with the query: ",
                    search_query)
                return ("search", "search", "comments " + search_query)
            elif search_provider == "contacts":
                print(
                    "User intends to search for contacts with the query: ",
                    search_query)
                return ("search", "search", "contacts " + search_query)
            elif search_provider == "talk":
                print(
                    "User intends to search for chat messages with the query: ",
                    search_query)
                return ("search", "search", "talk-message " + search_query)
            elif search_provider == "mail":
                print(
                    "User intends to search for mails with the query: ",
                    search_query)
                return ("search", "search", "mail " + search_query)
            elif search_provider == "calendar":
                print(
                    "User intends to search for events on the calendar with the query: ",
                    search_query)
                return ("search", "search", "calendar " + search_query)
            elif search_provider == "task":
                print(
                    "User intends to search for tasks with the query: ",
                    search_query)
                return ("search", "search", "tasks " + search_query)
            else:
                print(
                    f"Unable to determine the user's intention in search. {search_query}")
        elif contains_calendar_keyword:
            calendar_method, search_query = self.classify_calendar_method(doc)
            if calendar_method == "add_event":
                print("User intends to add an event to the calendar.")
                return ("calendar", "add_event", None)
            elif calendar_method == "get_calendars":
                print("User intends to retrieve a list of calendars.")
                return ("calendar", "get_calendars", None)
            elif calendar_method == "list_events":
                print("User intends to list events from the calendar.")
                return ("calendar", "get_calendars", None)
            elif calendar_method == "search_event":
                print("User intends to search for an event in the calendar.")
                return ("calendar", "search_event", search_query)
            else:
                print("Unable to determine the user's intention.")

        else:
            print("The text does not contain 'activity' or 'activities'.")


class NextcloudCommands:
    """
    A class for printing the docstrings of classes and methods from specified modules.

    :param input_name: The name of the input used to map to a module.
    :param base_url: The base URL of your Nextcloud instance (optional).
    :param username: Your Nextcloud username (optional).
    :param password: Your Nextcloud password (optional).
    :param room_name: The name of the Nextcloud Talk room (optional).
    """

    def __init__(self, input_name=None):
        self.input_name = input_name
        if input_name:
            self.module_name = self.module_name = self.map_input_to_module(
                input_name)
            self.load_module()
        else:
            self.module_name = None
        self.bot = nextcloud_talk_bot.NextcloudTalkBot()
        if hasattr(self.bot, "NEXTCLOUD_URL"):
            self.url = self.bot.NEXTCLOUD_URL
            self.username = self.bot.USERNAME
            self.password = self.bot.PASSWORD
            self.room_name = self.bot.ROOM_NAME
            self.room_token = self.bot.ROOM_TOKEN
        else:
            FirstRunSetup.first_run()

    def map_input_to_module(self, input_name):
        mapping = {
            "activities": "nextcloud_activities",
            "user": "nextcloud_user",
            "file": "nextcloud_file_operations",
            "meeting": "nextcloud_meeting",
            "messages": "nextcloud_messages",
            "poll": "nextcloud_poll",
            "requests": "nextcloud_requests",
            "extractor": "nextcloud_talk_extractor",
            "talkbot": "Nextcloudtalkbot",
            "search": "nextcloud_search",
            "calendar": "nextcloud_calendar",
        }
        return mapping.get(input_name, input_name)

    def load_module(self):
        module_name = self.module_name
        self.module = importlib.import_module(
            f"nextcloud_talk_bot.{self.module_name}")

    def get_first_class(self):
        for name, obj in inspect.getmembers(self.module):
            if inspect.isclass(obj) and self.module_name in obj.__module__:
                return obj
        return None

    def print_first_class_docstring(self):
        cls = self.get_first_class()
        if cls:
            docstring = inspect.getdoc(cls)
            if docstring:
                print(f"{docstring}\n")
            else:
                print(f"{cls.__name__} has no docstring.")
        else:
            print(f"No classes found in module {self.module_name}.")

    def print_method_docstring(self, method_name):
        cls = self.get_first_class()
        if cls:
            method = getattr(cls, method_name, None)
            if method:
                docstring = inspect.getdoc(method)
                if docstring:
                    print(f"{docstring}\n")
                else:
                    print(f"Method '{method_name}' has no docstring.")
            else:
                print(
                    f"Method '{method_name}' not found in class '{cls.__name__}'.")
        else:
            print(f"No classes found in module {self.module_name}.")

    def call_class_method(self, method_name, *args, **kwargs):
        unpacked_args = []
        for arg in args:
            if arg.startswith('[') and arg.endswith(']'):
                parsed_arg = ast.literal_eval(arg)
                if isinstance(parsed_arg, list):
                    unpacked_args.append(parsed_arg)
                else:
                    unpacked_args.append(arg)
            else:
                unpacked_args.append(arg)
        cls = self.get_first_class()
        if cls:
            instance = getattr(self.bot, self.input_name)
            method = getattr(instance, method_name, None)
            if method:
                if args:
                    print(*unpacked_args)
                    return method(*unpacked_args)
                else:
                    return method()
            else:
                print(
                    f"Method '{method_name}' not found in class '{cls.__name__}'.")
        else:
            print(f"No classes found in module {self.module_name}.")

    def print_available_classes_and_methods(self):
        print(f"Classes and methods in module {self.module_name}:\n")
        for name, obj in inspect.getmembers(self.module):
            if inspect.isclass(obj) and self.module_name in obj.__module__:
                print(f"Class: {name}")
                for method_name, method in inspect.getmembers(
                        obj, predicate=inspect.isfunction):
                    print(f"  - Method: {method_name}")

    def print_method_parameters(self, method_name):
        cls = self.get_first_class()
        if cls:
            method = getattr(cls, method_name, None)
            if method:
                signature = inspect.signature(method)
                print(f"Parameters for function '{method_name}':\n{signature}")
            else:
                print(
                    f"Function '{method_name}' not found in class '{cls.__name__}'.")
        else:
            print(f"No classes found in module {self.module_name}.")

    def print_available_classes(self):
        classes = [
            "activities",
            "calendar",
            "user",
            "file",
            "meeting",
            "messages",
            "poll",
            "search",
            "extractor"]
        print("Available options:")
        for options in classes:
            print(options)
        print("type options --list to get available functions")

    def lowercase_or_none(self, x):
        if x is not None:
            return x.lower()
        else:
            return None


if __name__ == "__main__":
    nc = NextcloudCommands()
    parser = argparse.ArgumentParser(
        description="Call Nextcloud Commands via NextcloudTalkBot Framework",
        add_help=False)
    parser.add_argument(
        "input_name",
        type=nc.lowercase_or_none,
        help="Option name. Type --list to get all options.",
        nargs="?",
        default=None)

    parser.add_argument(
        "--function",
        "-f",
        type=nc.lowercase_or_none,
        dest="method_name",
        default=None,
        help="Function to call. Type option --list to get all parameters or option --help for help")

    parser.add_argument(
        "--args",
        "-a",
        nargs="*",
        type=nc.lowercase_or_none,
        default=[],
        help="Arguments to pass to the function.")

    parser.add_argument(
        "--help",
        "-h",
        dest="help_flag",
        action="store_true",
        help="Print help.")

    parser.add_argument(
        "--list",
        "-l",
        dest="list_flag",
        action="store_true",
        help="List available options or functions.")

    parser.add_argument(
        "--setup",
        "-s",
        dest="setup_flag",
        action="store_true",
        help="First Run setup")

    args, unknown = parser.parse_known_args()

    if unknown:
        nlp = NLPCommands()
        nlpInput = (args.input_name, ' '.join(unknown))
        input_name, method_name, nargs = nlp.nlpcheck(str(nlpInput))
        args.input_name = input_name
        args.method_name = method_name

        print(args.input_name)
        print(args.method_name)
    # args = parser.parse_known_args()

    print(args)

    if args.input_name is not None:

        nextcloud_command = NextcloudCommands(args.input_name)
        if args.help_flag:
            if args.method_name:
                nextcloud_command.print_method_docstring(args.method_name)
            else:
                nextcloud_command.print_first_class_docstring()
        elif args.method_name and args.list_flag:
            nextcloud_command.print_method_parameters(args.method_name)
        elif args.method_name:
            result = nextcloud_command.call_class_method(
                args.method_name, *args.args)
            if result:
                print(f"Result: {result}")
        elif args.list_flag:
            nextcloud_command.print_available_classes_and_methods()
        else:
            parser.print_help()

    elif args.input_name is None:
        if args.list_flag:
            nextcloud_command = NextcloudCommands(args.input_name)
            nextcloud_command.print_available_classes()
        elif args.setup_flag:
            nextcloud_command = FirstSetup()
            nextcloud_command.start_setup()
        else:
            parser.print_help()
