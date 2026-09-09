 #####################################
 # Faker I.C.2 # Aseel Ali, 2026     #
 # ----------------------------------#
 # aseelali18@usf.edu # (C) 2026     #
 # ----------------------------------#
 # Create synthetic patient data     #
 # using the Faker lib and random #s #
 #                                   #
 # For research and educational use  #
 # only, not for clinical decisions. #
 #####################################

# Import libs
import json
import os
from faker import Faker
from anonymate.anonymizer import Anonymizer
from cryptography.fernet import Fernet

# load or create a persistent encryption key
KEY_FILE = "encryption.key"

if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        encryption_key = f.read()
else:
    encryption_key= Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(encryption_key)

# Initialize the Faker engine and Anonymizer engine
fake = Faker()
anonymizer = Anonymizer(encryption_key=encryption_key)

# Prompt user for data length
length = int(input("Enter the desired number of synthetic patient datasets you would like: "))

# Initialize Data Variable
data = []

# Call fake_len function to generate names
for _ in range(length):
    data.append(fake.word())

# Print data to terminal
print ("Unencrypted Data:")
print(data)

# Turn data into a string
data_str = json.dumps (data, default=str)

# Run anonymizer
secure_data = anonymizer.encrypt(data_str)

# how Enccrypted data to User
print ("Encrypted Data:")
print(secure_data)

# Create boolean question function for file write
def write_to_question(question: str) -> bool:
    while True:
        write_decision = input(f"{question} (y/n): "). strip().lower()
        if write_decision in ("y", "yes"):
            return True
        elif write_decision in ("n", "no"):
            return False

        print("Invalid input. Please enter 'y' or 'n'")

# ask if they would like to write data to file
write_bool = write_to_file_question ("would you like to write this data to file")

# write data if/else logic
if write_bool == True:
    custom_name = input ("Enter the name of the file. (no special characters): ")

    file_name = (f"{custom_name}.txt")

    with open(file_name, "w", encoding="utf-8") as file:
        file.write (secure_data)

    print(f"Saved to {fil_name}")
else:
        print ("Data not saved. All data will be lost when application is closed.")
