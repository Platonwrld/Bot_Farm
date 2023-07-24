from database.interfaces import AdminInterface


while True:
    username = input("Enter username: ")
    password = input("Password: ")
    AdminInterface.create_model(
        username,
        password
    )