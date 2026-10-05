import secrets
import sys
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


try:
    with open("salt.key", "rb") as salt_file:
        salt = salt_file.read()
except FileNotFoundError:

    salt = secrets.token_bytes(16)
    with open("salt.key", "wb") as salt_file:
        salt_file.write(salt)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=600000
)

master_password = "MasterPassword" # If you have people that love to sneak into your pc (physical), then follow the hashing guide!

raw_key = kdf.derive(master_password.encode())

url_safe_key = base64.urlsafe_b64encode(raw_key)

cipher = Fernet(url_safe_key)

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789=-~!@#$%^&()+[]|;:',.<>/?"
print("---Welcome to King Noob's Password Manager!---")

login = input("Enter the master password. ")
if login == master_password:
    print("Access granted! Welcome to the program! ")
else:
    print("Access denied! Maybe you typed it wrong, or you are a bad guy! ")
    sys.exit()

#Main loop
while True:

    #Password manager options
    choice = input("Do you want to (g)enerate a secure password, (a)dd a password to save, or(v)iew saved passwords?: ").lower()
    #View saved passwords
    if choice == "v":
        try:
            with open("password.txt", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    name, scrambled_text = line.strip().split(": ")
                    bytes_scrambled = scrambled_text.encode()
                    decrypted_bytes = cipher.decrypt(bytes_scrambled)
                    decrypted_password = decrypted_bytes.decode()
                    print(f"{name}: {decrypted_password}")
                print()
        except FileNotFoundError:
            print("Hmmm, it seems like you didn't save anything or you deleted them!")

        deletion = input("Would you like to delete one of the saved passwords? (y/n): ").lower()

        #Delete a saved password
        if deletion == "y":
            name_to_delete = input("Enter the name of the password you want to delete: ")
            try:
                with open("password.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                with open("password.txt", "w", encoding="utf-8") as f:
                    for line in lines:
                        if not line.startswith(name_to_delete + ":"):
                            f.write(line)
                if name_to_delete in [line.split(":")[0] for line in lines]:
                    print(f"Password '{name_to_delete}' deleted successfully.")
                else: 
                    print(f"No password found with the name '{name_to_delete}'. You did a mistake maybe, or you simply deleted it already!")
            except FileNotFoundError:
                print("Hmmm, it seems like you didn't save anything or you deleted them!")

        generate_another = input("Would you like to go back to the start? (y/n): ").lower() 
        
        if generate_another == "n":
            print("Goodbye!")
            break
    
    elif choice == "a":
        print("Alrighty, let's see what you got.")
        manual_password = input("Enter your password right here!: ")
        manual_name = input("Enter the name of your password!: ")
        with open("password.txt", "r", encoding="utf-8") as f:
            if manual_name in [line.split(":")[0] for line in f.readlines()]:
                print(f"A password with the name '{manual_name}' already exists! You might wanna delete the existing one!")
            elif manual_name not in [line.split(":")[0] for line in f.readlines()]:
                bytes_password = manual_password.encode()
                scrambled_password = cipher.encrypt(bytes_password)
                scrambled_text = scrambled_password.decode()
                with open("password.txt", "a", encoding="utf-8") as f:
                    f.write(f"{manual_name}: {scrambled_text}\n")
                print(f"Password '{manual_name}' militarily encrypted and saved successfully! ")

        generate_another = input("Would you like to go back to the start? (y/n): ").lower() 

        if generate_another == "n":
            print("Goodbye!")
            break

    elif choice == "g":
        print("Let's generate a secure password for you!")
        try:
            length = int(input("Enter password length: "))
        except ValueError:
            print("Please enter a valid whole number.")
            continue

        if length < 8:
            print("Password length must be at least 8 characters.")
            continue
        if length > 128:
            print("Password length must not exceed 128 characters.")
            continue

        password = "".join(secrets.choice(chars) for _ in range(length))
        print("Your secure password is: " + password)

        save_choice = input("Would you like to save this password to a file? (y/n): ").lower()

        if save_choice == "y":
            name = input("Enter the name of the password: ")
            with open("password.txt", "r", encoding="utf-8") as f:
                if name in [line.split(":")[0] for line in f.readlines()]:
                    print(f"A password with the name '{name}' already exists! You might wanna delete the existing one!")
                elif name not in [line.split(":")[0] for line in f.readlines()]:
                    bytes_password = password.encode()
                    scrambled_password = cipher.encrypt(bytes_password)
                    scrambled_text = scrambled_password.decode()
                    with open("password.txt", "a", encoding="utf-8") as f:
                        f.write(f"{name}: {scrambled_text}\n")
                        print("Password saved to password.txt")
        elif save_choice == "n":
            print("Good luck remembering it! Make sure to write it down somewhere safe.")

        generate_another = input("Would you like to go back to the start? (y/n): ").lower() 
    
        if generate_another == "n":
            print("Goodbye!")
            break