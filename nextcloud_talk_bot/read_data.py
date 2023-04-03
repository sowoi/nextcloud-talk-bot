from cryptography.fernet import Fernet

def read_nextcloud_data():
    # Read the .nextclouddata file and extract the data
    data = {}
    with open(".nextclouddata", "r") as data_file:
        for line in data_file:
            key, value = line.strip().split("::")
            data[key] = value

            
    with open(".decode", "r") as decode_file:
        decode_password = decode_file.readline()
        f = Fernet(decode_password)


    # Password decryption
    
    with open(".password", "r") as password_file:
        encrypted_password = password_file.readline()
        decrypted_password = f.decrypt(encrypted_password).decode()
        data['PASSWORD'] = decrypted_password

    return data
