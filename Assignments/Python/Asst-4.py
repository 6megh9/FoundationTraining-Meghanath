import mysql.connector as con
from mysql.connector import Error

class CourierOrder:
    def __init__(self, order_id, customer_id, order_date):
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_date = order_date

class CourierSystem:
    def __init__(self):
        try:
            self.connect = con.connect(host="localhost", user="root", password="Root", database=" couriermanagemnetsystem")
            if self.connect.is_connected():
                print("Connected to the database")
        except Error as e:
            print(f"Error: {e}")

    def execute_query(self, query, data=None):
        try:
            cursor = self.connect.cursor()
            cursor.execute(query, data)
            self.connect.commit()
        except Error as e:
            print(f"Error executing query: {e}")

    def place_order(self, order_id, customer_id, order_date):
        try:
            order = CourierOrder(order_id, customer_id, order_date)
            data = (order.order_id, order.customer_id, order.order_date)
            query = "INSERT INTO orders (order_id, customer_id, order_date) VALUES (%s, %s, %s);"
            self.execute_query(query, data)
            print("Order placed successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def menu(self):
        print("Courier Management System")
        print("1. Place Order")
        print("2. Exit")

        option = input("Enter option: ")

        if option == '1':
            order_id = input("Enter Order ID: ")
            customer_id = input("Enter Customer ID: ")
            order_date = input("Enter Order Date (YYYY-MM-DD): ")
            self.place_order(order_id, customer_id, order_date)
            self.menu()
        elif option == '2':
            print("Exiting the system.")
        else:
            print("Invalid option. Try again.")
            self.menu()

if __name__ == "__main__":
    courier_system = CourierSystem()
    courier_system.menu()
