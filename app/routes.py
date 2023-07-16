import logging
from flask import Blueprint, jsonify, request
from cache import cache
from datetime import datetime
from models import Sport, Event, Selection
from db import get_db

# Create a Blueprint for sports routes
sports_routes = Blueprint('sports', __name__)

# Create sport
@sports_routes.route('/sports', methods=['POST'])
def create_sport():
    try:
        sport_data = request.json
        sport = Sport(**sport_data)

        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sports (name, slug, active)
                VALUES (%s, %s, %s)
            """, (sport.name, sport.slug, sport.active))
            conn.commit()
        
        cache.delete('sports')

        return jsonify({'message': 'Sport created successfully'}), 201
    except Exception as e:
        logging.exception("Error creating sport:")
        return jsonify({'error': 'Failed to create sport'}), 500

# Search sport
@sports_routes.route('/sports/search', methods=['GET'])
@cache.cached(timeout=60, query_string=True, key_prefix='sports')
def search_sports():
    try:
        base_sql = """
            SELECT s.* FROM sports s 
            JOIN (
                SELECT e.sport, COUNT(*) active_events_count 
                FROM events e WHERE e.active = true GROUP BY e.sport
            ) ec ON s.id = ec.sport 
            WHERE 1=1
        """
        filters = {}
        if request.args.get('name_regex'):
            filters['name_regex'] = {
                'column': 's.name',
                'operator': 'REGEXP',
                'value': request.args.get('name_regex')
            }
        if request.args.get('min_active_events'):
            filters['min_active_events'] = {
                'column': 'ec.active_events_count',
                'operator': '>=',
                'value': int(request.args.get('min_active_events', 0))
            }
        return search(base_sql, filters)
    except Exception as e:
        logging.exception("Error searching sports:")
        return jsonify({'error': 'Failed to search sports'}), 500

# Update sport
@sports_routes.route('/sports/<int:sport_id>', methods=['PUT'])
def update_sport(sport_id):
    try:
        sport_data = request.json
        sport = Sport(**sport_data)

        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE sports
                    SET name = %s, slug = %s, active = %s
                    WHERE id = %s
                """, (sport.name, sport.slug, sport.active, sport_id))
                conn.commit()
        
        cache.delete('sports')

        return jsonify({'message': 'Sport updated successfully'}), 200
    except Exception as e:
        logging.exception("Error updating sport:")
        return jsonify({'error': 'Failed to update sport'}), 500

# When all events of a sport are inactive, the sport becomes inactive.
def check_sports_inactive():
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE sports s SET active = false WHERE 
                    (SELECT COUNT(*) FROM events e WHERE e.sport = s.id AND e.active = true) = 0
                """)
                conn.commit()

        cache.delete('sports')

    except Exception as e:
        logging.exception("Error checking sports inactive:")

# Create a Blueprint for events routes
events_routes = Blueprint('events', __name__)

# Create event
@events_routes.route('/events', methods=['POST'])
def create_event():
    try:
        event_data = request.json
        event = Event(**event_data)

        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO events (name, slug, active, type, sport, status, scheduled_start, actual_start)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (event.name, event.slug, event.active, event.type, event.sport.id, event.status, event.scheduled_start, event.actual_start))
                conn.commit()
        
        cache.delete('events')

        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        logging.exception("Error creating event:")
        return jsonify({'error': 'Failed to create event'}), 500

# Search events
@events_routes.route('/events/search', methods=['GET'])
@cache.cached(timeout=60, query_string=True, key_prefix='events')
def search_events():
    try:
        base_sql = """
            SELECT e.* FROM events e 
            JOIN (
                SELECT s.event, COUNT(*) active_selections_count 
                FROM selections s WHERE s.active = true GROUP BY s.event
            ) sc ON e.id = sc.event 
            WHERE 1=1
        """
        filters = {}
        if request.args.get('name_regex'):
            filters['name_regex'] = {
                'column': 'e.name',
                'operator': 'REGEXP',
                'value': request.args.get('name_regex')
            }
        if request.args.get('min_active_selections'):
            filters['min_active_selections'] = {
                'column': 'sc.active_selections_count',
                'operator': '>=',
                'value': int(request.args.get('min_active_selections', 0))
            }
        if request.args.get('start_time') and request.args.get('end_time'):
            filters['start_time'] = {
                'column': 'CONVERT_TZ(e.scheduled_start, "+00:00", %s)',
                'operator': 'BETWEEN',
                'value': (
                    request.args.get('timezone'),
                    datetime.fromisoformat(request.args.get('start_time')),
                    datetime.fromisoformat(request.args.get('end_time'))
                ) if request.args.get('start_time') and request.args.get('end_time') else None
            }
        return search(base_sql, filters)
    except Exception as e:
        logging.exception("Error searching events:")
        return jsonify({'error': 'Failed to search events'}), 500

# Update event
@events_routes.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    try:
        event_data = request.json
        event = Event(**event_data)

        with get_db() as conn:
            with conn.cursor() as cursor:
                if event.status == 'Started':
                    cursor.execute("""
                        UPDATE events
                        SET name = %s, slug = %s, active = %s, type = %s, sport = %s, status = %s, scheduled_start = %s, actual_start = NOW()
                        WHERE id = %s
                    """, (event.name, event.slug, event.active, event.type, event.sport.id, event.status, event.scheduled_start, event_id))
                else:
                    cursor.execute("""
                        UPDATE events
                        SET name = %s, slug = %s, active = %s, type = %s, sport = %s, status = %s, scheduled_start = %s
                        WHERE id = %s
                    """, (event.name, event.slug, event.active, event.type, event.sport.id, event.status, event.scheduled_start, event_id))
                conn.commit()

        cache.delete('events')

        if event.active == False:
            check_sports_inactive()

        return jsonify({'message': 'Event updated successfully'}), 200
    except Exception as e:
        logging.exception("Error updating event:")
        return jsonify({'error': 'Failed to update event'}), 500

# When all selections of an event are inactive, the event becomes inactive.
def check_events_inactive():
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE events e SET active = false WHERE 
                    (SELECT COUNT(*) FROM selections s WHERE s.event = e.id AND s.active = true) = 0
                """)
                conn.commit()
        
        cache.delete('events')

    except Exception as e:
        logging.exception("Error checking events inactive:")

# Create a Blueprint for selections routes
selections_routes = Blueprint('selections', __name__)

# Create selection
@selections_routes.route('/selections', methods=['POST'])
def create_selection():
    try:
        selection_data = request.json
        selection = Selection(**selection_data)

        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO selections (name, event, price, active, outcome)
                    VALUES (%s, %s, %s, %s, %s)
                """, (selection.name, selection.event.id, selection.price, selection.active, selection.outcome))
                conn.commit()
        
        cache.delete('selections')

        return jsonify({'message': 'Selection created successfully'}), 201
    except Exception as e:
        logging.exception("Error creating selection:")
        return jsonify({'error': 'Failed to create selection'}), 500

# Search selections
@selections_routes.route('/selections/search', methods=['GET'])
@cache.cached(timeout=60, query_string=True, key_prefix='selections')
def search_selections():
    try:
        base_sql = """
            SELECT * FROM selections 
            WHERE 1=1
        """
        filters = {}
        if request.args.get('name_regex'):
            filters['name_regex'] = {
                'column': 'name',
                'operator': 'REGEXP',
                'value': request.args.get('name_regex')
            }
        return search(base_sql, filters)
    except Exception as e:
        logging.exception("Error searching selections:")
        return jsonify({'error': 'Failed to search selections'}), 500

# Update selection
@selections_routes.route('/selections/<int:selection_id>', methods=['PUT'])
def update_selection(selection_id):
    try:
        selection_data = request.json
        selection = Selection(**selection_data)

        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE selections
                    SET name = %s, event = %s, price = %s, active = %s, outcome = %s
                    WHERE id = %s
                """, (selection.name, selection.event.id, selection.price, selection.active, selection.outcome, selection_id))
                conn.commit()
        
        cache.delete('selections')

        if selection.active == False:
            check_events_inactive()
            check_sports_inactive()

        return jsonify({'message': 'Selection updated successfully'}), 200
    except Exception as e:
        logging.exception("Error updating selection:")
        return jsonify({'error': 'Failed to update selection'}), 500

# General search function
"""
Takes a base sql query and a dictionary of filters as input. 
Each filter is a dictionary that specifies the column to filter on, 
the operator to use (e.g., '=', '>', 'REGEXP', 'BETWEEN', etc.), 
and the value to compare against. 
Additional filters can be added by extending the dictionaries in each route's function
"""
def search(sql, filters):
    try:
        params = []
        for key, filter in filters.items():
            if filter['value'] is not None:
                if filter['operator'] == 'BETWEEN' and isinstance(filter['value'], tuple):
                    sql += f" AND {filter['column']} {filter['operator']} %s AND %s"
                    params.extend(filter['value'])
                else:
                    sql += f" AND {filter['column']} {filter['operator']} %s"
                    params.append(filter['value'])
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        logging.exception("Error searching:")
        return jsonify({'error': 'Failed to perform search'}), 500
