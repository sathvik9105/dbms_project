from flask import Flask, render_template, jsonify, request
from datetime import datetime
import psycopg2
import psycopg2.extras
from psycopg2 import pool
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
csrf = CSRFProtect(app)

# Database configuration
DB_CONFIG = {
    'dbname': 'event_management',
    'user': 'postgres',
    'password': 'sathvik123',
    'host': 'localhost',
    'port': 5432
}

# Create connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,
    **DB_CONFIG
)

def get_db_connection():
    return connection_pool.getconn()

def return_db_connection(conn):
    connection_pool.putconn(conn)

@app.route('/')
def home():
    return render_template('index.html')

# Exempt CSRF for API endpoints
@csrf.exempt
@app.route('/api/venue-options', methods=['GET'])
def get_venue_options():
    try:
        event_type = request.args.get('event_type')
        facility = request.args.get('facility')
        guest_count = request.args.get('guest_count')

        if not event_type:
            return jsonify({"success": False, "error": "Event type is required"}), 400

        return jsonify({
            "success": True,
            "message": "Use frontend venues data for filtering"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@csrf.exempt
@app.route('/api/events', methods=['POST'])
def create_event():
    conn = None
    try:
        conn = get_db_connection()
        data = request.json
        
        # Input validation
        required_fields = ['customer_name', 'contact_info', 'event_type', 
                         'event_date', 'guest_count', 'venue', 'catering', 
                         'decoration', 'entertainment']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400

        with conn.cursor() as cursor:
            # First, check if customer already exists
            cursor.execute("""
                SELECT customer_id FROM customer 
                WHERE contact_info = %s
            """, (data['contact_info'],))
            
            customer_result = cursor.fetchone()
            
            if customer_result:
                customer_id = customer_result[0]
                # Update customer information
                cursor.execute("""
                    UPDATE customer 
                    SET name = %s, address = %s 
                    WHERE customer_id = %s
                """, (data['customer_name'], data.get('address', ''), customer_id))
            else:
                # Create new customer
                cursor.execute("""
                    INSERT INTO customer (name, contact_info, address)
                    VALUES (%s, %s, %s)
                    RETURNING customer_id
                """, (data['customer_name'], data['contact_info'], data.get('address', '')))
                customer_id = cursor.fetchone()[0]
            
            # Create event
            cursor.execute("""
                INSERT INTO event (
                    customer_id, event_type, event_date, guest_count,
                    venue, catering, decoration, entertainment,
                    created_at, total_cost, status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING event_id
            """, (
                customer_id,
                data['event_type'],
                data['event_date'],
                data['guest_count'],
                data['venue'],
                data['catering'],
                data['decoration'],
                data['entertainment'],
                datetime.now(),
                calculate_event_cost(data),
                'pending'
            ))
            
            event_id = cursor.fetchone()[0]
            conn.commit()
            
            return jsonify({
                "success": True,
                "message": "Event booked successfully",
                "event_id": event_id,
                "total_cost": calculate_event_cost(data)
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
    
    catering_cost = CATERING_PRICES.get(data['catering'], 0) * data['guest_count']
    decoration_cost = DECORATION_PRICES.get(data['decoration'], 0)
    entertainment_cost = ENTERTAINMENT_PRICES.get(data['entertainment'], 0)
    venue_cost = 15000
    
    tax = (catering_cost + decoration_cost + entertainment_cost + venue_cost) * 0.18
    service_charge = 7500 if data['guest_count'] > 100 else 3500
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
                SELECT e.*, c.name as customer_name, c.contact_info, c.address
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