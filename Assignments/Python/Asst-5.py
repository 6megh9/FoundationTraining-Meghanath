import mysql.connector as con
from mysql.connector import Error
import datetime

class DBUtil:
    @staticmethod
    def get_db_conn():
        try:
            conn = con.connect(
                host="localhost",
                user="root",
                password="Root",
                database="bookingsystem"
            )
            if conn.is_connected():
                print("Connected to MySQL database")
                return conn
        except Error as e:
            print(f"Error: {e}")
            return None

class Venue:
    def __init__(self, venue_name, address):
        self.venue_name = venue_name
        self.address = address

    def display_venue_details(self):
        print("Venue Name:", self.venue_name)
        print("Address:", self.address)

class Event:
    def __init__(self, event_id, event_name, event_date, event_time, venue_id, total_seats, available_seats, ticket_price, event_type):
        self.id = event_id
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.venue_id = venue_id
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.ticket_price = ticket_price
        self.event_type = event_type

    def display_event_details(self):
        print("Event ID:", self.id)
        print("Event Name:", self.event_name)
        print("Date:", self.event_date)
        print("Time:", self.event_time)
        print("Venue ID:", self.venue_id)
        print("Total Seats:", self.total_seats)
        print("Available Seats:", self.available_seats)
        print("Ticket Price:", self.ticket_price)
        print("Event Type:", self.event_type)

class Booking:
    def __init__(self, booking_id, customer_id, event_id, num_tickets, total_cost, booking_date):
        self.id = booking_id
        self.customer_id = customer_id
        self.event_id = event_id
        self.num_tickets = num_tickets
        self.total_cost = total_cost
        self.booking_date = booking_date

    def display_booking_details(self):
        print("Booking ID:", self.id)
        print("Customer ID:", self.customer_id)
        print("Event ID:", self.event_id)
        print("Number of Tickets:", self.num_tickets)
        print("Total Cost:", self.total_cost)
        print("Booking Date:", self.booking_date)

class TicketBookingSystem:
    def __init__(self):
        self.conn = DBUtil.get_db_conn()

    def load_events_from_db(self):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM event')
                rows = cursor.fetchall()
                events = []
                for row in rows:
                    event = Event(
                        row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
                    )
                    events.append(event)
                return events
        except Error as e:
            print(f"Error loading events: {e}")
            return []

    def load_bookings_from_db(self):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('SELECT * FROM booking')
                rows = cursor.fetchall()
                bookings = []
                for row in rows:
                    booking = Booking(
                        row[0], row[1], row[2], row[3], row[4], row[5]
                    )
                    bookings.append(booking)
                return bookings
        except Error as e:
            print(f"Error loading bookings: {e}")
            return []

    def calculate_booking_cost(self, num_tickets, event):
        return num_tickets * event.ticket_price

    def book_tickets(self, event_id, num_tickets):
        try:
            event = next((e for e in self.load_events_from_db() if e.id == event_id), None)
            if event:
                if event.available_seats >= num_tickets:
                    booking_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    total_cost = self.calculate_booking_cost(num_tickets, event)
                    # For simplicity, assume customer_id is 1 (replace with actual logic to get customer ID)
                    customer_id = 1
                    booking = Booking(None, customer_id, event.id, num_tickets, total_cost, booking_date)
                    self.save_booking_to_db(booking)
                    event.available_seats -= num_tickets
                    self.save_event_to_db(event)
                    print(f"Booking successful! Total cost: {total_cost}")
                else:
                    print("Not enough available seats.")
            else:
                print("Event not found.")
        except Exception as e:
            print(f"Error booking tickets: {e}")

    def save_event_to_db(self, event):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('''
                    UPDATE event 
                    SET available_seats = %s
                    WHERE id = %s
                ''', (event.available_seats, event.id))
                self.conn.commit()
        except Error as e:
            print(f"Error saving event: {e}")

    def save_booking_to_db(self, booking):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO booking 
                    (customer_id, event_id, num_tickets, total_cost, booking_date) 
                    VALUES (%s, %s, %s, %s, %s)
                ''', (booking.customer_id, booking.event_id, booking.num_tickets, booking.total_cost, booking.booking_date))
                self.conn.commit()
        except Error as e:
            print(f"Error saving booking: {e}")

# Example Usage:
if __name__ == "__main__":
    ticket_system = TicketBookingSystem()

    # Displaying event details
    events = ticket_system.load_events_from_db()
    for e in events:
        e.display_event_details()  # Corrected line

    # Booking tickets
    ticket_system.book_tickets(1, 2)

