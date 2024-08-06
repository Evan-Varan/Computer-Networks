import socket
import sys

def add_student(data):
    student_ID = data[1:7]
    with open('Students.txt', 'r') as file:
        for line in file:
            if student_ID in line:
                return "Student already exists with that ID."

    with open('Students.txt', 'a') as file:
        file.write(data + "\n")
    return "Added " + data + " to database."

def display_student(data):
    with open('Students.txt', 'r') as file:
        for line in file:
            if data in line:
                return line.strip()
        return 'No student found with that ID.'

def display_student_above_a_score(data):
    to_return = ''
    with open('Students.txt', 'r') as file:
        for line in file:
            index = line.rfind(' ')
            score = line[index+1:].strip()
            if int(score) > int(data):
                to_return += line
    if to_return == '':
        return "No students above that grade."
    else:
        return to_return

def display_all_students():
    to_return = ''
    with open('Students.txt', 'r') as file:
        for line in file:
            to_return += line.strip() + "\n"
    if to_return == '':
        return "No students in file."
    else:
        return to_return

def delete_student(data):
    removed_student = False
    removed_student_data= ""
    with open('Students.txt', "r") as file:
        lines = file.readlines()
    with open('Students.txt', "w") as file:
        for line in lines:
            if data not in line:
                file.write(line)
            else:
                removed_student = True
                removed_student_data = line
    if removed_student:
        return "Removed " + removed_student_data + " from database."
    else:
        return "No student found with that ID to remove."

def server_program():
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    host = '0.0.0.0'
    port = int(sys.argv[1])

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Listening for incoming connections on port", port)

    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    data = 0
    while data != "6":
        data = conn.recv(1024).decode()
        if data[0:1] == "1":
            conn.send(add_student(data[1:]).encode())
        if data[0:1] == "2":
            conn.send(display_student(data[1:]).encode())
        if data[0:1] == "3":
            conn.send(display_student_above_a_score(data[1:]).encode())
        if data[0:1] == "4":
            conn.send(display_all_students().encode())
        if data[0:1] == "5":
            conn.send(delete_student(data[1:]).encode())
        if data[0:1] == "6":
            print("Closing Connection...")
            conn.close()
            exit(0)

    conn.close()
    exit(0)


if __name__ == '__main__':
    server_program()