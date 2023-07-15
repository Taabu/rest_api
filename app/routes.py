from flask import Blueprint, jsonify, request
from models import Sport, Event, Selection
from db import get_db

# Create a Blueprint for sports routes
sports_routes = Blueprint('sports', __name__)

# Create sport
@sports_routes.route('/sports', methods=['POST'])
def create_sport():
    sport_data = request.json
    sport = Sport(**sport_data)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sports (name, slug, active)
            VALUES (%s, %s, %s)
        """, (sport.name, sport.slug, sport.active))
        conn.commit()

    return jsonify({'message': 'Sport created successfully'}), 201

# Create a Blueprint for events routes
events_routes = Blueprint('events', __name__)

# Create event
@events_routes.route('/events', methods=['POST'])
def create_event():
    event_data = request.json
    event = Event(**event_data)

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO events (name, slug, active, type, sport, status, scheduled_start, actual_start)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (event.name, event.slug, event.active, event.type, event.sport.id, event.status, event.scheduled_start, event.actual_start))
            conn.commit()

    return jsonify({'message': 'Event created successfully'}), 201


# Create a Blueprint for selections routes
selections_routes = Blueprint('selections', __name__)

# Create selection
@selections_routes.route('/selections', methods=['POST'])
def create_selection():
    selection_data = request.json
    selection = Selection(**selection_data)

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO selections (name, event, price, active, outcome)
                VALUES (%s, %s, %s, %s, %s)
            """, (selection.name, selection.event.id, selection.price, selection.active, selection.outcome))
            conn.commit()

    return jsonify({'message': 'Selection created successfully'}), 201

