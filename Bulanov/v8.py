import tkinter as tk
from tkinter import filedialog

# Create the window
window = tk.Tk()
window.title('Password Encryption/Decryption App')
window.geometry('400x400')

string = "abcdefghijklmnopqrstuvwxyz "

# Functions
def encrypt():
    # Get the password
    password = entry1.get()
    # Get the C
    c = entry2.get()
    # Encrypt the password
    encrypted_password = ""
    for i in range(len(password)):
        p_ind = ord(password[i]) - ord('a')
        c_ind = ord(c[i % len(c)]) - ord('a')
        encrypted_password += chr(ord('a') + (p_ind + c_ind) % 26)
    # Print the encrypted password
    label4 = tk.Label(text=encrypted_password)
    label4.grid(row=3, column=0)


def decrypt():
    # Get the password
    password = entry1.get()
    # Get the C
    c = entry2.get()
    # Decrypt the password
    decrypted_password = ""
    for i in range(len(password)):
        p_ind = ord(password[i]) - ord('a')
        c_ind = ord(c[i % len(c)]) - ord('a')
        decrypted_password += chr(ord('a') + (p_ind - c_ind) % 26)
    # Print the decrypted password
    label5 = tk.Label(text=decrypted_password)
    label5.grid(row=3, column=0)


def load_file():
    # Open the file
    file_path = filedialog.askopenfilename()
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    # Print the content
    label6 = tk.Label(text=content)
    label6.grid(row=3, column=0)


def save_file():
    # Get the password
    password = entry1.get()
    # Get the C
    c = entry2.get()
    # Encrypt the password
    encrypted_password = ""
    for i in range(len(password)):
        p_ind = ord(password[i]) - ord('a')
        c_ind = ord(c[i % len(c)]) - ord('a')
        encrypted_password += chr(ord('a') + (p_ind + c_ind) % 26)
    # Open the file
    file_path = filedialog.asksaveasfilename()
    # Write the encrypted password to the file
    with open(file_path, 'w') as f:
        f.write(encrypted_password)


# Create Labels
label1 = tk.Label(text='Password: ')
label2 = tk.Label(text='C: ')
label3 = tk.Label(text='Result: ')

# Create Input Boxes
entry1 = tk.Entry()
entry2 = tk.Entry()

# Create Buttons
encrypt_button = tk.Button(text='Encrypt', command=encrypt)
decrypt_button = tk.Button(text='Decrypt', command=decrypt)
load_button = tk.Button(text='Load File', command=load_file)
save_button = tk.Button(text='Save File', command=save_file)

# Place Labels
label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=2, column=0)

# Place Input Boxes
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

# Place Buttons
encrypt_button.grid(row=2, column=1)
decrypt_button.grid(row=2, column=2)
load_button.grid(row=3, column=1)
save_button.grid(row=3, column=2)

# Run the main loop
window.mainloop()
