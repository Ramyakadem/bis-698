import tkinter as tk
import mysql.connector
import random
from tkinter import messagebox

# Connect to MySQL database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="BIS_698_Group2"
    )
except Exception as e:
    messagebox.showerror("Database Connection Error", f"Failed to connect to the database: {e}")
    exit()

# Define colors for the application
background_color = '#F9F9F9'  # Light gray similar to iOS Notes
text_color = '#333333'  # Dark gray for text
button_color = '#2962FF'  # Blue for buttons

# Define a list of motivational quotes
motivational_quotes = [
    "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle.",
    "Start where you are. Use what you have. Do what you can.",
    "Don't be afraid to fail. Not failing is the biggest failure of all.",
    "The journey of a thousand miles begins with a single step.",
    "Believe you can and you're halfway there.",
]

# Function to handle user registration
def register_user():
    username = registration_username_entry.get()
    password = registration_password_entry.get()
    email = registration_email_entry.get()

    if username and password and email:
        cursor = db.cursor()

        try:
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            # Register the user if username doesn't exist
            if not existing_user:
                cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
                db.commit()
                messagebox.showinfo("Registration", "Registration successful!")
                registration_username_entry.delete(0, 'end')
                registration_password_entry.delete(0, 'end')
                registration_email_entry.delete(0, 'end')
                registration_window.destroy()  # Close registration window
            else:
                messagebox.showerror("Registration", "Username already exists.")

        except mysql.connector.errors.ProgrammingError as e:
            messagebox.showerror("Registration Error", f"Invalid SQL query. Check the placeholder parameters: {e}")

        cursor.close()
    else:
        messagebox.showerror("Registration", "Please fill in all the fields.")

# Function to handle user login
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    cursor = db.cursor()

    try:
        # Check user credentials against the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            messagebox.showinfo("Login", "Login successful!")
            root.destroy() 
        else:
            messagebox.showerror("Login", "Invalid username or password.")
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

    except mysql.connector.errors.ProgrammingError as e:
        messagebox.showerror("Login Error", f"Invalid SQL query. Check the placeholder parameters: {e}")

    cursor.close()

# Function to open the registration screen
def open_registration_screen():
    global registration_window, registration_username_entry, registration_password_entry, registration_email_entry

    registration_window = tk.Toplevel(root)
    registration_window.title('Registration')
    registration_window.geometry('600x400')
    registration_window.configure(bg='#F6F6F6')

    welcome_label_registration = tk.Label(registration_window, text='Welcome to Academic Goal Tracking Application Registration', bg='maroon', font=('cursive', 16, 'bold'), fg='yellow',  width=30)  # Set text color to white
    welcome_label_registration.pack(side='top', fill='x', padx=30, pady=30)

    # Labels and Entry widgets for registration
    registration_username_label = tk.Label(registration_window, text='Username:', bg='#F6F6F6', fg='black')
    registration_username_entry = tk.Entry(registration_window)

    registration_password_label = tk.Label(registration_window, text='Password:', bg='#F6F6F6', fg='black')
    registration_password_entry = tk.Entry(registration_window, show='*')

    registration_email_label = tk.Label(registration_window, text='Email:', bg='#F6F6F6', fg='black')
    registration_email_entry = tk.Entry(registration_window)

    # Button for registration
    register_button = tk.Button(registration_window, text='Register', command=register_user)

    # Layout for registration screen
    registration_username_label.pack(pady=5)
    registration_username_entry.pack(pady=5)
    registration_password_label.pack(pady=5)
    registration_password_entry.pack(pady=5)
    registration_email_label.pack(pady=5)
    registration_email_entry.pack(pady=5)
    register_button.pack(pady=15)


# Function to display a random motivational quote
def show_motivational_quote():
    quote = random.choice(motivational_quotes)
    quote_label.config(text=quote)
    root.after(5000, show_motivational_quote)  # Automatically show a new quote every 5 seconds

# Function to start showing motivational quotes
def start_motivational_quotes():
    show_motivational_quote()

# Create the main window
root = tk.Tk()
root.title('Welcome to Academic Goal Tracking')
root.geometry('500x300')
root.configure(bg='#F6F6F6')  # Set the background color to a light gray similar to iOS Notes

# Create a rectangle for the motivational quote
quote_rectangle = tk.Frame(root, width=300, height=200, bg='#F6F6F6')
quote_rectangle.place(x=10, y=150)  # Align the rectangle to the middle bottom of the screen

# Labels and Entry widgets for registration and login
welcome_label = tk.Label(root, text='Welcome to Academic Goal Tracking Application', bg='maroon', font=('cursive', 16, 'bold'), fg='yellow',  width=30)  # Set text color to white
welcome_label.pack(side='top', fill='x', padx=20, pady=30)
username_label = tk.Label(root, text='Username:', bg='#F6F6F6', fg='black')  # Set text color to black
username_entry = tk.Entry(root)
password_label = tk.Label(root, text='Password:', bg='#F6F6F6', fg='black')  # Set text color to black
password_entry = tk.Entry(root, show='*')
quote_label = tk.Label(quote_rectangle, text='', wraplength=400, justify='center', bg='maroon', font=('cursive', 12, 'bold'), fg='yellow')  # Set text color to black

# Create a frame to hold the "Login" and "Register" buttons
buttons_frame = tk.Frame(root, bg='#F6F6F6')
buttons_frame.pack(side='bottom')  # Align the frame to the bottom of the window

# Create buttons for registration and login within the buttons frame
register_button = tk.Button(buttons_frame, text='Register', command=open_registration_screen)
login_button = tk.Button(buttons_frame, text='Login', command=login_user)

# Pack layout for buttons in the middle
register_button.pack(side='left', padx=10, pady=30)
login_button.pack(side='left', padx=15, pady=30)

# Pack layout for other elements
welcome_label.pack(pady=5)
username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
quote_label.pack(pady=20)
quote_rectangle.pack()

# Display an initial motivational quote and start the automatic quote rotation
start_motivational_quotes()

root.mainloop()
