from flask import Flask, render_template, jsonify, request
from datetime import datetime
import psycopg2
import psycopg2.extras
from psycopg2 import pool
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with a secure key
csrf = CSRFProtect(app)

# Database configuration
DB_CONFIG = {
    'dbname': 'event_management',
    'user': 'postgres',
    'password': 'JaiMataKi',
    'host': 'localhost',
    'port': 5432
}

# Create connection pool
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        **DB_CONFIG
    )
except psycopg2.OperationalError as e:
    print(f"Error: Unable to connect to the database: {e}")
    exit(1)

def get_db_connection():
    return connection_pool.getconn()

def return_db_connection(conn):
    connection_pool.putconn(conn)


venues = {
    "birthday": [
        {"name": "Noma Convention", "facilities": ["ac", "valet_parking"], "capacity": 200},
        {"name": "Balaji Function Hall", "facilities": ["non_ac", "internet"], "capacity": 150},
        {"name": "Grand Paradise", "facilities": ["ac", "internet", "led_screens"], "capacity": 300},
        {"name": "Sunshine Hall", "facilities": ["non_ac", "valet_parking"], "capacity": 100}
    ],
    "wedding": [
        {"name": "Royal Orchid Palace", "facilities": ["ac", "valet_parking", "led_screens"], "capacity": 500},
        {"name": "Vivanta Taj", "facilities": ["ac", "internet", "led_screens"], "capacity": 400},
        {"name": "The Oberoi Venue", "facilities": ["ac", "valet_parking", "internet"], "capacity": 600},
        {"name": "Leela Banquet Hall", "facilities": ["ac", "valet_parking", "internet"], "capacity": 450}
    ],
    "house_warming": [
      { "name": "Cozy Corner", "facilities": ["ac", "internet"], "capacity": 100 },
      { "name": "Home Sweet Home", "facilities": ["non_ac", "valet_parking"], "capacity": 80 },
      { "name": "Garden Paradise", "facilities": ["non_ac", "internet"], "capacity": 120 },
      { "name": "Urban Nest", "facilities": ["ac", "valet_parking"], "capacity": 150 }
    ],
    "baby_shower": [
      { "name": "Little Angels Hall", "facilities": ["ac", "internet"], "capacity": 100 },
      { "name": "Tiny Tots Paradise", "facilities": ["ac", "valet_parking"], "capacity": 120 },
      { "name": "Stork's Corner", "facilities": ["non_ac", "internet"], "capacity": 80 },
      { "name": "Baby Bliss Center", "facilities": ["ac", "led_screens"], "capacity": 150 }
    ],
    "reunion": [
      { "name": "Memory Lane Hall", "facilities": ["ac", "internet", "led_screens"], "capacity": 200 },
      { "name": "Nostalgia Palace", "facilities": ["ac", "valet_parking"], "capacity": 250 },
      { "name": "Friends Forever Center", "facilities": ["non_ac", "internet"], "capacity": 180 },
      { "name": "Reunion Plaza", "facilities": ["ac", "valet_parking", "led_screens"], "capacity": 300 }
    ],
    "engagement": [
      { "name": "Promise Banquet", "facilities": ["ac", "internet", "led_screens"], "capacity": 300 },
      { "name": "Love Knot Venue", "facilities": ["ac", "valet_parking"], "capacity": 250 },
      { "name": "Celebration Hall", "facilities": ["ac", "valet_parking", "led_screens"], "capacity": 400 },
      { "name": "Dreamland Banquet", "facilities": ["ac", "internet", "led_screens"], "capacity": 350 }
    ],
    "reception": [
      { "name": "Grand Celebration Center", "facilities": ["ac", "valet_parking", "led_screens"], "capacity": 600 },
      { "name": "Royal Reception Hall", "facilities": ["ac", "internet", "led_screens"], "capacity": 500 },
      { "name": "Majestic Manor", "facilities": ["ac", "valet_parking", "internet"], "capacity": 700 },
      { "name": "Elite Events Plaza", "facilities": ["ac", "valet_parking", "led_screens"], "capacity": 550 }
    ],
    "conference": [
      { "name": "Tech Park Hall", "facilities": ["ac", "internet", "led_screens"], "capacity": 200 },
      { "name": "Business Center", "facilities": ["ac", "valet_parking", "internet"], "capacity": 150 },
      { "name": "Corporate Plaza", "facilities": ["ac", "internet", "led_screens"], "capacity": 300 },
      { "name": "Executive Summit Hall", "facilities": ["ac", "valet_parking", "led_screens"], "capacity": 250 }
    ]
}

@app.route('/')
def home():
    if(get_db_connection):
        print("Database connection successful")
        return render_template('index.html')
    else:
        return "Database connection failed"

@app.route('/events')
def events():
    if(get_db_connection):
        print("Database connection successful")
        return render_template('events.html')
    else:
        return "Database connection failed"


# Exempt CSRF for API endpoints
@csrf.exempt
@app.route('/api/venue-options', methods=['GET'])
def get_venue_options():
    try:
        event_type = request.args.get('event_type')

        if not event_type:
            return jsonify({"success": False, "error": "Event type is required"}), 400

        if event_type not in venues:
            return jsonify({"success": False, "error": "Invalid event type"}), 400

        return jsonify({
            "success": True,
            "data": venues[event_type]
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@csrf.exempt
@app.route('/api/events', methods=['GET'])
def get_events():
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    e.event_id,
                    e.event_type,
                    e.event_date,
                    c.first_name,
                    c.last_name,
                    c.phone,
                    c.email,
                    v.location as venue,
                    v.capacity,
                    v.facilities,
                    cat.menu_type as catering,
                    d.decor_style,
                    d.decor_cost,
                    ent.cost as entertainment_cost
                FROM event e
                JOIN customer c ON e.customer_id = c.customer_id
                JOIN venue v ON e.venue_id = v.venue_id
                JOIN catering cat ON e.catering_id = cat.category_id
                JOIN decoration d ON e.decor_id = d.decor_id
                JOIN entertainment ent ON e.entertainment_id = ent.entertainment_id
                ORDER BY e.event_date DESC
            """)
            
            columns = [desc[0] for desc in cursor.description]
            events = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return jsonify(events)
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn:
            return_db_connection(conn)

@app.route('/api/events', methods=['POST'])
def create_event():
    conn = None
    try:
        conn = get_db_connection()
        data = request.json

        # Input validation
        required_fields = [
            'firstName', 'lastName', 'phone', 'email', 
            'eventType', 'eventDate', 'venue', 'catering', 
            'decor_style', 'entertainment_cost'
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400

        with conn.cursor() as cursor:
            # Customer handling remains the same...
                 # Check if customer already exists
            cursor.execute("""
                SELECT customer_id FROM customer 
                WHERE phone = %s OR email = %s
            """, (data['phone'], data['email']))

            customer_result = cursor.fetchone()

            if customer_result:
                customer_id = customer_result[0]
                cursor.execute("""
                    UPDATE customer 
                    SET first_name = %s, last_name = %s, phone = %s, email = %s
                    WHERE customer_id = %s
                """, (
                    data['firstName'], data['lastName'], 
                    data['phone'], data['email'], customer_id
                ))
            else:
                cursor.execute("""
                    INSERT INTO customer (first_name, last_name, phone, email)
                    VALUES (%s, %s, %s, %s)
                    RETURNING customer_id
                """, (
                    data['firstName'], data['lastName'], 
                    data['phone'], data['email']
                ))
                customer_id = cursor.fetchone()[0]

            # Fetch venue_id - Modified to use venue name
            cursor.execute("SELECT venue_id FROM venue WHERE location = %s", 
                         (data['venue'],))
            venue_result = cursor.fetchone()
            if not venue_result:
                cursor.execute("""
                INSERT INTO venue (
                    facilities, location, capacity
                )
                VALUES (%s, %s, %s)
                RETURNING venue_id
                """, (
                    data['facilities'], 
                    data['venue'],  # Changed from location to venue
                    data['capacity']
                ))
                venue_id = cursor.fetchone()[0]
            else:
                venue_id = venue_result[0]

            # Fetch catering_id
            cursor.execute("SELECT category_id FROM catering WHERE menu_type = %s", 
                         (data['catering'],))
            catering_result = cursor.fetchone()
            if not catering_result:
                cursor.execute("""
                INSERT INTO catering (menu_type)
                VALUES (%s)
                RETURNING category_id
                """, (data['catering'],))
                catering_id = cursor.fetchone()[0]
            else:
                catering_id = catering_result[0]

            # Fetch decor_id
            cursor.execute("SELECT decor_id FROM decoration WHERE decor_style = %s", 
                         (data['decor_style'],))
            decor_result = cursor.fetchone()
            if not decor_result:
                cursor.execute("""
                INSERT INTO decoration (decor_style, decor_cost)
                VALUES (%s, %s)
                RETURNING decor_id
                """, (data['decor_style'], data['decor_cost']))
                decor_id = cursor.fetchone()[0]
            else:
                decor_id = decor_result[0]

            # Fetch entertainment_id
            cursor.execute("SELECT entertainment_id FROM entertainment WHERE cost = %s", 
                         (data['entertainment_cost'],))
            entertainment_result = cursor.fetchone()
            if not entertainment_result:
                cursor.execute("""
                INSERT INTO entertainment (cost)
                VALUES (%s)
                RETURNING entertainment_id
                """, (data['entertainment_cost'],))
                entertainment_id = cursor.fetchone()[0]
            else:
                entertainment_id = entertainment_result[0]

            # Create the event with proper value extraction
            cursor.execute("""
                INSERT INTO event (
                    event_type, event_date, venue_id, catering_id, 
                    decor_id, customer_id, entertainment_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING event_id
            """, (
                data['eventType'],
                data['eventDate'],
                venue_id,
                catering_id,
                decor_id,
                customer_id,  # This comes from earlier customer handling
                entertainment_id
            ))

            event_id = cursor.fetchone()[0]
            conn.commit()

            return jsonify({
                "success": True,
                "message": "Event booked successfully",
                "event_id": event_id
            })

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn:
            return_db_connection(conn)





def calculate_event_cost(data):
    CATERING_PRICES = {
        'indian': 500,
        'continental': 700,
        'chinese': 600,
        'italian': 800,
        'mexican': 900,
        'japanese': 1000,
        'thai': 750,
        'vegan_special': 850
    }
    
    DECORATION_PRICES = {
        'simple': 5000,
        'premium': 10000,
        'luxury': 20000
    }
    
    ENTERTAINMENT_PRICES = {
        'music': 8000,
        'dance': 12000,
        'comedy': 15000
    }
    
    catering_cost = CATERING_PRICES.get(data['catering'], 0) * data['guestCount']
    decoration_cost = DECORATION_PRICES.get(data['decoration'], 0)
    entertainment_cost = ENTERTAINMENT_PRICES.get(data['entertainment'], 0)
    venue_cost = 15000
    
    tax = (catering_cost + decoration_cost + entertainment_cost + venue_cost) * 0.18
    service_charge = 7500 if data['guestCount'] > 100 else 3500
    convenience_fee = 350
    security_deposit = 2500
    
    total_cost = (catering_cost + decoration_cost + entertainment_cost + 
                 venue_cost + tax + service_charge + convenience_fee + 
                 security_deposit)
    
    return total_cost

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("""
                SELECT e.*, c.name as customer_name, c.phone, c.email
                FROM event e
                JOIN customer c ON e.customer_id = c.customer_id
                WHERE e.event_id = %s
            """, (event_id,))
            event = cursor.fetchone()
            
            if event is None:
                return jsonify({"success": False, "error": "Event not found"}), 404
                
            return jsonify({
                "success": True,
                "event": dict(event)
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if conn:
            return_db_connection(conn)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
