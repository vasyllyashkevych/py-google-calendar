from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def create_event(info, new_start, new_end):
    # creates one hour event tomorrow 10 AM IST
    service = get_calendar_service()

    # d = datetime.now().date()
    # tomorrow = datetime(d.year, d.month, d.day, 17) + timedelta(days=1)
    # start = tomorrow.isoformat()
    # end = (tomorrow + timedelta(hours=info['duration'])).isoformat()

    event_result = service.events().insert(calendarId=info['calendar_id'],
                                           body={
                                               "summary": info['event'],
                                               "description": 'This is a tutorial example of automating google calendar with python',
                                               "start": {"dateTime": new_start, "timeZone": 'Europe/Kiev'},
                                               "end": {"dateTime": new_end, "timeZone": 'Europe/Kiev'},
                                           }
                                           ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])
