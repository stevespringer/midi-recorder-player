import os
import configparser

def read_config_value(config_file, section, key):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.get(section, key)

def get_file_contents(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, contents):
    with open(file_path, 'w') as file:
        file.write(contents)

def main():
    config_file = 'config.ini'
    section = 'Local'
    key = 'DownloadFolder'
    placeholder = 'DOWNLOADFOLDER'

    download_folder = read_config_value(config_file, section, key)
    template_file = 'reaper/populate-from-download-folder.py'

    contents = get_file_contents(template_file)
    contents = contents.replace(placeholder, download_folder)

    generated_target_file = 'reaper/populate-from-download-folder.generated.py'
    write_file(generated_target_file, contents)

    print(f"File '{generated_target_file}' has been generated with the correct placeholders.")

if __name__ == '__main__':
    main()

