import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import csv
from faker import Faker
import random
import re

fake = Faker()

def generate_random_data(num_rows, sample_type):
    data = []
    if sample_type == 'Personnel':
        for _ in range(num_rows):
            row = [
                fake.name(),
                fake.address(),
                fake.phone_number(),
                fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
                random.randint(10000, 1000000),
                random.choice(['A', 'B', 'C']),
                fake.job(),
                fake.company(),
            ]
            data.append(row)
    elif sample_type == 'Financial':
        for _ in range(num_rows):
            row = [
                fake.company(),
                fake.catch_phrase(),
                fake.job(),
                fake.date_this_decade().strftime('%Y-%m-%d'),
                random.randint(1000, 10000),
                random.choice(['X', 'Y', 'Z']),
                fake.address(),
                fake.city(),
            ]
            data.append(row)
    elif sample_type == 'Employee':
        for _ in range(num_rows):
            row = [
                fake.first_name(),
                fake.last_name(),
                fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
                fake.country(),
                fake.job(),
                random.randint(20000, 200000),
                fake.company(),
                fake.catch_phrase(),
            ]
            data.append(row)
    elif sample_type == 'Customer':
        for _ in range(num_rows):
            row = [
                fake.email(),
                fake.phone_number(),
                fake.city(),
                fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
                random.choice(['Male', 'Female']),
                random.randint(30000, 300000),
                fake.name(),
                fake.company(),
            ]
            data.append(row)
    return data

def write_to_csv(filename, data, sample_type):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(get_column_names(sample_type))
        writer.writerows(data)

def get_column_names(sample_type):
    column_names = {
        'Personnel': ['Name', 'Address', 'Phone', 'DOB', 'Salary', 'Category', 'Job Title', 'Company'],
        'Financial': ['Company', 'Catch Phrase', 'Job', 'Date', 'Salary', 'Category', 'Address', 'City'],
        'Employee': ['First Name', 'Last Name', 'DOB', 'Country', 'Job', 'Salary', 'Company', 'Catch Phrase'],
        'Customer': ['Email', 'Phone', 'City', 'DOB', 'Gender', 'Salary', 'Name', 'Company']
    }
    return column_names[sample_type]

def generate_csv():
    num_rows = int(entry_rows.get())
    sample_type = sample_choice.get()
    if num_rows <= 0:
        messagebox.showinfo("Invalid Input", "Please enter a valid number of rows.")
        return
    data = generate_random_data(num_rows, sample_type)
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    write_to_csv(file_path, data, sample_type)
    messagebox.showinfo("CSV Generated", f"{num_rows} rows of random data generated and saved to {file_path}")

def find_words_in_query(words_list, sql_query):
    found_words = {}
    lines = sql_query.split('\n')
    for i, line in enumerate(lines, start=1):
        for word in words_list:
            pattern = r'(\b{}\b|\S*{}\S*)'.format(re.escape(word), re.escape(word))
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                full_word = match.group(1)
                if word in found_words:
                    found_words[word].append((i, full_word, line.strip()))
                else:
                    found_words[word] = [(i, full_word, line.strip())]
    return found_words

def find_suggestions(sql_query):
    suggestions = {
        'Columns': set(),
        'Tables': set(),
        'Filters': set()
    }
    
    columns_pattern = r'SELECT\s+(.+?)\s+FROM'
    columns_match = re.search(columns_pattern, sql_query, re.IGNORECASE | re.DOTALL)
    if columns_match:
        columns_text = columns_match.group(1)
        columns_list = re.findall(r'\b(\w+)\b(?!\s+AS\s+\w+)', columns_text, re.IGNORECASE)
        suggestions['Columns'].update(columns_list)

    tables_pattern = r'\b(?:FROM|JOIN)\s+(\w+)\b'
    tables_match = re.findall(tables_pattern, sql_query, re.IGNORECASE)
    if tables_match:
        suggestions['Tables'].update(tables_match)

    where_pattern = r'WHERE\s+(.+?)(?:\s+ORDER BY|\s*$)'
    where_match = re.search(where_pattern, sql_query, re.IGNORECASE | re.DOTALL)
    if where_match:
        where_conditions = where_match.group(1)
        conditions = re.findall(r'([\w\.]+)\s*(?:=|<|>|<=|>=)\s*([\'\"]?\w+(?:-\w+-\w+)?[\'\"]?)', where_conditions)
        for condition in conditions:
            suggestions['Filters'].add(condition[1].strip("'"))

    return suggestions

def find_words():
    words_to_find = [word.strip() for word in entry_words.get().split(",")]
    if not any(words_to_find):
        messagebox.showinfo("No Words Entered", "Please enter words to find.")
        return

    sql_query = text_query.get("1.0", "end-1c")
    found_words = find_words_in_query(words_to_find, sql_query)

    found_output = []
    if not found_words:
        found_output.append("0 occurrences found")
    else:
        for word, occurrences in found_words.items():
            for line_num, full_word, full_line in occurrences:
                found_output.append(f"Word: {full_word} | Line {line_num}: {full_line}")
                found_output.append("-" * 50)

    text_found.config(state=tk.NORMAL)
    text_found.delete("1.0", "end")
    text_found.insert("1.0", "\n".join(found_output))
    text_found.config(state=tk.DISABLED)

    suggestions = find_suggestions(sql_query)
    text_suggestions.config(state=tk.NORMAL)
    text_suggestions.delete("1.0", "end")
    for category, words in suggestions.items():
        text_suggestions.insert("end", f"{category}:\n")
        for word in words:
            text_suggestions.insert("end", f"- {word}\n")
    text_suggestions.config(state=tk.DISABLED)

def upload_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        data_types = []
        for row in reader:
            for i, value in enumerate(row):
                try:
                    _ = int(value)
                    data_types.append("INT")
                except ValueError:
                    try:
                        _ = float(value)
                        data_types.append("FLOAT")
                    except ValueError:
                        data_types.append("VARCHAR(255)")

    table_name = file_path.split('/')[-1].split('.')[0] 
    create_query = f"CREATE TABLE {table_name} (\n"
    for col, data_type in zip(header, data_types):
        create_query += f"    {col} {data_type},\n"
    create_query = create_query.rstrip(",\n") + "\n);"

    text_create_query.config(state=tk.NORMAL)
    text_create_query.delete("1.0", "end")
    text_create_query.insert("1.0", create_query)
    text_create_query.config(state=tk.DISABLED)

root = tk.Tk()
root.title("SQL Tools 0.0.2")

tab_control = ttk.Notebook(root)
tab_find_words = ttk.Frame(tab_control)
tab_create_table = ttk.Frame(tab_control)
tab_generate_csv = ttk.Frame(tab_control)
tab_control.add(tab_find_words, text='Find Words')
tab_control.add(tab_create_table, text='Create Table')
tab_control.add(tab_generate_csv, text='Generate CSV')
tab_control.pack(expand=1, fill="both")

label_words = tk.Label(tab_find_words, text="Enter words to find (comma-separated):")
label_words.pack()
entry_words = tk.Entry(tab_find_words)
entry_words.pack()

label_query = tk.Label(tab_find_words, text="Enter SQL Query:")
label_query.pack()
text_query = scrolledtext.ScrolledText(tab_find_words, width=50, height=10)
text_query.pack()

button_find = tk.Button(tab_find_words, text="Find Words", command=find_words)
button_find.pack()

label_found = tk.Label(tab_find_words, text="Words found in the query:")
label_found.pack()
text_found = scrolledtext.ScrolledText(tab_find_words, width=50, height=7)
text_found.pack()

label_suggestions = tk.Label(tab_find_words, text="Search Suggestions:")
label_suggestions.pack()
text_suggestions = scrolledtext.ScrolledText(tab_find_words, width=50, height=7)
text_suggestions.pack()

button_upload_csv = tk.Button(tab_create_table, text="Upload CSV", command=upload_csv)
button_upload_csv.pack()

label_create_query = tk.Label(tab_create_table, text="Create Table Query:")
label_create_query.pack()
text_create_query = scrolledtext.ScrolledText(tab_create_table, width=50, height=28)
text_create_query.pack()

label_rows = tk.Label(tab_generate_csv, text="Enter number of rows:")
label_rows.pack()
entry_rows = tk.Entry(tab_generate_csv)
entry_rows.pack()

label_sample = tk.Label(tab_generate_csv, text="Select sample type:")
label_sample.pack()
sample_choice = tk.StringVar()
sample_choice.set('Personnel')  # Default value
radio_sample_a = tk.Radiobutton(tab_generate_csv, text='Personnel', variable=sample_choice, value='Personnel')
radio_sample_a.pack(anchor=tk.W)
radio_sample_b = tk.Radiobutton(tab_generate_csv, text='Financial', variable=sample_choice, value='Financial')
radio_sample_b.pack(anchor=tk.W)
radio_sample_c = tk.Radiobutton(tab_generate_csv, text='Employee', variable=sample_choice, value='Employee')
radio_sample_c.pack(anchor=tk.W)
radio_sample_d = tk.Radiobutton(tab_generate_csv, text='Customer', variable=sample_choice, value='Customer')
radio_sample_d.pack(anchor=tk.W)

button_generate_csv = tk.Button(tab_generate_csv, text="Generate CSV", command=generate_csv)
button_generate_csv.pack()

label_created_by = tk.Label(root, text="Created by Parreirao2", anchor="e")
label_created_by.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
