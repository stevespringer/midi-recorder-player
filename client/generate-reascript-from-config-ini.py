import os
import configparser
import shutil

def read_config_value(config_file, section, key):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config.get(section, key)

def replace_placeholder(file_path, placeholder, replacement):
    with open(file_path, 'r') as file:
        content = file.read()
        content = content.replace(placeholder, replacement)
    with open(file_path.replace('.generated', ''), 'w') as file:
        file.write(content)

def main():
    config_file = 'config.ini'
    section = 'Local'
    key = 'DownloadFolder'
    placeholder = 'DOWNLOADFOLDER'

    download_folder = read_config_value(config_file, section, key)
    target_file = 'reaper/populate-from-download-folder.py'
    generated_target_file = 'reaper/populate-from-download-folder.generated.py'

    shutil.copy(target_file, generated_target_file)

    replace_placeholder(generated_target_file, placeholder, download_folder)
    print(f"File '{generated_target_file}' has been generated with the correct placeholders.")

if __name__ == '__main__':
    main()

