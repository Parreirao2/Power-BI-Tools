import sys
import unittest
from unittest.mock import MagicMock, patch, mock_open
import io

# --- Mock PyQt5 modules before importing SQL_Tools ---
MOCK_QT_MODULES = {
    'PyQt5.QtWidgets': MagicMock(),
    'PyQt5.QtGui': MagicMock(),
    'PyQt5.QtCore': MagicMock(),
    'PyQt5': MagicMock()
}
MOCK_QT_MODULES['PyQt5'].QtWidgets = MOCK_QT_MODULES['PyQt5.QtWidgets']
MOCK_QT_MODULES['PyQt5'].QtGui = MOCK_QT_MODULES['PyQt5.QtGui']
MOCK_QT_MODULES['PyQt5'].QtCore = MOCK_QT_MODULES['PyQt5.QtCore']
sys.modules.update(MOCK_QT_MODULES)

# Import functions and the 'window' instance from SQL_Tools
# 'window' is imported to be used as the correct parent in QMessageBox assertions
try:
    from SQL_Tools import (
        _sanitize_identifier, _sanitize_table_name, _sanitize_column_name,
        _is_bool, _is_int, _is_float, _is_date, _is_datetime, _infer_data_type,
        upload_csv, find_words_in_query, find_suggestions,
        window as sql_tools_window # Import the main window instance for assertions
    )
except ImportError:
    import os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    from SQL_Tools import (
        _sanitize_identifier, _sanitize_table_name, _sanitize_column_name,
        _is_bool, _is_int, _is_float, _is_date, _is_datetime, _infer_data_type,
        upload_csv, find_words_in_query, find_suggestions,
        window as sql_tools_window
    )

QtWidgets = MOCK_QT_MODULES['PyQt5.QtWidgets']


class TestSanitizeIdentifier(unittest.TestCase):
    def test_valid_names(self):
        self.assertEqual(_sanitize_identifier("valid_name"), "valid_name")
        self.assertEqual(_sanitize_identifier("ValidName123"), "ValidName123")

    def test_names_with_spaces(self):
        self.assertEqual(_sanitize_identifier("name with spaces"), "name_with_spaces")

    def test_names_with_special_chars(self):
        self.assertEqual(_sanitize_identifier("name-with-hyphens!@#"), "name_with_hyphens_")
        self.assertEqual(_sanitize_identifier("test(parentheses)"), "test_parentheses_")

    def test_names_starting_with_numbers(self):
        self.assertEqual(_sanitize_identifier("123name"), "_123name")

    def test_names_too_long(self):
        long_name = "a" * 100
        sanitized = _sanitize_identifier(long_name)
        self.assertEqual(len(sanitized), 63) 
        self.assertTrue(sanitized.startswith("a" * 63))

    def test_empty_or_problematic_names(self):
        self.assertEqual(_sanitize_identifier(""), "default_identifier")
        self.assertEqual(_sanitize_identifier(None), "default_identifier")
        self.assertEqual(_sanitize_identifier("   "), "default_identifier")
        self.assertEqual(_sanitize_identifier("_"), "_") 
        self.assertEqual(_sanitize_identifier("__"), "_") 
        self.assertEqual(_sanitize_identifier("___"), "_")
        self.assertEqual(_sanitize_identifier("!@#$"), "_") 

    def test_specific_column_sanitization(self):
        self.assertEqual(_sanitize_column_name("First Name"), "First_Name")
        self.assertEqual(_sanitize_column_name("Address (Street)"), "Address_Street_")
        self.assertEqual(_sanitize_column_name("data-value"), "data_value")
        self.assertEqual(_sanitize_column_name("@timestamp"), "_timestamp")
        self.assertEqual(_sanitize_column_name("123_ID"), "_123_ID")


class TestInferDataType(unittest.TestCase):
    def test_pure_boolean_text(self): 
        self.assertEqual(_infer_data_type(["true", "false", "yes", "no", "T", "F"]), "BOOLEAN")
        self.assertEqual(_infer_data_type([True, False]), "BOOLEAN") 

    def test_pure_boolean_numeric(self): 
        self.assertEqual(_infer_data_type(["0", "1"]), "FLOAT") 
        self.assertEqual(_infer_data_type([0, 1]), "FLOAT")   

    def test_pure_int(self):
        self.assertEqual(_infer_data_type(["10", "200", "-5", "0"]), "FLOAT") 
        
    def test_mixed_bool_int(self):
        self.assertEqual(_infer_data_type(["1", "0", "true"]), "FLOAT") 

    def test_pure_float(self):
        self.assertEqual(_infer_data_type(["10.1", "200.0", "-5.5", "0.0"]), "FLOAT")
        self.assertEqual(_infer_data_type(["1", "2.5", "true"]), "FLOAT") 

    def test_pure_date(self):
        self.assertEqual(_infer_data_type(["2023-01-01", "12/31/2022", "15-07-2021"]), "DATE")

    def test_pure_datetime(self):
        self.assertEqual(_infer_data_type(["2023-01-01 10:00:00", "2022-12-31 23:59:59"]), "DATETIME")

    def test_mixed_int_float(self):
        self.assertEqual(_infer_data_type(["10", "20.5", "30"]), "FLOAT")

    def test_mixed_numeric_string(self):
        self.assertEqual(_infer_data_type(["10", "20.5", "hello"]), "VARCHAR(255)")
        self.assertEqual(_infer_data_type(["10", "20.5", "very long string data"]), "VARCHAR(255)")

    def test_mixed_date_datetime(self):
        self.assertEqual(_infer_data_type(["2023-01-01", "2023-01-01 10:00:00"]), "DATETIME")

    def test_all_empty_or_none(self):
        self.assertEqual(_infer_data_type(["", None, " ", None]), "VARCHAR(255)")
        self.assertEqual(_infer_data_type([]), "VARCHAR(255)")

    def test_varchar_length_determination(self):
        self.assertEqual(_infer_data_type(["hello", "world"]), "VARCHAR(255)")
        medium_string = "x" * 500
        self.assertEqual(_infer_data_type([medium_string, "text"]), f"VARCHAR(500)")
        very_long_string = "y" * 1200
        self.assertEqual(_infer_data_type([very_long_string, "text"]), f"VARCHAR(1024)")
        self.assertEqual(_infer_data_type(["123", "test", very_long_string]), "VARCHAR(1024)")


class TestUploadCSV(unittest.TestCase):
    def setUp(self):
        self.patcher_qfiledialog = patch('SQL_Tools.QFileDialog.getOpenFileName')
        self.mock_get_open_file_name = self.patcher_qfiledialog.start()

        self.mock_text_create_query = MagicMock()
        self.patcher_text_widget = patch('SQL_Tools.text_create_query', self.mock_text_create_query)
        self.patcher_text_widget.start()
        
        self.patcher_qmessagebox = patch('SQL_Tools.QMessageBox') 
        self.mock_qmessagebox_constructor = self.patcher_qmessagebox.start()
        
        self.patcher_sql_tools_window = patch('SQL_Tools.window', new_callable=MagicMock)
        self.mock_sql_tools_window = self.patcher_sql_tools_window.start()

    def tearDown(self):
        self.patcher_qfiledialog.stop()
        self.patcher_text_widget.stop()
        self.patcher_qmessagebox.stop()
        self.patcher_sql_tools_window.stop()

    def test_successful_csv_upload(self):
        csv_content = "Name,Age,City\nAlice,30,New York\nBob,24,Los Angeles\nCharlie,N/A,Chicago"
        self.mock_get_open_file_name.return_value = ("/fake/path/test.csv", "CSV files (*.csv)")
        
        with patch('builtins.open', mock_open(read_data=csv_content)):
            upload_csv() 

        expected_query_parts = [
            'CREATE TABLE "test" (',
            '"Name" VARCHAR(255),',
            '"Age" VARCHAR(255),', 
            '"City" VARCHAR(255)', 
            ');'
        ]
        actual_query = self.mock_text_create_query.setPlainText.call_args[0][0]
        
        for part in expected_query_parts:
            self.assertIn(part, actual_query)
        self.assertTrue(actual_query.endswith(");"))
        self.mock_qmessagebox_constructor.warning.assert_not_called()

    def test_empty_csv_file(self):
        self.mock_get_open_file_name.return_value = ("/fake/path/empty.csv", "CSV files (*.csv)")
        with patch('builtins.open', mock_open(read_data="")):
            upload_csv()
        self.mock_qmessagebox_constructor.warning.assert_any_call(self.mock_sql_tools_window, "Empty CSV File", "The selected CSV file is empty.")

    def test_csv_with_header_only(self):
        self.mock_get_open_file_name.return_value = ("/fake/path/header_only.csv", "CSV files (*.csv)")
        with patch('builtins.open', mock_open(read_data="Header1,Header2\n")):
            upload_csv()
        self.mock_qmessagebox_constructor.warning.assert_any_call(self.mock_sql_tools_window, "No Data Rows", "The CSV file contains a header but no data rows for analysis.")

    def test_ragged_rows_csv(self):
        csv_content = "ColA,ColB,ColC\nVal1,Val2,Val3\nVal4,Val5\nVal6,Val7,Val8,Val9Extra"
        self.mock_get_open_file_name.return_value = ("/fake/path/ragged.csv", "CSV files (*.csv)")
        
        with patch('builtins.open', mock_open(read_data=csv_content)):
            upload_csv()
        
        self.mock_qmessagebox_constructor.warning.assert_any_call(
            self.mock_sql_tools_window,
            "Inconsistent Column Count",
            "Data row 2 has 2 columns, but the header has 3. Data type inference will be based on available data, padding short rows with None."
        )
        self.mock_qmessagebox_constructor.warning.assert_any_call(
            self.mock_sql_tools_window,
            "Inconsistent Column Count",
            "Data row 3 has 4 columns, but the header has 3. Data type inference will be based on available data, padding short rows with None."
        )
        self.mock_text_create_query.setPlainText.assert_called()


class TestFindWordsInQuery(unittest.TestCase):
    def test_simple_whole_word(self):
        res = find_words_in_query(["word"], "This is a word in a sentence.")
        self.assertIn("word", res)
        self.assertEqual(len(res["word"]), 1)
        self.assertEqual(res["word"][0][1], "word") 

    def test_case_insensitivity(self):
        res = find_words_in_query(["Word"], "this is a wOrD.")
        self.assertIn("Word", res) 
        self.assertEqual(res["Word"][0][1], "wOrD") 

    def test_adjacent_punctuation(self):
        res = find_words_in_query(["word"], "word, (word) schema.word word;")
        self.assertEqual(len(res["word"]), 4)

    def test_no_substring_match(self):
        self.assertNotIn("cat", find_words_in_query(["cat"], "This is a catalog."))
        self.assertIn("cat", find_words_in_query(["cat"], "The cat sat."))

    def test_multiple_words_and_occurrences(self):
        query = "SELECT col1 FROM table1 WHERE col1 = 'val' AND table1.active = true"
        words = ["col1", "table1"]
        res = find_words_in_query(words, query)
        self.assertIn("col1", res)
        self.assertEqual(len(res["col1"]), 2)
        self.assertIn("table1", res)
        self.assertEqual(len(res["table1"]), 2)


class TestFindSuggestions(unittest.TestCase):
    def test_columns_simple_and_qualified(self):
        query = "SELECT a, t.b, sch.tab.c FROM sch.tab t"
        sugg = find_suggestions(query)
        self.assertIn("a", sugg['Columns'])
        self.assertIn("t.b", sugg['Columns'])
        self.assertIn("sch.tab.c", sugg['Columns'])

    def test_columns_aliases(self):
        query = "SELECT customer_name AS name, o.order_id AS \"Order ID\" FROM customers c JOIN orders o ON c.id = o.cid"
        sugg = find_suggestions(query)
        self.assertIn("customer_name", sugg['Columns'])
        self.assertIn("o.order_id", sugg['Columns'])

    def test_columns_functions(self):
        query = "SELECT COUNT(*), SUM(price), CONCAT(first, last) AS full_name FROM orders"
        sugg = find_suggestions(query)
        self.assertIn("COUNT(*)", sugg['Columns'])
        self.assertIn("SUM(price)", sugg['Columns'])
        self.assertIn("price", sugg['Columns']) 
        self.assertIn("CONCAT(first, last)", sugg['Columns'])
        self.assertIn("first", sugg['Columns']) 
        self.assertIn("last", sugg['Columns'])

    def test_columns_asterisk(self):
        query = "SELECT *, t.* FROM table1 t"
        sugg = find_suggestions(query)
        self.assertIn("*", sugg['Columns'])
        self.assertIn("t.*", sugg['Columns'])

    def test_tables_simple_aliases_joins(self):
        query = "FROM table1 t1, schema.table2 AS t2 JOIN another_table j_t ON t1.id = j_t.id LEFT JOIN tbl_extra AS te ON t1.id = te.id"
        sugg = find_suggestions(query)
        self.assertIn("table1", sugg['Tables'])
        self.assertIn("schema.table2", sugg['Tables'])
        self.assertIn("another_table", sugg['Tables'])
        self.assertIn("tbl_extra", sugg['Tables'])


    def test_filters_simple_qualified_complex(self):
        query = "WHERE a = 1 AND t1.b > 'text' OR (sch.t2.c LIKE '%val%' AND d IN (1,2,3) AND is_active)"
        sugg = find_suggestions(query)
        self.assertIn("a", sugg['Filters'])
        self.assertIn("t1.b", sugg['Filters'])
        self.assertIn("sch.t2.c", sugg['Filters'])
        self.assertIn("d", sugg['Filters'])
        self.assertIn("is_active", sugg['Filters']) 


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
