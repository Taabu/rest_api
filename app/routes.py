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

# Search sports
@sports_routes.route('/sports', methods=['GET'])
def get_sports():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM sports")
            sports = cursor.fetchall()

    return jsonify(sports), 200

# Update sport
@sports_routes.route('/sports/<int:id>', methods=['PUT'])
def update_sport(id):
    sport_data = request.json
    sport = Sport(**sport_data)

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE sports
                SET name = %s, slug = %s, active = %s
                WHERE id = %s
            """, (sport.name, sport.slug, sport.active, id))
            conn.commit()

    return jsonify({'message': 'Sport updated successfully'}), 200

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

# Search events
@events_routes.route('/events', methods=['GET'])
def get_events():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM events")
            events = cursor.fetchall()

    return jsonify(events), 200

# Update event
@events_routes.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    event_data = request.json
    event = Event(**event_data)

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE events
                SET name = %s, slug = %s, active = %s, type = %s, sport = %s, status = %s, scheduled_start = %s, actual_start = %s
                WHERE id = %s
            """, (event.name, event.slug, event.active, event.type, event.sport.id, event.status, event.scheduled_start, event.actual_start, id))
            conn.commit()

    return jsonify({'message': 'Event updated successfully'}), 200

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

# Search selections
@selections_routes.route('/selections', methods=['GET'])
def get_selections():
    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM selections")
            selections = cursor.fetchall()

    return jsonify(selections), 200

# Update selection
@selections_routes.route('/selections/<int:id>', methods=['PUT'])
def update_selection(id):
    selection_data = request.json
    selection = Selection(**selection_data)

    with get_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE selections
                SET name = %s, event = %s, price = %s, active = %s, outcome = %s
                WHERE id = %s
            """, (selection.name, selection.event.id, selection.price, selection.active, selection.outcome, id))
            conn.commit()

    return jsonify({'message': 'Selection updated successfully'}), 200
