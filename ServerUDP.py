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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('192.168.68.144', 12123)
    server_socket.bind(server_address)
    server_socket.settimeout(60)

    print("UDP server up and listening. (Will auto close in 60 seconds if there is no data sent)")

    try:
        while socket.timeout:
            data, address = server_socket.recvfrom(1024)
            print(f"Received: {data.decode()} from {address}")
            data = data.decode()
            if data[0:1] == "1":
                server_socket.sendto(add_student(data[1:]).encode(), address)
            if data[0:1] == "2":
                server_socket.sendto(display_student(data[1:]).encode(), address)
            if data[0:1] == "3":
                server_socket.sendto(display_student_above_a_score(data[1:]).encode(), address)
            if data[0:1] == "4":
                server_socket.sendto(display_all_students().encode(), address)
            if data[0:1] == "5":
                server_socket.sendto(delete_student(data[1:]).encode(), address)
    except socket.timeout:
        print("Auto closing connection. No data sent in the last 60 seconds.")
        server_socket.close()
        exit(0)

    server_socket.close()
    exit(0)


if __name__ == '__main__':
    server_program()