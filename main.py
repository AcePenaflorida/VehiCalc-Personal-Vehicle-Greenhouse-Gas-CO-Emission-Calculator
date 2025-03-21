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

class CarbonFootprintCalculator: #Parent
    def __init__(self, user_input):
        self.user_input = user_input
        self.carbon_emission = 0

    def calculate_carbon_emission(self):
        pass

# Fuel-based calculator
class FuelBasedCalculator(CarbonFootprintCalculator):
    EMISSION_FACTORS = {"Gasoline": 2.31, "Diesel": 2.68}
    
    def calculate_carbon_emission(self):
        fuel_used = self.user_input.distance_travelled / self.user_input.fuel_efficiency
        self.carbon_emission = fuel_used * self.EMISSION_FACTORS.get(self.user_input.fuel_type, 0)
        return self.carbon_emission

# Distance-based calculator
class DistanceBasedCalculator(CarbonFootprintCalculator):
    AVERAGE_EMISSION_FACTOR = 0.21  # kg CO₂ per km
    
    def calculate_carbon_emission(self):
        self.carbon_emission = self.user_input.distance_travelled * self.AVERAGE_EMISSION_FACTOR
        return self.carbon_emission

# Urban adjustment calculator
class UrbanAdjustmentCalculator(CarbonFootprintCalculator):
    ADJUSTMENT_FACTOR = 1.2
    EMISSION_FACTOR = 0.21  # kg CO₂ per km
    
    def calculate_carbon_emission(self):
        self.carbon_emission = (self.user_input.distance_travelled * self.ADJUSTMENT_FACTOR) * self.EMISSION_FACTOR
        return self.carbon_emission


# Carbon footprint summary
class CarbonFootPrintSummary:
    def __init__(self, user_input, carbon_emission):
        self.user_input = user_input
        self.carbon_emission = carbon_emission
    
    def display_summary(self):
        print("\n📊 Carbon Footprint Summary:")
        print(f"User: {self.user_input.username}")
        print(f"Vehicle Type: {self.user_input.vehicle_type}")
        print(f"Fuel Type: {self.user_input.fuel_type}")
        print(f"Fuel Efficiency: {self.user_input.fuel_efficiency} km/L")
        print(f"Distance Traveled: {self.user_input.distance_travelled} km")
        print(f"Month: {self.user_input.emission_month}")
        print(f"Total Carbon Emission: {self.carbon_emission:.2f} kg CO₂\n")

def get_calculator(user_input, urban_mode=False):
    if user_input.fuel_efficiency and user_input.fuel_type:  # Check if fuel data is available
        return FuelBasedCalculator(user_input)
    elif urban_mode:  # If urban mode is specified, apply urban adjustment
        return UrbanAdjustmentCalculator(user_input)
    else:  # Default to distance-based calculation
        return DistanceBasedCalculator(user_input)


