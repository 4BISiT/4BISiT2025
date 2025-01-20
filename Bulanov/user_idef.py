import random
import tkinter as tk
from tkinter import messagebox

# Global Variables
user_list = ['superuser', 'test']
user_details = {
    'superuser': {
        'handshake': '1+2',
        'password': '3',
        'args': {
            'a': 1,
            'b': 2,
            'c': 3
        }
    },
    'test': {
        'handshake': '1+1',
        'password': '2',
        'args': {
            'a': 10,
            'b': 20,
            'c': 30
        }
    }
}

# Main window
root = tk.Tk()
root.title('Command Processor')


# Functions
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username not in user_list:
        messagebox.showerror('Error', 'Username does not exist')
        return

    if username and password == "":
        label_password.config(text=("Handshake: " + user_details[username]['handshake'] + " ?"))
        return

    if user_details[username]['password'] != password:
        messagebox.showerror('Error', 'Incorrect password')
        return

    if username == 'superuser':
        show_superuser_window()
    else:
        show_user_window(username)


entry_a = tk.Entry()
entry_b = tk.Entry()
entry_c = tk.Entry()


def show_superuser_window():
    top = tk.Toplevel()
    top.title('Superuser Window')

    # Widgets
    label_username = tk.Label(top, text='Username')
    # label_password = tk.Label(top, text='Password')
    label_a = tk.Label(top, text='Argument A')
    label_b = tk.Label(top, text='Argument B')
    label_c = tk.Label(top, text='Argument C')

    entry_username = tk.Entry(top)
    # entry_password = tk.Entry(top, show='*')
    entry_a = tk.Entry(top)
    entry_b = tk.Entry(top)
    entry_c = tk.Entry(top)

    button_add = tk.Button(top, text='Add User', command=add_user)
    button_remove = tk.Button(top, text='Delete User', command=delete_user)
    button_change_password = tk.Button(top, text='Change Handshake', command=change_password)
    button_change_args = tk.Button(top, text='Change Args', command=change_args)
    button_view_user_info = tk.Button(top, text='View User Info', command=view_user_info)

    # Layout
    label_username.grid(row=0, column=0)
    label_password.grid(row=1, column=0)
    label_a.grid(row=2, column=0)
    label_b.grid(row=3, column=0)
    label_c.grid(row=4, column=0)

    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)
    entry_a.grid(row=2, column=1)
    entry_b.grid(row=3, column=1)
    entry_c.grid(row=4, column=1)

    button_add.grid(row=5, column=0, columnspan=2, pady=10)
    button_remove.grid(row=6, column=0, columnspan=2)
    button_change_password.grid(row=7, column=0, columnspan=2)
    button_change_args.grid(row=8, column=0, columnspan=2)
    button_view_user_info.grid(row=9, column=0, columnspan=2)


def show_user_window(username):
    top = tk.Toplevel()
    top.title(f'{username} Window')

    # Widgets
    label_password = tk.Label(top, text='Password')
    label_a = tk.Label(top, text='Argument A')
    label_b = tk.Label(top, text='Argument B')
    label_c = tk.Label(top, text='Argument C')

    entry_password = tk.Entry(top, show='*')
    entry_a = tk.Entry(top)
    entry_b = tk.Entry(top)
    entry_c = tk.Entry(top)

    button_change_password = tk.Button(top, text='Change Password', command=change_password)
    button_change_args = tk.Button(top, text='Change Args', command=change_args)
    button_view_user_info = tk.Button(top, text='View User Info', command=view_user_info)

    # Layout
    label_password.grid(row=0, column=0)
    label_a.grid(row=1, column=0)
    label_b.grid(row=2, column=0)
    label_c.grid(row=3, column=0)

    entry_password.grid(row=0, column=1)
    entry_a.grid(row=1, column=1)
    entry_b.grid(row=2, column=1)
    entry_c.grid(row=3, column=1)

    button_change_password.grid(row=4, column=0, columnspan=2, pady=10)
    button_change_args.grid(row=5, column=0, columnspan=2)
    button_view_user_info.grid(row=6, column=0, columnspan=2)


def add_user():
    username = entry_username.get()
    password = entry_password.get()
    a = entry_a.get()
    b = entry_b.get()
    c = entry_c.get()

    if username in user_list:
        messagebox.showerror('Error', 'Username already exists')
        return

    if not username or not password or not a or not b or not c:
        messagebox.showerror('Error', 'Please enter all fields')
        return

    user_list.append(username)
    user_details[username] = {
        'password': password,
        'args': {
            'a': a,
            'b': b,
            'c': c
        }
    }
    messagebox.showinfo('Info', 'User added successfully')


def delete_user():
    username = entry_username.get()

    if username not in user_list:
        messagebox.showerror('Error', 'Username does not exist')
        return

    user_list.remove(username)
    del user_details[username]
    messagebox.showinfo('Info', 'User deleted successfully')


def change_password():
    username = entry_username.get()
    # password = entry_password.get()

    if username not in user_list:
        messagebox.showerror('Error', 'Username does not exist')
        return

    user_details[username]['handshake'] = str(random.randint(1, 10) % 10) + "+" + str(random.randint(1,20) % 20)
    user_details[username]['password'] = str(eval(user_details[username]['handshake']))
    messagebox.showinfo('Info', f"Password changed successfully!\nNew handshake: {user_details[username]['handshake']}")


def change_args():
    username = entry_username.get()
    a = entry_a.get()
    b = entry_b.get()
    c = entry_c.get()

    if username not in user_list:
        messagebox.showerror('Error', 'Username does not exist')
        return

    if not a or not b or not c:
        messagebox.showerror('Error', 'Please enter all fields')
        return

    user_details[username]['args']['a'] = a
    user_details[username]['args']['b'] = b
    user_details[username]['args']['c'] = c
    messagebox.showinfo('Info', 'Args changed successfully')


def view_user_info():
    username = entry_username.get()

    if username not in user_list:
        messagebox.showerror('Error', 'Username does not exist')
        return

    password = user_details[username]['handshake']
    args = user_details[username]['args']
    messagebox.showinfo('Info', f'Handshake: {password}, Args: {args}')


# Widgets
label_username = tk.Label(root, text='Username')
label_password = tk.Label(root, text='Handshake')

entry_username = tk.Entry(root)

label_ans = tk.Label(root, text='Answer')
entry_password = tk.Entry(root, show='*')

button_login = tk.Button(root, text='Login', command=login)

# Layout
label_username.grid(row=0, column=0)
label_password.grid(row=1, column=0)

entry_username.grid(row=0, column=1)

label_ans.grid(row=2, column=0)
entry_password.grid(row=2, column=1)

button_login.grid(row=3, column=0, columnspan=3, pady=10)

# Run main loop
root.mainloop()