import PySimpleGUI as sg
import re

def find_words_in_query(words_list, sql_query):
    found_words = {}
    lines = sql_query.split('\n')
    for i, line in enumerate(lines, start=1):
        for word in words_list:
            matches = re.findall(r'\b{}\b'.format(re.escape(word)), line, re.IGNORECASE)
            if matches:
                if word in found_words:
                    found_words[word].append((i, len(matches)))
                else:
                    found_words[word] = [(i, len(matches))]
    return found_words

layout = [
    [sg.Text("Enter words to find (comma-separated):")],
    [sg.InputText(key="-WORDS-")],
    [sg.Text("Enter SQL Query:")],
    [sg.Multiline(key="-QUERY-", size=(50, 10))],
    [sg.Button("Find", key="-FIND-")],
    [sg.Text("Words found in the query:")],
    [sg.Multiline(key="-FOUND-", size=(50, 5))],
]

window = sg.Window("Word Search in SQL Query", layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-FIND-":
        words_to_find = [word.strip() for word in values["-WORDS-"].split(",")]
        sql_query = values["-QUERY-"]
        found_words = find_words_in_query(words_to_find, sql_query)

        found_output = []
        for word, occurrences in found_words.items():
            found_output.append(f"{word}:")
            for line_num, count in occurrences:
                found_output.append(f"  - Line {line_num}: {count} occurrence(s)")

        window["-FOUND-"].update("\n".join(found_output))

window.close()
