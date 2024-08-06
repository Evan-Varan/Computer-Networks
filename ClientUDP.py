import socket
import sys
def display_options():
    print("Choose an option:")
    print("1. Add a new student to the database.")
    print("2. Display a specific students information.")
    print("3. Display all students above a specific score.")
    print("4. Display all students.")
    print("5. Delete a student ID from the database.")
    print("6. Exit Program.")
def add_student():
    while True:
        student_ID = input("Enter a 6-digit student ID number: ")
        if student_ID.isdigit() and len(student_ID) == 6:
            break
        else:
            print("The entered data was incorrect. Please try again.")

    while True:
        student_first_name = input("Enter the students first name that is less than 10 characters: ")
        if len(student_first_name) < 10:
            break
        else:
            print("The entered data was incorrect. Please try again.")

    while True:
        student_last_name = input("Enter the students last name that is less than 10 characters: ")
        if len(student_last_name) < 10:
            break
        else:
            print("The entered data was incorrect. Please try again.")

    while True:
        student_score = input("Enter the students score (0-100): ")
        if student_score.isdigit() and 100 >= int(student_score) >= 0 and (not student_score.startswith("0") or student_score == "0"):
            break
        else:
            print("The entered data was incorrect. Please try again.")

    data = student_ID + " " + student_first_name + " " + student_last_name + " " + student_score
    return data
def display_student():
    while True:
        student_ID = input("Enter a 6-digit student ID number: ")
        if student_ID.isdigit() and len(student_ID) == 6:
            break
        else:
            print("The entered data was incorrect. Please try again.")

    return student_ID
def delete_student():
    while True:
        student_ID = input("Enter a 6-digit student ID number: ")
        if student_ID.isdigit() and len(student_ID) == 6:
            break
        else:
            print("The entered data was incorrect. Please try again.")

    return student_ID


def try_send_data(data, client_socket, server_address):
    try:
        client_socket.sendto(data, server_address)
        msg, server = client_socket.recvfrom(1024)
        print(msg.decode())

    except socket.timeout:
        print("No response received from the server within the timeout period. (10 seconds)")
        exit(0)
    except OSError as e:
        print("Failed to send data to the server. Please check your port and IP.")
        exit(0)
    except Exception as e:
        print("Failed to send data to the server. Please check your port and IP.")
        exit(0)
def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(10)

    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    if port < 10000 or port > 15000:
        print("Invalid port number. Port must be between 10000 and 15000. Please try again. ")
        exit(0)

    server_address = (host, port)



    user_input = 0

    while (user_input != '6') and (user_input != '7'):
        display_options()
        user_input = input("Enter your choice: ")

        if user_input == '1':
            try_send_data(("1" + add_student()).encode(), client_socket, server_address)

        elif user_input == '2':
            try_send_data(("2" + display_student()).encode(), client_socket, server_address)

        elif user_input == '3':
            while True:
                student_score = input("Enter the students score (0-100): ")
                if student_score.isdigit() and 100 >= int(student_score) >= 0 and (
                        not student_score.startswith("0") or student_score == "0"):
                    break
                else:
                    print("The entered data was incorrect. Please try again.")

            try_send_data(("3" + student_score).encode(), client_socket, server_address)

        elif user_input == '4':
            try_send_data("4".encode(), client_socket, server_address)

        elif user_input == '5':
            try_send_data(("5" + delete_student()).encode(), client_socket, server_address)

        elif user_input == '6':
            exit(0)
        else:
            print("Invalid choice, Try again!")

    client_socket.close()


if __name__ == '__main__':
    client_program()
