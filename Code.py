import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import mysql.connector

# Function to log data to the MySQL database
def log_data():
    selected_action = action_var.get()
    selected_log = log_var.get()
    value = log_entry.get()

    try:
        if selected_action == "Log Data":
            if selected_log == "Exercise":
                table_name = "exercise_diet_log"
                log_type = "Exercise"
            elif selected_log == "Diet":
                table_name = "exercise_diet_log"
                log_type = "Diet"
            else:
                raise ValueError("Invalid log type selected.")
                return

            # Connect to the MySQL database
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='fitness_logger'
            )
            cursor = db.cursor()

            # Insert data into the database
            current_time = datetime.datetime.now()
            insert_query = "INSERT INTO " + table_name + " (log, log_type, timestamp) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (value, log_type, current_time))
            db.commit()
            db.close()

            messagebox.showinfo("Success", "Data logged successfully.")
        update_combobox()  # Update the Combobox with the latest data
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"MySQL Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to retrieve data from the MySQL database
def retrieve_data():
    selected_action = action_var.get()
    selected_log = log_var.get()

    try:
        if selected_action == "Retrieve Data":
            if selected_log == "Exercise":
                table_name = "exercise_diet_log"
                log_type = "Exercise"
            elif selected_log == "Diet":
                table_name = "exercise_diet_log"
                log_type = "Diet"
            else:
                raise ValueError("Invalid log type selected.")
                return

            # Connect to the MySQL database
            db = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='fitness_logger'
            )
            cursor = db.cursor()

            # Retrieve data from the database
            select_query = f"SELECT timestamp, log FROM {table_name} WHERE log_type = %s"
            cursor.execute(select_query, (log_type,))
            data = cursor.fetchall()
            db.close()

            # Display the data in the output screen
            output_text.config(state=tk.NORMAL)
            output_text.delete("1.0", tk.END)  # Clear the output screen
            for entry in data:
                timestamp, value = entry
                output_text.insert(tk.END, f"{timestamp}: {value}\n")
            output_text.config(state=tk.DISABLED)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"MySQL Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to update the Combobox with log types
def update_combobox():
    log_types = ["Exercise", "Diet"]
    log_combobox["values"] = log_types

# Create the main tkinter window
root = tk.Tk()
root.title("Health Management System")
root.geometry("800x600")

# Create left frame to hold buttons and input elements
left_frame = tk.Frame(root, bg="#FFFACD")
left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

# Create right frame to display the output screen
right_frame = tk.Frame(root, bg="#FFFACD")
right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

# Create log type selection Combobox
log_label = tk.Label(left_frame, text="Select Log Type", bg="#FFFACD")
log_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
log_var = tk.StringVar(root)
log_var.set("Exercise")
log_combobox = ttk.Combobox(left_frame, textvariable=log_var, state="readonly")
log_combobox.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Create action selection radio buttons
action_label = tk.Label(left_frame, text="Select Action", bg="#FFFACD")
action_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
action_var = tk.StringVar(root)
action_var.set("Log Data")
log_data_radio = tk.Radiobutton(left_frame, text="Log Data", variable=action_var, value="Log Data", bg="#FFFACD")
retrieve_data_radio = tk.Radiobutton(left_frame, text="Retrieve Data", variable=action_var, value="Retrieve Data", bg="#FFFACD")
log_data_radio.grid(row=3, column=0, padx=10, pady=5, sticky="w")
retrieve_data_radio.grid(row=4, column=0, padx=10, pady=5, sticky="w")

# Create data entry field
log_entry_label = tk.Label(left_frame, text="Enter Data", bg="#FFFACD")
log_entry_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
log_entry = tk.Entry(left_frame)
log_entry.grid(row=6, column=0, padx=10, pady=10, sticky="we")

# Create log button
log_button = tk.Button(left_frame, text="Log Data", command=log_data, bg="black", fg="white", width=20)
log_button.grid(row=7, column=0, padx=10, pady=10)

# Create retrieve button
retrieve_button = tk.Button(left_frame, text="Retrieve Data", command=retrieve_data, bg="black", fg="white", width=20)
retrieve_button.grid(row=8, column=0, padx=10, pady=10)

# Create output screen on the right
output_text = scrolledtext.ScrolledText(right_frame, bg="black", fg="white")
output_text.pack(expand=True, fill="both")

# Update the Combobox with log types
update_combobox()

# Start the tkinter main loop
root.mainloop()
