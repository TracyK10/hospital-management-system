# lib/cli.py

from helpers import (
    exit_program,
    helper_1
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
        else:
            print("Invalid choice")


def menu():
    print("\n--- Hospital Management System ---")
    print("0. Exit the program")
    print("2. Manage Patients")
    print("3. Manage Doctors")
    print("4. Manage Appointments")
    print("5. Manage Medical Records")


if __name__ == "__main__":
    main()