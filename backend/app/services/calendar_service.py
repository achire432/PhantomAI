from sqlalchemy.orm import Session
from backend.app.models.calendar import CalendarEvent
from backend.app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate
from datetime import datetime

def create_event(db: Session, user_id: int, event_data: CalendarEventCreate) -> CalendarEvent:
    event = CalendarEvent(
        user_id=user_id,
        title=event_data.title,
        description=event_data.description,
        location=event_data.location,
        start_time=event_data.start_time,
        end_time=event_data.end_time,
        all_day=event_data.all_day
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_events(db: Session, user_id: int, start: datetime = None, end: datetime = None) -> list:
    query = db.query(CalendarEvent).filter(CalendarEvent.user_id == user_id)
    if start:
        query = query.filter(CalendarEvent.start_time >= start)
    if end:
        query = query.filter(CalendarEvent.end_time <= end)
    return query.order_by(CalendarEvent.start_time).all()

def get_event(db: Session, event_id: int, user_id: int) -> CalendarEvent:
    return db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.user_id == user_id
    ).first()

def update_event(db: Session, event_id: int, user_id: int, event_data: CalendarEventUpdate) -> CalendarEvent:
    event = get_event(db, event_id, user_id)
    if not event:
        return None
    if event_data.title is not None:
        event.title = event_data.title
    if event_data.description is not None:
        event.description = event_data.description
    if event_data.location is not None:
        event.location = event_data.location
    if event_data.start_time is not None:
        event.start_time = event_data.start_time
    if event_data.end_time is not None:
        event.end_time = event_data.end_time
    if event_data.all_day is not None:
        event.all_day = event_data.all_day
    event.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int, user_id: int) -> bool:
    event = get_event(db, event_id, user_id)
    if not event:
        return False
    db.delete(event)
    db.commit()
    return True