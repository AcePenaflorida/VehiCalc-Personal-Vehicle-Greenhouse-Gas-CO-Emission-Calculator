# VehiCalc
import csv
import hashlib
import os

# File paths
USER_FILE = "users.csv"
EMISSION_FILE = "emission_history.csv"

# Utility function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User authentication class
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = hash_password(password)

    def save_user(self):
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password"])
        
        with open(USER_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.username, self.password])

    @staticmethod
    def validate_user(username, password):
        if not os.path.exists(USER_FILE):
            return False
        with open(USER_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username and row["password"] == hash_password(password):
                    return True
        return False
# User input class
class UserInput:
    def __init__(self, username, vehicle_type, fuel_type, fuel_efficiency, distance_travelled, emission_month):
        self.username = username
        self.vehicle_type = vehicle_type
        self.fuel_type = fuel_type
        self.fuel_efficiency = fuel_efficiency
        self.distance_travelled = distance_travelled
        self.emission_month = emission_month

    def validate(self):
        if self.vehicle_type not in ["Car", "Motorcycle", "Van"]:
            raise ValueError("Invalid vehicle type. Choose Car, Motorcycle, or Van.")
        if self.fuel_efficiency <= 0 or self.distance_travelled <= 0:
            raise ValueError("Fuel efficiency and distance must be positive numbers.")
class CarbonFootprintCalculator:
    def __init__(self, user_input):
        self.user_input = user_input
        self.carbon_emission = 0

    def calculate_carbon_emission(self):
        pass
