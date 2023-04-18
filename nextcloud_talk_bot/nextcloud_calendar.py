import caldav
from caldav.elements import dav, cdav
from icalendar import Event, Calendar
import vobject
from datetime import datetime, timedelta
from dateutil import tz
import gettext

locale_path = "../locales"
supported_languages = ["de", "fr", "es"]
translation = gettext.translation("NextcloudTalkBot", localedir=locale_path, languages=supported_languages, fallback=True)
_ = translation.gettext


class NextcloudCalendar:
    def __init__(self, url, username, password):
        self.client = caldav.DAVClient(
            url=url, username=username, password=password)
        self.principal = self.client.principal()
        self.calendars = self.principal.calendars()
        """
        Initialize the NextcloudCalendar class.

        :param url: The URL to the Nextcloud CalDAV server.
        :param username: The username for authentication.
        :param password: The password for authentication.
        """

    def get_calendars(self, calendar_name=None):
        """
        Get a list of calendars or a specific calendar by its name.

        :param calendar_name: The name of the calendar to search for (optional).
        :return: If a calendar_name is specified, returns the matching calendar; otherwise, returns a list of all available calendars.
        """
        for calendar in self.calendars:
            print(calendar)
            if calendar_name is not None and calendar_name == calendar.name:
                return calendar
        else:
            calendar_names = []
            for key, value in calendars.items():
                calendar_names.append(key)
            return "Found:", calendar_names

    def list_events(self, calendar_name, days=1):
        """
        List events from a specific calendar within a given number of days.

        :param calendar_name: The name of the calendar to search for events.
        :param days: The number of days to search for events (default: 1).
        :return: A dictionary of found events with their UID as the key.
        """
        local_tz = tz.tzlocal()
        start_date = datetime.now()
        end_date = start_date + timedelta(days=days)
        calendar = NextcloudCalendar.get_calendars(self, calendar_name)

        events = calendar.search(
            start=start_date,
            end=end_date,
            event=True,
            expand=True)
        date_format = "%Y-%m-%d %H:%M"
        events_found = {}

        for event in events:
            data = event.data
            cal = vobject.readOne(data)
            if cal.name == "VCALENDAR":
                for event in cal.vevent_list:
                    summary = 'No summary available'
                    location = 'No location available'
                    start = datetime.strptime(
                        event.dtstart.value.strftime(date_format), date_format)

                    event_dtstart_value = start.replace(tzinfo=tz.UTC)
                    local_start_time = event_dtstart_value.astimezone(local_tz)
                    formatted_start_time = local_start_time.strftime(
                        "%Y-%m-%d %H:%M %Z")

                    end = datetime.strptime(
                        event.dtend.value.strftime(date_format), date_format)

                    event_dtend_value = end.replace(tzinfo=tz.UTC)
                    local_end_time = event_dtend_value.astimezone(local_tz)
                    formatted_end_time = local_end_time.strftime(
                        "%Y-%m-%d %H:%M %Z")

                    try:
                        if hasattr(event.summary, 'value'):
                            summary = event.summary.value
                        if hasattr(event.location, 'value'):
                            location = event.location.value
                    except AttributeError:
                        pass

                    events_found[event.uid.value] = summary, formatted_start_time, formatted_end_time, location
        return (events_found)

    def add_event(self, calendar_name, summary, start, end, location=None):
        """
        Add an event to the specified calendar.

        :param calendar_name: The name of the calendar to add the event to.
        :param summary: The summary of the event.
        :param start: The start time of the event in the format "YYYY-MM-DD HH:MM".
        :param end: The end time of the event in the format "YYYY-MM-DD HH:MM".
        :param location: The location of the event (optional).
        :return: A string indicating that the event has been added.
        """
        local_tz = tz.tzlocal()
        calendar = NextcloudCalendar.get_calendars(self, calendar_name)
        event = Event()
        date_format = "%Y-%m-%d %H:%M"
        start_time = datetime.strptime(start, date_format)
        end_time = datetime.strptime(end, date_format)
        event.add("summary", summary)
        event.add("dtstart", start_time)
        event.add("dtend", end_time)
        calendar_event = Calendar()
        calendar_event.add_component(event)
        new_event = calendar.add_event(calendar_event.to_ical())
        return f"Added event {summary}"

    def search_event(self, calendar_name, summary):
        """
        Search for an event in the specified calendar by its summary.

        :param calendar_name: The name of the calendar to search for events.
        :param summary: The summary of the event to search for.
        :return: The UID of the selected event or None if not found.
        """
        events_found = NextcloudCalendar.list_events(
            self, calendar_name, days=30, uid=1)
        matching_uids = []
        matching_events = {}

        for uid, event_data in events_found.items():
            search_summary = event_data[0]
            if summary == search_summary:
                matching_uids.append(uid)
                matching_events[uid] = event_data
        if matching_events:
            event_list = list(matching_events.items())
            for index, (uid, event_data) in enumerate(event_list, start=1):
                print(f"{index}: {event_data}")

            while True:
                try:
                    choice = int(input(_("Please choose event by number: ")))
                    if 1 <= choice <= len(event_list):
                        selected_uid = event_list[choice - 1][0]
                        return selected_uid
                        break
                    else:
                        print(_("Invalid entry."))
                except ValueError:
                    print(_("Please enter a number."))
