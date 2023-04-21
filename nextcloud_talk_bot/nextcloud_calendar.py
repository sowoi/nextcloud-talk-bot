import caldav
import logging
from caldav.elements import dav, cdav
from icalendar import Event, Calendar
import vobject
from datetime import datetime, timedelta
from dateutil import tz
from .i18n import _


class NextcloudCalendar:
    """
    Initialize the NextcloudCalendar class.

    :param url: The URL to the Nextcloud CalDAV server.
    :param username: The username for authentication.
    :param password: The password for authentication.
    """

    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.password = password
        self.username = username
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def calendar_init(self):
        self.caldav_url = f"{self.base_url}/remote.php/dav/"
        self.client = caldav.DAVClient(
            self.caldav_url,
            username=self.username,
            password=self.password)
        self.principal = caldav.Principal(self.client)
        self.calendars = self.principal.calendars()

    def get_calendars(self, calendar_name=None):
        """
        Get a list of calendars or a specific calendar by its name.

        :param calendar_name: The name of the calendar to search for (optional).
        :return: If a calendar_name is specified, returns the matching calendar; otherwise, returns a list of all available calendars.
        """
        self.calendar_init()
        for calendar in self.calendars:
            if calendar_name is not None and calendar_name == calendar.name:
                return calendar
        calendar_names = []
        for key in self.calendars.items():
            calendar_names.append(key)
            self.logger.debug(f"Calendar found: {calendar}")
        self.logger.info(
            f"Getting calendar(s) with name '{calendar_name if calendar_name else 'all'}'")
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
        calendar = self.get_calendars(calendar_name)

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
        self.logger.info(
            f"Listed events from calendar '{calendar_name}' within {days} days")
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
        calendar = self.get_calendars(self, calendar_name)
        event = Event()
        date_format = "%Y-%m-%d %H:%M"
        start_time = datetime.strptime(start, date_format)
        end_time = datetime.strptime(end, date_format)
        event.add("summary", summary)
        event.add("dtstart", start_time)
        event.add("dtend", end_time)
        calendar_event = Calendar()
        calendar_event.add_component(event)
        calendar.add_event(calendar_event.to_ical())
        self.logger.info(
            f"Added event '{summary}' to calendar '{calendar_name}'")
        return f"Added event {summary}"

    def search_event(self, calendar_name, summary):
        """
        Search for an event in the specified calendar by its summary.

        :param calendar_name: The name of the calendar to search for events.
        :param summary: The summary of the event to search for.
        :return: The UID of the selected event or None if not found.
        """
        events_found = self.list_events(
            calendar_name, days=30)
        matching_uids = []
        matching_events = {}

        for uid, event_data in events_found.items():
            search_summary = event_data[0]
            if summary in search_summary:
                matching_uids.append(uid)
                matching_events[uid] = event_data
        self.logger.info(
            f"Searched for event '{summary}' in calendar '{calendar_name}'")
        return matching_events
