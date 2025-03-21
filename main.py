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
