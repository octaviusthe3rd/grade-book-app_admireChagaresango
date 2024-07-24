import getpass
import csv
import os

class Auth:
    def __init__(self):
        self.user_file = 'data/users.csv'
        if not os.path.exists(self.user_file):
            os.makedirs(os.path.dirname(self.user_file), exist_ok=True)
            with open(self.user_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'password'])
        self.users = self.read_users()

    def read_users(self):
        users = {}
        with open(self.user_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                users[row[0]] = row[1]
        return users

    def write_users(self):
        with open(self.user_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password'])
            for username, password in self.users.items():
                writer.writerow([username, password])

    def register(self):
        username = input("Enter a new username: ")
        if username in self.users:
            print("Username already exists.")
            return False
        password = getpass.getpass("Enter a new password: ")
        self.users[username] = password
        self.write_users()
        return True

    def login(self):
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        if username in self.users and self.users[username] == password:
            print("Login successful!")
            return True
        else:
            print("Invalid credentials. Try again.")
            return False