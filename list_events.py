import datetime
import pytz
from cal_setup import get_calendar_service


def list_events(info, freebusy=False, display=False):
    service = get_calendar_service()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting List o 10 events')
    events_result = service.events().list(calendarId=info['calendar_id'],
                                          timeMin=now,
                                          maxResults=info['max_events'],
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if display:
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    if freebusy:
        # This event should be returned by freebusy
        # tz = pytz.timezone('US/Central')
        tz = pytz.timezone('Europe/Kiev')
        the_datetime = tz.localize(datetime.datetime(2021, 4, 2, 0))
        the_datetime2 = tz.localize(datetime.datetime(2021, 4, 4, 8))
        body = {
          "timeMin": the_datetime.isoformat(),
          "timeMax": the_datetime2.isoformat(),
          "timeZone": 'US/Central',
          "items": [{"id": 'my.email@gmail.com'}]
        }

        eventsResult = service.freebusy().query(body=body).execute()
        cal_dict = eventsResult[u'calendars']
        for cal_name in cal_dict:
            print(cal_name, cal_dict[cal_name])
        return eventsResult
    else:
        return events
