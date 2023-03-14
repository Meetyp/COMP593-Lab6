import requests
import hashlib
import os
import subprocess
import time

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    
    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe.sha256'
    resp_msg = requests.get(file_url)
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
    # Extract text file content from response message body
        file_content = resp_msg.text
        # Split the text file content to get hashvalue
        hash_value = file_content.split('*')[0]
        # Print the expected SHA-256 value
        hash_value = hash_value.strip()
        print("Expected sha256 value: " + hash_value)
    return hash_value

def download_installer():
    # Send GET message to download the file
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.exe'
    resp_msg = requests.get(file_url)
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract binary file content from response message body
        file_content = resp_msg.content
    return file_content

def installer_ok(installer_data, expected_sha256):
    # Calculate SHA-256 hash value
    exe_hash = hashlib.sha256(installer_data).hexdigest()
    # Print our exe sha256 value
    print("Our exe sha256 value: " + exe_hash)
    # Matching both the sha256 value 
    if exe_hash == expected_sha256:
        print("Match")
        return True
    else:
        print("Not Match")

def save_installer(installer_data):
    # Building filepath
    get_temp_path = os.getenv('TEMP')
    filename = 'file.exe'
    file_path = os.path.join(get_temp_path, filename)
    # Save the binary file to disk
    with open(file_path, 'wb') as file:
        file.write(installer_data)
    return file_path

def run_installer(installer_path):
    print("Installation begain...")
    print("It will take some moments...")
    print("Please press 'YES' for User Account Control to continue the process.")
    # Run installer silently
    subprocess.run([installer_path, '/L=1033', '/S'], shell=True)
    
def delete_installer(installer_path):
    print("Installation Complete. Enjoy!")
    # Delete the installer
    os.remove(installer_path)

if __name__ == '__main__':
    main()