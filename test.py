import tkinter as tk
import mysql.connector
import random
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText

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
background_color = '#F9F9F9'
text_color = '#333333'
button_color = '#2962FF'
highlight_color = '#407BFF'

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
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

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
                send_registration_email(email)
                messagebox.showinfo("Registration", "Registration successful! Please check your email for confirmation.")
            else:
                messagebox.showerror("Registration", "Username already exists.")

        except mysql.connector.errors.ProgrammingError as e:
            messagebox.showerror("Registration Error", f"Invalid SQL query. Check the placeholder parameters: {e}")

        cursor.close()
    else:
        messagebox.showerror("Registration", "Please fill in all the fields.")

# Function to send a registration confirmation email
def send_registration_email(email):
    try:
        smtp_server = "smtp.gmail.com"  # Set your SMTP server
        smtp_port = 587  # Set your SMTP port
        sender_email = "academictracker698@gmail.com"  # Set your sender email
        sender_password = "BIS698Group2"  # Set your sender email password
        subject = "Registration Confirmation"
        message = "Thank you for registering with Academic Goal Tracking. Your registration is confirmed."

        # Create a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Create an email message
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = email

        # Send the email
        server.sendmail(sender_email, [email], msg.as_string())
        server.quit()

    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send the registration confirmation email: {e}")

# Function to handle user login
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    cursor = db.cursor()

    try:
        # Check user credentials against the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()

        # Close the database connection
        db.close()

        if result:
            user_id = result[0]
            messagebox.showinfo("Login", "Login successful!")
            root.destroy()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    except mysql.connector.errors.ProgrammingError as e:
        messagebox.showerror("Login Error", f"Invalid SQL query. Check the placeholder parameters: {e}")

    cursor.close()

# Define a function to display a random motivational quote
def show_motivational_quote():
    quote = random.choice(motivational_quotes)
    quote_label.config(text=quote)
    root.after(5000, show_motivational_quote)

# Define a function to start showing motivational quotes
def start_motivational_quotes():
    show_motivational_quote()

# Create the main window
root = tk.Tk()
root.title('Welcome to Academic Goal Tracking')
root.geometry('500x350')
root.configure(bg='#F6F6F6')

# Create a rectangle for the motivational quote
quote_rectangle = tk.Frame(root, width=400, height=200, bg='#F6F6F6')
quote_rectangle.place(x=50, y=150)

# Labels and Entry widgets for registration and login
welcome_label = tk.Label(root, text='Welcome to Academic Goal Tracking Application', bg='maroon', font=('cursive', 16, 'bold'), fg='yellow', width=30)
welcome_label.pack(side='top', fill='x', padx=20, pady=30)
username_label = tk.Label(root, text='Username:', bg='#F6F6F6', fg='black')
username_entry = tk.Entry(root)
password_label = tk.Label(root, text='Password:', bg='#F6F6F6', fg='black')
password_entry = tk.Entry(root, show='*')
email_label = tk.Label(root, text='Email:', bg='#F6F6F6', fg='black')
email_entry = tk.Entry(root)
quote_label = tk.Label(quote_rectangle, text='', wraplength=400, justify='center', bg='maroon', font=('cursive', 12, 'bold'), fg='yellow')

# Create a frame to hold the "Login" and "Register" buttons
buttons_frame = tk.Frame(root, bg='#F6F6F6')
buttons_frame.pack(side='bottom')

# Create buttons for registration and login within the buttons frame
register_button = tk.Button(buttons_frame, text='Register', command=register_user)
login_button = tk.Button(buttons_frame, text='Login', command=login_user)

# Pack layout for buttons in the middle
register_button.pack(side='left', padx=10, pady=30)
login_button.pack(side='left', padx=15, pady=30)

# Pack layout for other elements
welcome_label.pack(pady=10)
username_label.pack()
username_entry.pack()
password_label.pack()
password_entry.pack()
email_label.pack()
email_entry.pack()
quote_label.pack(pady=20)
quote_rectangle.pack()

# Display an initial motivational quote and start the automatic quote rotation
start_motivational_quotes()

root.mainloop()
