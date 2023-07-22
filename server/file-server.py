import os
import base64
import socket
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

def get_recent_file_groups(directory):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Sort the files by their modification time in descending order
    sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

    groups = []
    current_group = []
    prev_modification_time = None

    for file_name in sorted_files:
        file_path = os.path.join(directory, file_name)
        modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        timestamp = file_name.split(".")[0]
        creation_time = datetime.strptime(timestamp, "%Y%m%d%H%M%S")

        if prev_modification_time is None or prev_modification_time - creation_time <= timedelta(seconds=1000):
            current_group.append({'filename': file_name, 'creation_time': creation_time, 'modification_time': modification_time})
        else:
            groups.append(current_group)
            current_group = [{'filename': file_name, 'creation_time': creation_time, 'modification_time': modification_time}]

        prev_modification_time = modification_time

    groups.append(current_group)

    return groups

def group_file_groups_by_date(directory):
    # Call get_recent_file_groups to get the file groups
    file_groups = get_recent_file_groups(directory)

    # Create a dictionary to store the grouped file groups by date
    grouped_file_groups = defaultdict(list)

    # Iterate over each file group and group them by date
    for file_group in file_groups:
        if len(file_group) > 0:
            first_file = file_group[0]
            creation_time = first_file['creation_time']
            date = creation_time.date()
            grouped_file_groups[date].append(file_group)

    return grouped_file_groups

def format_group(group):
        first_file = group[-1]
        last_file = group[0]
        creation_time = first_file['creation_time']
        modification_time = last_file['modification_time']

        time_difference = modification_time - creation_time
        minutes = time_difference.total_seconds() // 60
        seconds = time_difference.total_seconds() % 60

        file_count = len(group)

        date = creation_time.strftime("%d/%-m")
        start_time = creation_time.strftime("%H:%M")
        duration = "%02d:%02d" % (minutes, seconds)
        return (date, start_time, duration, file_count, first_file['filename'])

def get_groups_from_recent_days(file_directory, num_days):
    date_set = set()
    for group in get_recent_file_groups(file_directory):
        item = format_group(group)
        date_set.add(item[0])
        if(len(date_set) > num_days):
            return
        yield item

def encode_file_contents(file_path):
    with open(file_path, 'rb') as file:
        file_contents = file.read()
        encoded_contents = base64.b64encode(file_contents).decode('utf-8')
    return encoded_contents

def handle_get_files_request(directory, requested_group):
    recent_file_groups = get_recent_file_groups(directory)
    group = None

    for session in recent_file_groups:
        if session[-1]['filename'] == requested_group:
            group = session
            break

    if group is None:
        return "Invalid group identifier."

    response = ""

    for item in group:
        file_name = item['filename']
        file_path = os.path.join(directory, file_name)
        encoded_contents = encode_file_contents(file_path)
        response += file_name + '\n'
        response += encoded_contents + '\n'

    return response


def groups_to_csv(groups):
    records = []
    for group in groups:
        records.append(','.join(str(i) for i in group))
    return '\n'.join(records)

def listen_for_get_files_requests(port, directory):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind(('0.0.0.0', port))
        server_sock.listen()

        print("Server listening on port", port)

        while True:
            client_sock, addr = server_sock.accept()
            print("Accepted connection from", addr)

            request = client_sock.recv(4096).decode('utf-8')
            print("Received request:", request)

            if request.startswith("GETFILES"):
                try:
                    requested_group = request.split()[1]
                    response = handle_get_files_request(directory, requested_group)
                except (IndexError):
                    response = "Invalid request format."

                client_sock.sendall(response.encode('utf-8'))
            elif request.startswith("LISTFILES"):
                try:
                    requested_num_days = int(request.split()[1])
                    response = groups_to_csv(get_groups_from_recent_days(directory, requested_num_days))
                except (IndexError, ValueError):
                    response = "Invalid request format."                
                
                client_sock.sendall(response.encode('utf-8'))

            client_sock.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Session Manager')
    parser.add_argument('folder', type=str, help='The path to the folder containing the midi recordings to serve')
    parser.add_argument('port', type=int, help='TCP Port to listen on')

    args = parser.parse_args()

    listen_for_get_files_requests(args.port, args.folder)


