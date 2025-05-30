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
    """
    Generates a list of random data rows based on the specified sample type.

    Args:
        num_rows (int): The number of data rows to generate.
        sample_type (str): The type of sample data to generate 
                           (e.g., 'Personnel', 'Financial').

    Returns:
        list: A list of lists, where each inner list represents a row of data.
    """
    data = []
    # Conditional data generation based on sample_type
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
    # Add more sample types here if needed
    return data

def write_to_csv(filename, data, sample_type):
    """
    Writes the given data to a CSV file with appropriate headers.

    Args:
        filename (str): The path to the CSV file to be written.
        data (list): A list of lists representing the data rows.
        sample_type (str): The type of sample data, used to get column headers.
    
    Raises:
        IOError: If an error occurs during file writing.
    """
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(get_column_names(sample_type)) # Write headers
            writer.writerows(data) # Write data rows
    except IOError as e:
        # Display error to the user if file writing fails
        QMessageBox.critical(window, "File Write Error", f"Could not write to CSV file: {filename}.\n\nDetails: {e}")
        raise # Re-raise for potential further handling if necessary, or remove if GUI should just stop.
    except Exception as e: # Catch any other unexpected errors during writing
        QMessageBox.critical(window, "CSV Writing Error", f"An unexpected error occurred while writing the CSV file.\nError: {e}")
        raise # Re-raise


def get_column_names(sample_type):
    """
    Retrieves the column names (headers) for a given sample data type.

    Args:
        sample_type (str): The type of sample data (e.g., 'Personnel').

    Returns:
        list: A list of strings representing the column names.
              Returns an empty list if sample_type is unknown, though current usage
              implies sample_type will always be one of the predefined keys.
    """
    column_names = {
        'Personnel': ['Name', 'Address', 'Phone', 'DOB', 'Salary', 'Category', 'Job Title', 'Company'],
        'Financial': ['Company', 'Catch Phrase', 'Job', 'Date', 'Salary', 'Category', 'Address', 'City'],
        'Employee': ['First Name', 'Last Name', 'DOB', 'Country', 'Job', 'Salary', 'Company', 'Catch Phrase'],
        'Customer': ['Email', 'Phone', 'City', 'DOB', 'Gender', 'Salary', 'Name', 'Company']
    }
    return column_names.get(sample_type, []) # Return empty list for unknown type

def generate_csv():
    """
    Handles the "Generate CSV" button click event.
    Prompts the user for the number of rows and sample type,
    generates random data, and saves it to a CSV file.
    Displays messages to the user via QMessageBox.
    """
    try:
        num_rows, ok = QInputDialog.getInt(window, "Enter Number of Rows", "Number of Rows:", 100, 1, 1, 1000000) # Min 1, Max 1M rows
        if not ok:
            return # User cancelled

        sample_type = sample_choice.currentText() # Get selected sample type from combobox
        data = generate_random_data(num_rows, sample_type) # Generate data

        # Prompt user for save location
        file_path, _ = QFileDialog.getSaveFileName(window, "Save CSV", "", "CSV files (*.csv)")
        if not file_path:
            return # User cancelled save dialog
        
        # Write data to CSV (includes its own error handling for file I/O)
        write_to_csv(file_path, data, sample_type) 
        
        # Show success message only if no exceptions were raised by write_to_csv
        QMessageBox.information(window, "CSV Generated", f"{num_rows} rows of random data generated and saved to {file_path}")
    except Exception as e:
        # Catch any other unexpected errors during the process
        QMessageBox.critical(window, "Generation Error", f"An unexpected error occurred during CSV generation: {e}")


def find_words_in_query(words_list, sql_query):
    """
    Finds occurrences of specified words within an SQL query string.
    Each word is searched independently. The search is case-insensitive.
    The pattern aims to match whole words or words delimited by common SQL delimiters
    (e.g., space, comma, dot, underscore), avoiding partial matches within other words.

    Args:
        words_list (list of str): A list of words to search for.
        sql_query (str): The SQL query text.

    Returns:
        dict: A dictionary where keys are the search words (from `words_list`)
              that were found in the `sql_query`. Each value is a list of tuples,
              where each tuple contains:
              (line_number (int), matched_text (str), full_line_content (str)).
              Returns an empty dictionary if no words are found or inputs are invalid.
    """
    found_words = {}
    if not words_list or not sql_query: # Basic validation
        return found_words

    lines = sql_query.split('\n')
    for i, line in enumerate(lines, start=1): # Line numbers start from 1
        for word in words_list:
            if not word: continue # Skip empty search words

            escaped_word = re.escape(word)
            pattern = r'(?:^|(?<=[^a-zA-Z0-9_]))({})(?:$|(?=[^a-zA-Z0-9_]))'.format(escaped_word)

            try:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    matched_text = match.group(1) 
                    if word not in found_words:
                        found_words[word] = []
                    found_words[word].append((i, matched_text, line.strip()))
            except re.error as e:
                print(f"Regex error for word '{word}': {e}") 
                continue 
                
    return found_words

def find_suggestions(sql_query):
    """
    Analyzes an SQL query string to extract potential column names, table names,
    and column names used in filter conditions (typically in the WHERE clause).
    The extraction is based on regular expressions and common SQL patterns.
    This is not a full SQL parser and may have limitations with very complex queries
    or dialect-specific syntax.

    Args:
        sql_query (str): The SQL query string to analyze.

    Returns:
        dict: A dictionary with three keys: 'Columns', 'Tables', 'Filters'.
              Each key holds a set of unique strings representing the suggestions
              found in that category. Sets are used to avoid duplicate suggestions.
    """
    suggestions = {
        'Columns': set(), 
        'Tables': set(),  
        'Filters': set()
    }

    processed_query_for_suggestions = re.sub(r'--[^\n]*', '', sql_query)
    processed_query_for_suggestions = re.sub(r'/\*.*?\*/', '', processed_query_for_suggestions, flags=re.DOTALL)

    # --- 1. Column Parsing ---
    columns_match = re.search(r'SELECT\s+(.+?)\s+FROM', processed_query_for_suggestions, re.IGNORECASE | re.DOTALL)
    if columns_match:
        columns_text = columns_match.group(1).strip()
        # Split column candidates by comma, respecting parentheses to avoid splitting function arguments
        raw_column_parts = [p.strip() for p in re.split(r',\s*(?![^()]*\))', columns_text)]
        
        for part in raw_column_parts:
            if not part: continue 

            col_name_part = part
            alias_match_outer = re.match(r'(.+?)\s+AS\s+([\"\']?[\w\s]+[\"\']?)$', part, re.IGNORECASE)
            if alias_match_outer:
                col_name_part = alias_match_outer.group(1).strip()
                # alias_name_for_col = alias_match_outer.group(2).strip().strip('"\'') # Alias not stored for now

            func_match = re.match(r'(\w+)\s*\((.*?)\)$', col_name_part, re.IGNORECASE) 
            if func_match:
                func_name = func_match.group(1)
                func_args_str = func_match.group(2).strip()
                suggestions['Columns'].add(f"{func_name}({func_args_str})") 
                
                arg_candidates = re.findall(r'([\w\."\*]+)', func_args_str) 
                for arg_cand in arg_candidates: 
                    if arg_cand != '*': 
                        suggestions['Columns'].add(arg_cand.strip().strip('"\''))
                continue 

            direct_col_match = re.match(r'([\w\."\*]+(?:[\w\."\*]+)*)', col_name_part, re.IGNORECASE)
            if direct_col_match:
                if direct_col_match.group(0) == col_name_part:
                    suggestions['Columns'].add(direct_col_match.group(1).strip().strip('"\''))
                elif col_name_part: 
                    suggestions['Columns'].add(col_name_part) 
            elif col_name_part : 
                 suggestions['Columns'].add(col_name_part)

    # --- 2. Table Parsing ---
    table_pattern = r"""
        (?:FROM|JOIN)\s+
        ((?:[\w`"]+(?:[\.:`"][\w`"]+)*)|[\w`"]+) 
        (?:\s+(?:AS\s+)?([\w`]+))?             
    """
    for match in re.finditer(table_pattern, processed_query_for_suggestions, re.IGNORECASE | re.VERBOSE):
        table_name_full = match.group(1)
        table_name_cleaned = table_name_full.replace('"', '').replace('`', '')
        
        if '(' not in table_name_cleaned and ')' not in table_name_cleaned and table_name_cleaned.lower() != 'on':
            suggestions['Tables'].add(table_name_cleaned)

    from_clause_match = re.search(r'\bFROM\s+([^;]+?)(?=\sWHERE|\sLEFT JOIN|\sRIGHT JOIN|\sINNER JOIN|\sOUTER JOIN|\sON|\sGROUP BY|\sORDER BY|\sLIMIT|\sSELECT|\sUNION|\sINTERSECT|\sEXCEPT|\sOFFSET|\sFETCH|\sWITH|\s*$)', processed_query_for_suggestions, re.IGNORECASE | re.DOTALL)
    if from_clause_match:
        from_content = from_clause_match.group(1)
        # Remove JOIN parts from this content as JOINs are handled by the table_pattern finditer above
        from_content_no_joins = re.split(r'\s+(?:INNER\s+|LEFT\s+|RIGHT\s+|FULL\s+)?(?:OUTER\s+)?JOIN\s+', from_content, flags=re.IGNORECASE)[0]
        from_tables_parts = from_content_no_joins.split(',')
        for table_entry_part in from_tables_parts:
            table_entry_part = table_entry_part.strip()
            table_alias_match = re.match(r'((?:[\w`"]+(?:[\.:`"][\w`"]+)*)|[\w`"]+)\s*(?:AS\s+|\s+)?([\w`]+)?', table_entry_part)
            if table_alias_match:
                table_name = table_alias_match.group(1).replace('"', '').replace('`', '')
                if '(' not in table_name and ')' not in table_name and table_name.lower() != 'on':
                     suggestions['Tables'].add(table_name)
                    
    # --- 3. Filter Parsing (WHERE clause) ---
    where_match = re.search(r'WHERE\s+(.+?)(?:\sGROUP BY|\sORDER BY|\sLIMIT|\s*$)', processed_query_for_suggestions, re.IGNORECASE | re.DOTALL)
    if where_match:
        where_conditions_text = where_match.group(1)
        filter_columns = re.findall(r'([\w\."`]+(?:[\w\."`]+)*)\s*(?:=|!=|<|>|<=|>=|LIKE\b|IN\b|BETWEEN\b|IS(?:\s+NOT)?\b)', where_conditions_text, re.IGNORECASE)
        for col in filter_columns:
            cleaned_col = col.strip().strip('"`').replace('`.`', '.').replace('"."', '.')
            suggestions['Filters'].add(cleaned_col)
        
        boolean_context_cols = re.findall(r'(?:\bAND\b|\bOR\b|\bNOT\b)\s+([\w\."`]+(?:[\w\."`]+)*)|([\w\."`]+(?:[\w\."`]+)*)\s+(?:\bAND\b|\bOR\b)', where_conditions_text, re.IGNORECASE)
        for match_tuple in boolean_context_cols: 
            for col_in_tuple in match_tuple: 
                if col_in_tuple: 
                    cleaned_col = col_in_tuple.strip().strip('"`').replace('`.`', '.').replace('"."', '.')
                    suggestions['Filters'].add(cleaned_col)
    return suggestions

def find_words():
    """
    Handles the "Find Words" button click event.
    Gets words to find and the SQL query from the UI,
    calls helper functions to find word occurrences and suggestions,
    and updates the UI text areas with the results.
    """
    try:
        words_to_find_str = entry_words.text()
        if not words_to_find_str.strip():
            QMessageBox.information(window, "No Words Entered", "Please enter words to find in the SQL query.")
            return
        
        words_to_find = [word.strip() for word in words_to_find_str.split(",") if word.strip()]
        if not words_to_find: 
            QMessageBox.information(window, "No Valid Words", "Please enter valid words, separated by commas.")
            return

        sql_query = text_query.toPlainText()
        if not sql_query.strip():
            QMessageBox.information(window, "No SQL Query", "Please enter an SQL query to analyze.")
            return
            
        found_words_occurrences = find_words_in_query(words_to_find, sql_query)

        found_output = []
        if not found_words_occurrences:
            found_output.append("0 occurrences found for the specified word(s).")
        else:
            for word, occurrences in found_words_occurrences.items():
                found_output.append(f"Occurrences of '{word}':")
                for line_num, full_word, full_line in occurrences:
                    found_output.append(f"  Line {line_num}: {full_line} (Matched: '{full_word}')")
                found_output.append("-" * 50) 
        text_found.setPlainText("\n".join(found_output))

        sql_suggestions = find_suggestions(sql_query)
        suggestions_output_text = ""
        if not sql_suggestions['Columns'] and not sql_suggestions['Tables'] and not sql_suggestions['Filters']:
            suggestions_output_text = "No specific SQL suggestions found. Try a different query structure."
        else:
            for category, items in sql_suggestions.items():
                if items: 
                    suggestions_output_text += f"{category.capitalize()}:\n"
                    for item in sorted(list(items)): 
                        suggestions_output_text += f"  - {item}\n"
                    suggestions_output_text += "\n" 
        text_suggestions.setPlainText(suggestions_output_text.strip())
    except Exception as e:
        QMessageBox.critical(window, "Processing Error", f"An unexpected error occurred: {e}")


def upload_csv():
    """
    Handles the "Upload CSV" button click event.
    Prompts the user to select a CSV file, reads it, infers data types
    for each column, sanitizes the table name, and generates a
    CREATE TABLE SQL query. Displays the query in a text area.
    Includes error handling for file operations and CSV parsing.
    """
    file_path, _ = QFileDialog.getOpenFileName(window, "Open CSV", "", "CSV files (*.csv)")
    if not file_path:
        return 

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile: 
            reader = csv.reader(csvfile)
            try:
                header = next(reader) 
            except StopIteration: 
                QMessageBox.warning(window, "Empty CSV File", "The selected CSV file is empty.")
                return

            if not header: 
                QMessageBox.warning(window, "Empty CSV Header", "The CSV file has an empty header row.")
                return

            data_rows_sample = []
            for i, row in enumerate(reader):
                if i < 100: 
                    data_rows_sample.append(row)
                else:
                    break 
            
            if not data_rows_sample: 
                QMessageBox.warning(window, "No Data Rows", "The CSV file contains a header but no data rows for analysis.")
                return

            num_cols_header = len(header)
            columns_for_inference = [[] for _ in range(num_cols_header)]
            
            for row_num, current_row_data in enumerate(data_rows_sample):
                if len(current_row_data) != num_cols_header:
                    QMessageBox.warning(window, "Inconsistent Column Count", 
                                        f"Data row {row_num + 1} has {len(current_row_data)} columns, "
                                        f"but the header has {num_cols_header}. "
                                        "Data type inference will be based on available data, padding short rows with None.")
                    while len(current_row_data) < num_cols_header:
                        current_row_data.append(None)
                    current_row_data = current_row_data[:num_cols_header]

                for col_idx, cell_value in enumerate(current_row_data):
                    columns_for_inference[col_idx].append(cell_value) 
            
            inferred_sql_types = [_infer_data_type(col_data) for col_data in columns_for_inference]

    except FileNotFoundError:
        QMessageBox.critical(window, "File Not Found", f"Error: The file '{file_path}' was not found.")
        return
    except IOError as e: 
        QMessageBox.critical(window, "File Access Error", f"Error: Could not read the file '{file_path}'.\nReason: {e}")
        return
    except csv.Error as e: 
        QMessageBox.critical(window, "CSV Parsing Error", f"Error parsing the CSV file: {e}.\nPlease ensure it's a valid CSV.")
        return
    except Exception as e: 
        QMessageBox.critical(window, "Unexpected Error", f"An unexpected error occurred while processing the CSV file: {e}")
        return

    raw_table_name = file_path.split('/')[-1].split('.')[0]
    table_name = _sanitize_table_name(raw_table_name)
    sanitized_header = [_sanitize_column_name(col) for col in header]
    
    escaped_table_name = table_name.replace('"', '""')
    create_query = f'CREATE TABLE "{escaped_table_name}" (\n'

    column_definitions = []
    for col_name, data_type in zip(sanitized_header, inferred_sql_types): 
        escaped_col_name = col_name.replace('"', '""')
        quoted_col_name = f'"{escaped_col_name}"'
        column_definitions.append(f"    {quoted_col_name} {data_type}")
    
    create_query += ",\n".join(column_definitions)
    create_query += "\n);"

    text_create_query.setPlainText(create_query)

# --- Helper functions for upload_csv (data type inference and sanitization) ---

def _sanitize_identifier(identifier, default_name="default_identifier"):
    """
    Sanitizes a generic SQL identifier (table or column name).
    - Replaces spaces and special characters (non-alphanumeric, non-underscore) with underscores.
    - Ensures it starts with a letter or underscore (prepends '_' if not).
    - Truncates to a maximum length of 63 characters (common SQL limit).

    Args:
        identifier (str): The proposed identifier name.
        default_name (str): The default name to return if the input is empty.

    Returns:
        str: The sanitized identifier name.
    """
    if not identifier or not str(identifier).strip():
        return default_name

    identifier_str = str(identifier).strip()
    identifier_str = re.sub(r'[^\w_]', '_', identifier_str) 
    identifier_str = re.sub(r'_+', '_', identifier_str) 
    
    if not re.match(r'^[a-zA-Z_]', identifier_str):
        identifier_str = '_' + identifier_str
    
    if not identifier_str: 
        return default_name

    if not re.match(r'^[a-zA-Z_]', identifier_str): 
        identifier_str = '_' + identifier_str
        
    return identifier_str[:63] 


def _sanitize_table_name(table_name):
    """
    Sanitizes a table name using the generic _sanitize_identifier function.
    """
    return _sanitize_identifier(table_name, "default_table_name")

def _sanitize_column_name(column_name):
    """
    Sanitizes a column name using the generic _sanitize_identifier function.
    """
    return _sanitize_identifier(column_name, "default_column_name")


def _is_bool(value_str):
    """
    Checks if a value can be reasonably interpreted as a boolean.
    Case-insensitive check for common boolean representations.
    Accepts Python bool, int (0,1), or string.

    Args:
        value_str (any): The value to check.

    Returns:
        bool: True if the value appears to be boolean, False otherwise.
    """
    if isinstance(value_str, bool): return True
    if isinstance(value_str, int) and value_str in [0, 1]: return True
    if isinstance(value_str, str):
        return value_str.lower() in ['true', 'false', 'yes', 'no', '0', '1', 't', 'f', 'y', 'n']
    return False

def _is_int(value_str):
    """
    Checks if a value can be converted to an integer.
    Accepts values that can be losslessly converted to int (e.g., "1", 1.0, "0").

    Args:
        value_str (any): The value to check.

    Returns:
        bool: True if convertible to int, False otherwise.
    """
    try:
        val_float = float(str(value_str))
        return val_float.is_integer()
    except (ValueError, TypeError):
        return False

def _is_float(value_str):
    """
    Checks if a value can be converted to a float.

    Args:
        value_str (any): The value to check.

    Returns:
        bool: True if convertible to float, False otherwise.
    """
    try:
        float(str(value_str))
        return True
    except (ValueError, TypeError):
        return False

def _is_datetime(value_str):
    """
    Checks if a string value matches 'YYYY-MM-DD HH:MM:SS' datetime format.

    Args:
        value_str (str): The string value to check.

    Returns:
        bool: True if it matches the datetime format, False otherwise.
    """
    if not isinstance(value_str, str): return False
    try:
        datetime.strptime(value_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def _is_date(value_str):
    """
    Checks if a string value matches common date formats (YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY)
    OR the specific DATETIME format 'YYYY-MM-DD HH:MM:SS'.

    Args:
        value_str (str): The string value to check.

    Returns:
        bool: True if it matches one of the date or datetime formats, False otherwise.
    """
    if not isinstance(value_str, str): return False
    if _is_datetime(value_str):
        return True
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y'):
        try:
            datetime.strptime(value_str, fmt)
            return True
        except ValueError:
            continue
    return False

from datetime import datetime 

def _infer_data_type(column_values):
    """
    Infers the most appropriate SQL data type for a column based on a sample of its values.
    Follows priority: BOOLEAN -> INT -> FLOAT -> DATETIME -> DATE -> VARCHAR.
    If mixed types are present, it promotes to the more general type in the hierarchy.

    Args:
        column_values (list): A list of sample values from the column.
                              Values can be of any type, will be converted to string for checks.

    Returns:
        str: The inferred SQL data type string (e.g., "INT", "VARCHAR(255)").
    """
    if not column_values:
        return "VARCHAR(255)" 

    processed_values = []
    for v in column_values:
        if v is not None:
            s_val = str(v).strip()
            if s_val != "":
                processed_values.append(s_val) 

    if not processed_values: 
        return "VARCHAR(255)"

    max_str_len = 0
    for s_val in processed_values:
        max_str_len = max(max_str_len, len(s_val))

    has_string = False      
    has_datetime = False    
    has_date = False        
    has_float = False       
    has_int = False         
    has_bool = False        

    for v_str in processed_values:
        is_b, is_i, is_f, is_d, is_dt = _is_bool(v_str), _is_int(v_str), _is_float(v_str), _is_date(v_str), _is_datetime(v_str)
        
        if is_b: has_bool = True
        if is_i: has_int = True
        if is_f: has_float = True
        if is_d: has_date = True
        if is_dt: has_datetime = True
        
        if not (_is_float(v_str) or _is_date(v_str) or (_is_bool(v_str) and not _is_int(v_str) and not _is_float(v_str)) ):
            has_string = True

    if has_string:
        return f"VARCHAR({max(255, min(max_str_len, 1024))})"
    if has_datetime:
        return "DATETIME"
    if has_date:
        return "DATE"
    if has_float:
        return "FLOAT"
    if has_int:
        return "INT"
    if has_bool:
        return "BOOLEAN"
        
    return f"VARCHAR({max(255, min(max_str_len, 1024))})"

# Global UI elements
app = QApplication(sys.argv)
window = QMainWindow() 
window.setWindowTitle("SQL Tools 0.0.4") 

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
text_create_query = QTextEdit() # This is the global variable the test tries to mock
text_create_query.setReadOnly(True)
layout_create_table.addWidget(text_create_query)

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

if __name__ == '__main__':
    window.show()
    sys.exit(app.exec_())
