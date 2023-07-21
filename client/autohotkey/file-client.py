import os
import base64
import socket
import shutil
import argparse

def delete_folder_contents(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def decode_file_contents(encoded_contents):
    decoded_contents = base64.b64decode(encoded_contents)
    return decoded_contents

def recreate_files_from_tcp(connection_details, first_file_of_session, output_directory):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(connection_details)

        group_number = 0
        request = f"GETFILES {first_file_of_session}"
        sock.sendall(request.encode('utf-8'))

        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk

    delete_folder_contents(output_directory)

    lines = data.decode('utf-8').split('\n')

    for i in range(0, len(lines)-1, 2):
        file_name = lines[i].strip()
        encoded_contents = lines[i+1].strip()

        file_path = os.path.join(output_directory, file_name)
        decoded_contents = decode_file_contents(encoded_contents)

        with open(file_path, 'wb') as output_file:
            output_file.write(decoded_contents)

def list_recent_file_groups(connection_details, num_days, out_file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(connection_details)

        request = f"LISTFILES {num_days}"
        sock.sendall(request.encode('utf-8'))

        data = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk

        text_file = open(out_file, "w")
        text_file.write(data.decode('utf-8'))
        text_file.close()

def get_command(connection_details, args):
    session_id = args.sessionid
    output_directory = args.outputdirectory
    recreate_files_from_tcp(connection_details, session_id, output_directory)

def list_command(connection_details, args):
    num_days = args.numdays
    out_file = args.outfile
    list_recent_file_groups(connection_details, num_days, out_file)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Session Manager')
    parser.add_argument('--host', type=str, help='Host name or ip of the server to connect to', required=True)
    parser.add_argument('--port', type=int, help='Port of the server to connect to', required=True)
    subparsers = parser.add_subparsers(dest='command')

    # 'get' command
    get_parser = subparsers.add_parser('get', help='Get a session')
    get_parser.add_argument('sessionid', type=str, help='Filename of the first item in the session')
    get_parser.add_argument('outputdirectory', type=str, help='Local folder to download session files to')    

    # 'list' command
    list_parser = subparsers.add_parser('list', help='List sessions')
    list_parser.add_argument('numdays', type=int, help='Number of past days to retrieve sessions for')
    list_parser.add_argument('outfile', type=str, help='Local file path to write the session list csv to')

    args = parser.parse_args()

    connection_details = (args.host, args.port)

    if args.command == 'get':
        get_command(connection_details, args)
    elif args.command == 'list':
        list_command(connection_details, args)
    else:
        print('Invalid command')

