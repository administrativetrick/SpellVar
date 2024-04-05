import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, Menu, filedialog
import csv

# Function to create and initialize the database
def create_database():
    connection = sqlite3.connect('spelling_variances.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS variances (
            word TEXT UNIQUE NOT NULL,
            region TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

# Function to add a spelling variance to the database
def add_variance_to_database(word, region):
    connection = sqlite3.connect('spelling_variances.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO variances (word, region) VALUES (?, ?)', (word, region))
        connection.commit()
        messagebox.showinfo("Success", f"Added '{word}' for {region} region.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"The word '{word}' already exists in the database.")
    finally:
        connection.close()

# Function to fetch and display all spelling variances from the database
def view_spelling_variances():
    connection = sqlite3.connect('spelling_variances.db')
    cursor = connection.cursor()
    cursor.execute('SELECT word, region FROM variances')
    variances = cursor.fetchall()
    connection.close()

    display_text = "Spelling variances in database:\n" + "\n".join(f"{word} - {region}" for word, region in variances)
    messagebox.showinfo("Spelling Variances", display_text)

# Function to analyze a text sample and identify regional spelling characteristics
def analyze_text(text):
    connection = sqlite3.connect('spelling_variances.db')
    cursor = connection.cursor()
    words = text.split()
    region_counts = {}

    for word in words:
        cursor.execute('SELECT region FROM variances WHERE word = ?', (word,))
        result = cursor.fetchone()
        if result:
            region = result[0]
            if region in region_counts:
                region_counts[region] += 1
            else:
                region_counts[region] = 1

    connection.close()
    return region_counts

# Function to load variances from a file into the database
def upload_variances():
    filepath = filedialog.askopenfilename(title="Select file", filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
    if filepath:
        with open(filepath, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) == 2:
                    add_variance_to_database(row[0], row[1])

# Function to create and display the GUI
# Function to create and display the GUI
def gui():
    root = tk.Tk()
    root.title("SpellVar")

    # Menu setup
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="View Spelling Variances", command=view_spelling_variances)
    file_menu.add_command(label="Upload Variances", command=upload_variances)
    menu_bar.add_cascade(label="File", menu=file_menu)

    def add_variance():
        word = simpledialog.askstring("Input", "Enter the spelling variance:", parent=root)
        if word:  # Ensure word is not empty
            region = simpledialog.askstring("Input", "Enter the region:", parent=root)
            if region:  # Ensure region is not empty
                add_variance_to_database(word, region)

    def evaluate_text():
        text = text_area.get("1.0", tk.END).strip()
        if text:
            region_counts = analyze_text(text)
            result_message = "Spelling analysis by region:\n" + "\n".join(f"{region}: {count}" for region, count in region_counts.items())
            messagebox.showinfo("Analysis Result", result_message)

    text_area = scrolledtext.ScrolledText(root, height=10)
    text_area.pack()

    evaluate_button = tk.Button(root, text="Evaluate Text", command=evaluate_text)
    evaluate_button.pack(side=tk.BOTTOM)

    add_button = tk.Button(root, text="Add Spelling Variance", command=add_variance)
    add_button.pack(side=tk.BOTTOM)

    root.mainloop()

# Main execution
if __name__ == "__main__":
    create_database()  # Ensure the database is set up
    gui()  # Start the GUI
