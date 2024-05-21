import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QRadioButton,
                             QVBoxLayout, QTabWidget, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea)

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
    num_rows, ok = QInputDialog.getInt(window, "Enter Number of Rows", "Number of Rows:", 100, 1)
    if not ok:
        return
    sample_type = sample_choice.currentText()
    data = generate_random_data(num_rows, sample_type)
    file_path, _ = QFileDialog.getSaveFileName(window, "Save CSV", "", "CSV files (*.csv)")
    if not file_path:
        return
    write_to_csv(file_path, data, sample_type)
    QMessageBox.information(window, "CSV Generated", f"{num_rows} rows of random data generated and saved to {file_path}")

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
    words_to_find = [word.strip() for word in entry_words.text().split(",")]
    if not any(words_to_find):
        QMessageBox.information(window, "No Words Entered", "Please enter words to find.")
        return

    sql_query = text_query.toPlainText()
    found_words = find_words_in_query(words_to_find, sql_query)

    found_output = []
    if not found_words:
        found_output.append("0 occurrences found")
    else:
        for word, occurrences in found_words.items():
            for line_num, full_word, full_line in occurrences:
                found_output.append(f"Word: {full_word} | Line {line_num}: {full_line}")
                found_output.append("-" * 50)

    text_found.setPlainText("\n".join(found_output))

    suggestions = find_suggestions(sql_query)
    suggestions_text = ""
    for category, words in suggestions.items():
        suggestions_text += f"{category}:\n"
        for word in words:
            suggestions_text += f"- {word}\n"
    text_suggestions.setPlainText(suggestions_text)

def upload_csv():
    file_path, _ = QFileDialog.getOpenFileName(window, "Open CSV", "", "CSV files (*.csv)")
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

    text_create_query.setPlainText(create_query)

app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("SQL Tools 0.0.2")

tab_widget = QTabWidget()
tab_find_words = QWidget()
tab_create_table = QWidget()
tab_generate_csv = QWidget()
tab_widget.addTab(tab_find_words, "Find Words")
tab_widget.addTab(tab_create_table, "Create Table")
tab_widget.addTab(tab_generate_csv, "Generate CSV")

layout_find_words = QVBoxLayout(tab_find_words)
layout_create_table = QVBoxLayout(tab_create_table)
layout_generate_csv = QVBoxLayout(tab_generate_csv)

label_words = QLabel("Enter words to find (comma-separated):")
layout_find_words.addWidget(label_words)
entry_words = QLineEdit()
layout_find_words.addWidget(entry_words)

label_query = QLabel("Enter SQL Query:")
layout_find_words.addWidget(label_query)
text_query = QTextEdit()
layout_find_words.addWidget(text_query)

button_find = QPushButton("Find Words")
button_find.clicked.connect(find_words)
layout_find_words.addWidget(button_find)

label_found = QLabel("Words found in the query:")
layout_find_words.addWidget(label_found)
text_found = QTextEdit()
text_found.setReadOnly(True)
layout_find_words.addWidget(text_found)

label_suggestions = QLabel("Search Suggestions:")
layout_find_words.addWidget(label_suggestions)
text_suggestions = QTextEdit()
text_suggestions.setReadOnly(True)
layout_find_words.addWidget(text_suggestions)

button_upload_csv = QPushButton("Upload CSV")
button_upload_csv.clicked.connect(upload_csv)
layout_create_table.addWidget(button_upload_csv)

label_create_query = QLabel("Create Table Query:")
layout_create_table.addWidget(label_create_query)
text_create_query = QTextEdit()
text_create_query.setReadOnly(True)
layout_create_table.addWidget(text_create_query)

label_rows = QLabel("Enter number of rows:")
layout_generate_csv.addWidget(label_rows)
entry_rows = QLineEdit()
layout_generate_csv.addWidget(entry_rows)

label_sample = QLabel("Select sample type:")
layout_generate_csv.addWidget(label_sample)
sample_choice = QtWidgets.QComboBox()
sample_choice.addItems(['Personnel', 'Financial', 'Employee', 'Customer'])
layout_generate_csv.addWidget(sample_choice)

button_generate_csv = QPushButton("Generate CSV")
button_generate_csv.clicked.connect(generate_csv)
layout_generate_csv.addWidget(button_generate_csv)

layout_main = QVBoxLayout()
layout_main.addWidget(tab_widget)

window.setCentralWidget(QWidget())
window.centralWidget().setLayout(layout_main)
window.show()
sys.exit(app.exec_())
