import spacy

# Laden des Sprachmodells
nlp = spacy.load("en_core_web_sm")

# Textklassifikation basierend auf Keywords für Poll-Methoden
def classify_poll_method(doc):
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
    
# Textklassifikation basierend auf Keywords für User-Methoden
def classify_user_method(doc):
    get_preferred_language_keywords = ["language", "preferred", "preference"]
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


def classify_message_method(doc):
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
    
    
def classify_activity_method(doc):
    get_last_activities_keywords = ["last", "recent", "latest", "show", "get", "see"]
    search_last_activities_keywords = ["search", "find", "lookup", "seek", "where"]

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
        return "search_last_activities"
    else:
        return "unknown"
    
def classify_file_method(doc):
    delete_remote_file_in_nextcloud_keywords = ["delete", "remove", "remote", "file", "files"]
    list_files_in_nextcloud_folder_keywords = ["list", "show", "files", "file", "folders", "folder"]
    send_local_file_to_nextcloud_folder_keywords = ["create", "send", "upload", "local", "file", "files", "folder"]
    delete_remote_file_in_nextcloud_count = 0
    list_files_in_nextcloud_folder_count = 0
    send_local_file_to_nextcloud_folder_count = 0

    # Prüfen, ob ein Token im Dokument einem Keyword für eine Methode entspricht
    for token in doc:
        if token.lemma_.lower() in delete_remote_file_in_nextcloud_keywords:
            delete_remote_file_in_nextcloud_count += 1
        elif token.lemma_.lower() in list_files_in_nextcloud_folder_keywords:
            list_files_in_nextcloud_folder_count += 1
        elif token.lemma_.lower() in send_local_file_to_nextcloud_folder_keywords:
            send_local_file_to_nextcloud_folder_count += 1

    # Ermitteln der am häufigsten vorkommenden Methode
    if delete_remote_file_in_nextcloud_count > list_files_in_nextcloud_folder_count and delete_remote_file_in_nextcloud_count > send_local_file_to_nextcloud_folder_count:
        return "delete_remote_file_in_nextcloud"
    elif list_files_in_nextcloud_folder_count > delete_remote_file_in_nextcloud_count and list_files_in_nextcloud_folder_count > send_local_file_to_nextcloud_folder_count:
        return "list_files_in_nextcloud_folder"
    elif send_local_file_to_nextcloud_folder_count > delete_remote_file_in_nextcloud_count and send_local_file_to_nextcloud_folder_count > list_files_in_nextcloud_folder_count:
        return "send_local_file_to_nextcloud_folder"
    else:
        return "unknown"


def classify_meeting_method(doc):
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
    

# Benutzereingabe
user_input = input("Enter a text with 'poll'/'polls' or 'user'/'users': ")

# Verarbeiten der Benutzereingabe
doc = nlp(user_input)

# Prüfen, ob der Text das Schlüsselwort "poll"/"polls" oder "user"/"users" enthält
contains_poll_keyword = any(token.lemma_.lower() in ["poll", "polls"] for token in doc)
contains_user_keyword = any(token.lemma_.lower() in ["user", "users"] for token in doc)
contains_message_keyword = any(token.lemma_.lower() in ["message", "messages"] for token in doc)
contains_activity_keyword = any(token.lemma_.lower() in ["activity", "activities"] for token in doc)
contains_meeting_keyword = any(token.lemma_.lower() in ["meeting", "meetings"] for token in doc)
contains_file_keyword = any(token.lemma_.lower() in ["file", "files"] for token in doc)

if contains_poll_keyword:
    poll_method = classify_poll_method(doc)
if contains_poll_keyword:
    poll_method = classify_poll_method(doc)
    if poll_method == "close_poll":
        print("User intends to close a poll.")
    elif poll_method == "create_poll":
        print("User intends to create a poll.")
    elif poll_method == "get_poll_result":
        print("User intends to get poll results.")
    else:
        print("Unable to determine the user's intention.")
elif contains_user_keyword:
    user_method = classify_user_method(doc)
    if user_method == "get_preferred_language":
        print("User intends to get preferred language.")
    elif user_method == "get_quota":
        print("User intends to get quota.")
    elif user_method == "test_user_login":
        print("User intends to test user login.")
    else:
        print("Unable to determine the user's intention.")
elif contains_message_keyword:
    message_method = classify_message_method(doc)
    if message_method == "delete_message_in_nextcloud_talk_group":
        print("User intends to delete a message in Nextcloud Talk group.")
    elif message_method == "receive_messages_of_nextcloud_talk_group":
        print("User intends to receive messages from Nextcloud Talk group.")
    elif message_method == "send_message_to_nextcloud_talk_group":
        print("User intends to send a message to Nextcloud Talk group.")
    else:
        print("Unable to determine the user's intention.")
elif contains_activity_keyword:
    activity_method = classify_activity_method(doc)
    if activity_method == "get_last_activities":
        print("User intends to get last activities.")
    elif activity_method == "search_last_activities":
        print("User intends to search for last activities.")
    else:
        print("Unable to determine the user's intention.")
elif contains_file_keyword:
    file_method = classify_file_method(doc)
    if file_method == "delete_remote_file_in_nextcloud":
        print("User intends to delete a remote file in Nextcloud.")
    elif file_method == "list_files_in_nextcloud_folder":
        print("User intends to list files in a Nextcloud folder.")
    elif file_method == "send_local_file_to_nextcloud_folder":
        print("User intends to send a local file to a Nextcloud folder.")
    else:
        print("Unable to determine the user's intention.")
elif contains_meeting_keyword:
    meeting_method = classify_meeting_method(doc)
    if meeting_method == "create_room":
        print("User intends to create a meeting room.")
    elif meeting_method == "delete_room":
        print("User intends to delete a meeting room.")
    else:
        print("Unable to determine the user's intention.")
else:
    print("The text does not contain 'activity' or 'activities'.")

    
