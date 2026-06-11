import subprocess
import os

password = "admin123"

user_input = input("Enter command: ")

subprocess.run(user_input, shell=True)

print("Done")
