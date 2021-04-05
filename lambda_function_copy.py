import json
from random import choice
from string import ascii_uppercase
from datetime import date, datetime, timedelta
from list_events import list_events as le
from create_event import create_event as ce
from workalendar.europe import Ukraine
# import delete_event
import dateutil.parser

calendar_id = "7f65bpo8mq6csbfq3v15e2r7mk@group.calendar.google.com"
calendar = Ukraine()


def in_time(tm):
    tmp = tm.split(":")
    return [int(tmp[0]), int(tmp[1])]


def get_day_name(day):
    # name = datetime.strptime(day, '%Y-%m-%dT%H:%M:%S')
    name = datetime.strptime(day, '%Y-%m-%d')
    return '{0:%A}'.format(name)


def check_timeslot(start, end, events):
    print(24, start, end)
    for k, v in events.items():
        print(26, k, v)
        event_start = in_time(v['start'])
        event_end = in_time(v['end'])
        if start[0] > event_end[0]:
            continue
        elif start[0] == event_end[0]:
            continue
        elif end[0] == event_start[0]:
            continue
        elif start[0] < event_start[0] and end[0] < event_start[0]:
            continue
        elif start[0] < event_start[0] and end[0] == event_start[0] and end[1] < event_start[1]:
            continue
        else:
            return True

    return False


def parse_events(events):
    parsed = {}
    for event in events:
        dt_start = dateutil.parser.parse(event['start']['dateTime']).strftime('%H:%M')
        dt_end = dateutil.parser.parse(event['end']['dateTime']).strftime('%H:%M')
        parsed[event['id']] = {'start': dt_start, 'end': dt_end}
        # print(dt_start)
        # print(dt_end)
    return parsed


def lambda_handler(event, context):
    print(event)
# def lambda_handler(context):
    info = {"calendar_id": calendar_id,
            'max_events': 50,
            'duration': 1,
            'working_start': 8,
            'working_end': 19,
            'userId': event['userId'],
            'bot': event['bot']
            }

    new_day_name = event['currentIntent']['slots']['BookingDayOfWeek']
    new_day = event['currentIntent']['slots']['PickupDate']
    new_start = event['currentIntent']['slots']['PickupTime']

    start_hours, start_mins = new_start.split(":")

    new_end = str(int(start_hours)+1) + start_mins

    # get name of day
    # new_day_name = get_day_name(new_day)
    # print("Day is: ", day)

    day_year, day_month, day_day = new_day.split("-")

    dt_start = dateutil.parser.parse(new_start).strftime('%H:%M')
    dt_end = dateutil.parser.parse(new_end).strftime('%H:%M')

    dt_start_time = in_time(dt_start)
    dt_end_time = in_time(dt_end)

    # check if working day
    if not calendar.is_working_day(date(int(day_year), int(day_month), int(day_day))):
        print(new_day_name + ' is not a working day, please, choose another day !')
        return {
            'statusCode': 200,
            'body': json.dumps('It is not a working day, please, choose another day !')
        }

    # check if time is correct
    if dt_start_time[0] < info['working_start'] or dt_end_time[0] > info['working_end']:
        print('Working hours are incorrect !')
        return {
            'statusCode': 200,
            'body': json.dumps('Working hours are incorrect !')
        }

    # parse list of events
    events = parse_events(le(info))
    # print(22, events)

    # check if free slots
    if check_timeslot(dt_start_time, dt_end_time, events):
        print('Busy')
        return {
            'statusCode': 200,
            'body': json.dumps('Busy')
        }
    else:
        info['event'] = ''.join(choice(ascii_uppercase) for i in range(12))
        ce(info, new_start, new_end)
        return {
            'statusCode': 200,
            'body': json.dumps('The appointment is scheduled!'),
            'event_id': info['event']
        }

#
# # TEST
# d = datetime.now().date()
# tomorrow = datetime(d.year, d.month, d.day, 19) + timedelta(days=2)
#
# start = tomorrow.isoformat()
# end = (tomorrow + timedelta(hours=1)).isoformat()
#
# lambda_handler({'start': start, 'end': end, 'event': "Birthday"})
