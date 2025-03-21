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

# Store emission history
class EmissionHistory:
    def __init__(self, user_input, carbon_emission):
        self.user_input = user_input
        self.carbon_emission = carbon_emission

    def store_emission(self):
        if not os.path.exists(EMISSION_FILE):
            with open(EMISSION_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])

        data = []
        found = False

        with open(EMISSION_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == self.user_input.username:
                    row[self.user_input.emission_month] = str(float(row.get(self.user_input.emission_month, "0") or 0) + self.carbon_emission)
                    found = True
                data.append(row)

        if not found:
            new_entry = {"username": self.user_input.username, self.user_input.emission_month: str(self.carbon_emission)}
            data.append(new_entry)

        with open(EMISSION_FILE, "w", newline="") as file:
            fieldnames = ["username"] + ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
            
# Emission history viewer
class EmissionHistoryViewer:
    @staticmethod
    def view_emission_history(username):
        if not os.path.exists(EMISSION_FILE):
            print("No emission history found.")
            return
        
        with open(EMISSION_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    print("\n📜 Emission History:")
                    for month, emission in row.items():
                        if month != "username" and emission:
                            print(f"{month}: {emission} kg CO₂")
                    return
            print("No emission records found for this user.")
            
def get_calculator(user_input, urban_mode=False):
    if user_input.fuel_efficiency and user_input.fuel_type:  # Check if fuel data is available
        return FuelBasedCalculator(user_input)
    elif urban_mode:  # If urban mode is specified, apply urban adjustment
        return UrbanAdjustmentCalculator(user_input)
    else:  # Default to distance-based calculation
        return DistanceBasedCalculator(user_input)


if __name__ == "__main__":
    while True:
        print("\n[1] Sign Up\n[2] Log In\n[3] Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = User(username, password)
            user.save_user()
            print("User registered successfully!")

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            
            if User.validate_user(username, password):
                os.system("cls")
                print("Login successful!")
                status = True
                
                while status:
                    print("\n[1] Record Emission\n[2] View Emission History\n[3] Exit")
                    action = input("Action: ")
                    
                    if action == "1":
                        
                        vehicle_type = input("Enter vehicle type (Car, Motorcycle, Van): ")
                        fuel_type = input("Enter fuel type (Gasoline, Diesel) or press Enter if unknown: ")
                        fuel_efficiency = input("Enter fuel efficiency (km/L) or press Enter if unknown: ")
                        distance_travelled = float(input("Enter distance travelled (km): "))
                        emission_month = input("Enter month (e.g., Jan, Feb, etc.): ")
                        urban_mode = input("Is the travel in urban traffic? (yes/no): ").strip().lower() == "yes"
                        
                        # Convert fuel efficiency input to float if provided
                        fuel_efficiency = float(fuel_efficiency) if fuel_efficiency else None
                        user_input = UserInput(username, vehicle_type, fuel_type, fuel_efficiency, distance_travelled, emission_month)
                        calculator = get_calculator(user_input, urban_mode)
                        
                        # Calculate emission
                        emission = calculator.calculate_carbon_emission()
                                                
                        
                        
                        summary = CarbonFootPrintSummary(user_input, emission)
                        summary.display_summary()
                        
                        history = EmissionHistory(user_input, emission)
                        history.store_emission()
                    
                    elif action == "2":
                        EmissionHistoryViewer.view_emission_history(username)
                    
                    elif action == "3":
                        status = False
                    
                    else:
                        print("Invalid Input. Please try again.")
            
            else:
                print("Invalid username or password.")

        elif choice == "3":
            print("Goodbye!")
            exit()
        
        else:
            print("Invalid choice. Please try again.")


