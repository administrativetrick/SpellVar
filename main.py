import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, Menu, filedialog
import csv

# Function to create and initialize the database
def create_database():
    connection = sqlite3.connect('spelling_variances.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS variances')  # Be cautious, this will remove existing data
    cursor.execute('''
        CREATE TABLE variances (
            word TEXT NOT NULL,
            region TEXT NOT NULL,
            PRIMARY KEY (word, region)
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
    except sqlite3.IntegrityError as e:
        messagebox.showerror("Error", f"Error adding '{word}' with region '{region}': {e}")
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
    total_counted_words = 0  # Total of words found in the database

    for word in words:
        cursor.execute('SELECT region FROM variances WHERE word = ?', (word,))
        result = cursor.fetchall()
        if result:
            total_counted_words += 1  # Increment for each word found in the database
            for region in result:
                region_name = region[0]
                region_counts[region_name] = region_counts.get(region_name, 0) + 1

    connection.close()

    # Convert counts to percentages
    region_percentages = {region: (count / total_counted_words * 100) if total_counted_words else 0 for region, count in region_counts.items()}

    return region_percentages


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
def gui():
    root = tk.Tk()
    root.title("Spelling Variance Database Manager")

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
