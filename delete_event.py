from cal_setup import get_calendar_service


def delete_event(info):
    # Delete the event
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId=info['calendar_id'],
            eventId='4qnt0okd4dmr0hik3mh073qnls',
        ).execute()
        print("Event deleted")
        return True
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")
        return False
