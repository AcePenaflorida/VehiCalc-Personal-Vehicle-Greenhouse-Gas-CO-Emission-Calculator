from enum import Enum, auto

# Enums and constants
VALID_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

class VehicleType(Enum):
    CAR = auto()
    MOTORCYCLE = auto()
    VAN = auto()

class FuelType(Enum):
    GASOLINE = auto()
    DIESEL = auto()

# Validation & Utility functions 
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
    if not fuel_type:
        return None
    try:
        return FuelType[fuel_type.upper()]
    except KeyError:
        raise ValueError(f"Invalid fuel type. Must be one of: {[f.name for f in FuelType]} or empty")

def validate_fuel_efficiency(efficiency):
    if efficiency is None:
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


# Manual Unit Test
def run_all_validation_tests():
    test_groups = [
        {
            "label": "Username",
            "func": validate_username,
            "cases": [
                {"input": "ValidUser", "expected": "ValidUser", "case_type": "Happy Case"},
                {"input": "User", "expected": "User", "case_type": "Edge Case"},
                {"input": "@User!", "expected": "Username can only contain letters and numbers", "case_type": "Invalid Case"},
            ]
        },
        {
            "label": "Password",
            "func": validate_password,
            "cases": [
                {"input": "StrongPass", "expected": "StrongPass", "case_type": "Happy Case"},
                {"input": "Passwrd8", "expected": "Passwrd8", "case_type": "Edge Case"},
                {"input": "123", "expected": "Password must be at least 8 characters long", "case_type": "Invalid Case"},
            ]
        },
        {
            "label": "Vehicle Type",
            "func": validate_vehicle_type,
            "cases": [
                {"input": "car", "expected": VehicleType.CAR, "case_type": "Happy Case"},
                {"input": "VaN", "expected": VehicleType.VAN, "case_type": "Edge Case"},
                {"input": "plane", "expected": "Invalid vehicle type. Must be one of: ['CAR', 'MOTORCYCLE', 'VAN']", "case_type": "Invalid Case"},
            ]
        },
        {
            "label": "Fuel Type",
            "func": validate_fuel_type,
            "cases": [
                {"input": "diesel", "expected": FuelType.DIESEL, "case_type": "Happy Case"},
                {"input": 0, "expected": None, "case_type": "Edge Case"},
                {"input": "electric", "expected": "Invalid fuel type. Must be one of: ['GASOLINE', 'DIESEL'] or empty", "case_type": "Invalid Case"},
            ]
        },
        {
            "label": "Fuel Efficiency",
            "func": validate_fuel_efficiency,
            "cases": [
                {"input": 15.5, "expected": 15.5, "case_type": "Happy Case"},
                {"input": None, "expected": None, "case_type": "Edge Case"},
                {"input": -2, "expected": "Fuel efficiency must be a positive number", "case_type": "Invalid Case"},
            ]
        },
        {
            "label": "Distance",
            "func": validate_distance,
            "cases": [
                {"input": 120.0, "expected": 120.0, "case_type": "Happy Case"},
                {"input": 0.1, "expected": 0.1, "case_type": "Edge Case"},
                {"input": 0, "expected": "Distance must be positive", "case_type": "Invalid Case"},
            ]
        },
        {
            "label": "Month",
            "func": validate_month,
            "cases": [
                {"input": "Jan", "expected": "Jan", "case_type": "Happy Case"},
                {"input": "Dec", "expected": "Dec", "case_type": "Edge Case"},
                {"input": "HelloMonth", "expected": f"Invalid month. Must be one of: {VALID_MONTHS}", "case_type": "Invalid Case"},
            ]
        }
    ]

    for group in test_groups:
        print(f"\n=== {group['label']} Validation Tests ===")
        for i, case in enumerate(group["cases"], 1):
            print(f"\nTest Case {i} - {case['case_type']}")
            print(f"Input           : {repr(case['input'])}")
            print(f"Expected Output : {repr(case['expected'])}")
            try:
                result = group["func"](case["input"])
                print(f"Actual Output   : {repr(result)}")
                if result == case["expected"]:
                    print("Result          : ✅ Test Passed")
                else:
                    print("Result          : ❌ Test Failed")
            except ValueError as e:
                print(f"Actual Output   : {repr(str(e))}")
                if str(e) == case["expected"]:
                    print("Result          : ✅ Test Passed")
                else:
                    print("Result          : ❌ Test Failed")


run_all_validation_tests()
