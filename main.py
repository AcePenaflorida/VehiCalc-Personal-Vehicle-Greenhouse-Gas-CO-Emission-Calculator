# VehiCalc - Enhanced with robust validation and error handling
import csv
import hashlib
import os
from datetime import datetime
from enum import Enum, auto

# Constants
USER_FILE = "users.csv"
EMISSION_FILE = "emission_history.csv"
VALID_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class VehicleType(Enum):
    CAR = auto()
    MOTORCYCLE = auto()
    VAN = auto()

class FuelType(Enum):
    GASOLINE = auto()
    DIESEL = auto()

# Utility functions for validation
def validate_username(username):
    if not username or not isinstance(username, str):
        raise ValueError("Username must be a non-empty string")
    if len(username) < 4 or len(username) > 20:
        raise ValueError("Username must be between 4 and 20 characters")
    if not username.isalnum():
        raise ValueError("Username can only contain letters and numbers")
    return username

def validate_password(password):
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    return password

def validate_vehicle_type(vehicle_type):
    try:
        return VehicleType[vehicle_type.upper()]
    except KeyError:
        raise ValueError(f"Invalid vehicle type. Must be one of: {[v.name for v in VehicleType]}")

def validate_fuel_type(fuel_type):
    if not fuel_type:  # Allow empty for distance-based calculation
        return None
    try:
        return FuelType[fuel_type.upper()]
    except KeyError:
        raise ValueError(f"Invalid fuel type. Must be one of: {[f.name for f in FuelType]} or empty")

def validate_fuel_efficiency(efficiency):
    if efficiency is None:  # Allow None for distance-based calculation
        return None
    try:
        eff = float(efficiency)
        if eff <= 0:
            raise ValueError("Fuel efficiency must be positive")
        return eff
    except (ValueError, TypeError):
        raise ValueError("Fuel efficiency must be a positive number")

def validate_distance(distance):
    try:
        dist = float(distance)
        if dist <= 0:
            raise ValueError("Distance must be positive")
        return dist
    except (ValueError, TypeError):
        raise ValueError("Distance must be a positive number")

def validate_month(month):
    if month not in VALID_MONTHS:
        raise ValueError(f"Invalid month. Must be one of: {VALID_MONTHS}")
    return month

# Utility function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User authentication class with enhanced validation
class User:
    def __init__(self, username, password):
        self.username = validate_username(username)
        self.password = hash_password(validate_password(password))

    def save_user(self):
        try:
            if not os.path.exists(USER_FILE):
                with open(USER_FILE, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["username", "password"])
            
            # Check if username already exists
            if os.path.exists(USER_FILE):
                with open(USER_FILE, "r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["username"] == self.username:
                            raise ValueError("Username already exists")

            with open(USER_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.username, self.password])
                
        except IOError as e:
            raise IOError(f"Failed to save user: {str(e)}")

    @staticmethod
    def validate_user(username, password):
        try:
            if not os.path.exists(USER_FILE):
                return False
            
            with open(USER_FILE, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username and row["password"] == hash_password(password):
                        return True
            return False
        except IOError as e:
            raise IOError(f"Failed to validate user: {str(e)}")

# Enhanced UserInput class with validation
class UserInput:
    def __init__(self, username, vehicle_type, fuel_type, fuel_efficiency, distance_travelled, emission_month):
        self.username = validate_username(username)
        self.vehicle_type = validate_vehicle_type(vehicle_type)
        self.fuel_type = validate_fuel_type(fuel_type)
        self.fuel_efficiency = validate_fuel_efficiency(fuel_efficiency)
        self.distance_travelled = validate_distance(distance_travelled)
        self.emission_month = validate_month(emission_month)

    def validate(self):
        # Fuel-based calculation requires both fuel type and efficiency
        if self.fuel_type and not self.fuel_efficiency:
            raise ValueError("Fuel efficiency required when fuel type is specified")
        if self.fuel_efficiency and not self.fuel_type:
            raise ValueError("Fuel type required when fuel efficiency is specified")

# Carbon Footprint Calculator classes with error handling
class CarbonFootprintCalculator:
    def __init__(self, user_input):
        if not isinstance(user_input, UserInput):
            raise TypeError("user_input must be an instance of UserInput")
        self.user_input = user_input
        self.carbon_emission = 0

    def calculate_carbon_emission(self):
        raise NotImplementedError("Subclasses must implement this method")

class FuelBasedCalculator(CarbonFootprintCalculator):
    EMISSION_FACTORS = {
        FuelType.GASOLINE: 2.31,
        FuelType.DIESEL: 2.68
    }
    
    def calculate_carbon_emission(self):
        try:
            if not self.user_input.fuel_type or not self.user_input.fuel_efficiency:
                raise ValueError("Both fuel type and efficiency are required for fuel-based calculation")
            
            fuel_used = self.user_input.distance_travelled / self.user_input.fuel_efficiency
            emission_factor = self.EMISSION_FACTORS.get(self.user_input.fuel_type)
            if emission_factor is None:
                raise ValueError(f"No emission factor available for fuel type: {self.user_input.fuel_type}")
            
            self.carbon_emission = fuel_used * emission_factor
            return self.carbon_emission
        except ZeroDivisionError:
            raise ValueError("Fuel efficiency cannot be zero")
        except Exception as e:
            raise ValueError(f"Error in fuel-based calculation: {str(e)}")

class DistanceBasedCalculator(CarbonFootprintCalculator):
    AVERAGE_EMISSION_FACTOR = 0.21  # kg CO₂ per km
    
    def calculate_carbon_emission(self):
        try:
            self.carbon_emission = self.user_input.distance_travelled * self.AVERAGE_EMISSION_FACTOR
            return self.carbon_emission
        except Exception as e:
            raise ValueError(f"Error in distance-based calculation: {str(e)}")

class UrbanAdjustmentCalculator(CarbonFootprintCalculator):
    ADJUSTMENT_FACTOR = 1.2
    EMISSION_FACTOR = 0.21  # kg CO₂ per km
    
    def calculate_carbon_emission(self):
        try:
            adjusted_distance = self.user_input.distance_travelled * self.ADJUSTMENT_FACTOR
            self.carbon_emission = adjusted_distance * self.EMISSION_FACTOR
            return self.carbon_emission
        except Exception as e:
            raise ValueError(f"Error in urban-adjusted calculation: {str(e)}")

# Enhanced CarbonFootPrintSummary with validation
class CarbonFootPrintSummary:
    def __init__(self, user_input, carbon_emission):
        if not isinstance(user_input, UserInput):
            raise TypeError("user_input must be an instance of UserInput")
        if not isinstance(carbon_emission, (int, float)) or carbon_emission < 0:
            raise ValueError("Carbon emission must be a non-negative number")
        
        self.user_input = user_input
        self.carbon_emission = carbon_emission
    
    def display_summary(self):
        try:
            print("\n📊 Carbon Footprint Summary:")
            print(f"User: {self.user_input.username}")
            print(f"Vehicle Type: {self.user_input.vehicle_type.name}")
            print(f"Fuel Type: {self.user_input.fuel_type.name if self.user_input.fuel_type else 'Not specified'}")
            print(f"Fuel Efficiency: {self.user_input.fuel_efficiency if self.user_input.fuel_efficiency else 'Not specified'} km/L")
            print(f"Distance Traveled: {self.user_input.distance_travelled} km")
            print(f"Month: {self.user_input.emission_month}")
            print(f"Total Carbon Emission: {self.carbon_emission:.2f} kg CO₂\n")
        except Exception as e:
            print(f"Error displaying summary: {str(e)}")

# Enhanced EmissionHistory with error handling
class EmissionHistory:
    def __init__(self, user_input, carbon_emission):
        if not isinstance(user_input, UserInput):
            raise TypeError("user_input must be an instance of UserInput")
        if not isinstance(carbon_emission, (int, float)) or carbon_emission < 0:
            raise ValueError("Carbon emission must be a non-negative number")
        
        self.user_input = user_input
        self.carbon_emission = carbon_emission

    def store_emission(self):
        try:
            fieldnames = ["username"] + VALID_MONTHS
            data = []
            
            # Read existing data if file exists
            if os.path.exists(EMISSION_FILE):
                with open(EMISSION_FILE, "r", newline="") as file:
                    reader = csv.DictReader(file)
                    data = list(reader)

            # Update or add user data
            found = False
            for row in data:
                if row["username"] == self.user_input.username:
                    current_value = float(row.get(self.user_input.emission_month, "0") or 0)
                    row[self.user_input.emission_month] = str(current_value + self.carbon_emission)
                    found = True
                    break
            
            if not found:
                new_entry = {"username": self.user_input.username}
                new_entry.update({month: "0" for month in VALID_MONTHS})
                new_entry[self.user_input.emission_month] = str(self.carbon_emission)
                data.append(new_entry)

            # Write back to file
            with open(EMISSION_FILE, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
                
        except IOError as e:
            raise IOError(f"Failed to store emission data: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error processing emission data: {str(e)}")

# Enhanced EmissionHistoryViewer with error handling
class EmissionHistoryViewer:
    @staticmethod
    def view_emission_history(username):
        try:
            validate_username(username)
            
            if not os.path.exists(EMISSION_FILE):
                print("No emission history found.")
                return
            
            with open(EMISSION_FILE, "r") as file:
                reader = csv.DictReader(file)
                found = False
                
                for row in reader:
                    if row["username"] == username:
                        print("\n📜 Emission History:")
                        for month in VALID_MONTHS:
                            if row.get(month, "0") != "0":
                                print(f"{month}: {row[month]} kg CO₂")
                        found = True
                        break
                
                if not found:
                    print("No emission records found for this user.")
                    
        except IOError as e:
            print(f"Error accessing emission history: {str(e)}")
        except Exception as e:
            print(f"Error viewing history: {str(e)}")

def get_calculator(user_input, urban_mode=False):
    try:
        if not isinstance(user_input, UserInput):
            raise TypeError("Invalid user input type")
            
        if user_input.fuel_efficiency and user_input.fuel_type:
            return FuelBasedCalculator(user_input)
        elif urban_mode:
            return UrbanAdjustmentCalculator(user_input)
        else:
            return DistanceBasedCalculator(user_input)
    except Exception as e:
        raise ValueError(f"Error selecting calculator: {str(e)}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        try:
            clear_screen()
            print("\n=== VehiCalc - Carbon Footprint Calculator ===")
            print("[1] Sign Up\n[2] Log In\n[3] Exit")
            choice = input("Choose an option (1-3): ").strip()
            
            if choice == "1":
                handle_signup()
            elif choice == "2":
                handle_login()
            elif choice == "3":
                print("Thank you for using VehiCalc. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            exit()
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("Press Enter to continue...")

def handle_signup():
    clear_screen()
    print("\n=== User Registration ===")
    username = input("Enter username (4-20 alphanumeric characters): ").strip()
    password = input("Enter password (minimum 8 characters): ").strip()
    
    try:
        user = User(username, password)
        user.save_user()
        print("\n✅ User registered successfully!")
        input("Press Enter to continue...")
    except ValueError as e:
        print(f"\n❌ Registration failed: {str(e)}")
        input("Press Enter to try again...")
    except IOError as e:
        print(f"\n❌ Database error: {str(e)}")
        input("Press Enter to try again...")

def handle_login():
    clear_screen()
    print("\n=== User Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    try:
        if User.validate_user(username, password):
            user_session(username)
        else:
            print("\n❌ Invalid username or password")
            input("Press Enter to try again...")
    except Exception as e:
        print(f"\n❌ Login error: {str(e)}")
        input("Press Enter to try again...")

def user_session(username):
    while True:
        try:
            clear_screen()
            print(f"\n=== Welcome, {username} ===")
            print("[1] Record Emission\n[2] View Emission History\n[3] Logout")
            action = input("Choose an action (1-3): ").strip()
            
            if action == "1":
                record_emission(username)
            elif action == "2":
                view_history(username)
            elif action == "3":
                print("\nLogging out...")
                input("Press Enter to continue...")
                return
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\nReturning to main menu...")
            input("Press Enter to continue...")
            return
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("Press Enter to continue...")

def record_emission(username):
    clear_screen()
    print("\n=== Record New Emission ===")
    
    try:
        # Get vehicle type
        print("\nAvailable vehicle types:")
        for i, vt in enumerate(VehicleType, 1):
            print(f"[{i}] {vt.name}")
        vt_choice = input("Select vehicle type (1-3): ").strip()
        vehicle_type = list(VehicleType)[int(vt_choice)-1].name
        
        # Get fuel information
        print("\nAvailable fuel types:")
        for i, ft in enumerate(FuelType, 1):
            print(f"[{i}] {ft.name}")
        print("[0] Skip (for distance-based calculation)")
        ft_choice = input("Select fuel type (0-2): ").strip()
        fuel_type = list(FuelType)[int(ft_choice)-1].name if ft_choice != "0" else ""
        
        # Get other inputs
        fuel_efficiency = input("Enter fuel efficiency (km/L) or leave blank: ").strip() or None
        distance_travelled = input("Enter distance travelled (km): ").strip()
        emission_month = input("Enter month (e.g., Jan, Feb, etc.): ").strip().capitalize()
        urban_mode = input("Is the travel in urban traffic? (y/n): ").strip().lower() == "y"
        
        # Create and validate user input
        user_input = UserInput(
            username=username,
            vehicle_type=vehicle_type,
            fuel_type=fuel_type,
            fuel_efficiency=fuel_efficiency,
            distance_travelled=distance_travelled,
            emission_month=emission_month
        )
        
        # Calculate emissions
        calculator = get_calculator(user_input, urban_mode)
        emission = calculator.calculate_carbon_emission()
        
        # Show summary and store
        summary = CarbonFootPrintSummary(user_input, emission)
        summary.display_summary()
        
        history = EmissionHistory(user_input, emission)
        history.store_emission()
        
        print("\n✅ Emission recorded successfully!")
        input("Press Enter to continue...")
        
    except (ValueError, IndexError) as e:
        print(f"\n❌ Invalid input: {str(e)}")
        input("Press Enter to try again...")
    except Exception as e:
        print(f"\n❌ Error recording emission: {str(e)}")
        input("Press Enter to try again...")

def view_history(username):
    clear_screen()
    print("\n=== Emission History ===")
    try:
        EmissionHistoryViewer.view_emission_history(username)
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"\n❌ Error viewing history: {str(e)}")
        input("Press Enter to try again...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        exit()
    except Exception as e:
        print(f"\nFatal error: {str(e)}")
        exit(1)
