<img align='right' src="https://github-readme-stats.vercel.app/api?username=parreirao2&show_icons=true&title_color=023047&text_color=023047&icon_color=219ebc&bg_color=8ecae6&cache_seconds=2300" alt="My Github Stats">

### Hi, my name is Diogo Parreirão!

<img src="https://img.shields.io/static/v1?label=Overview&message=Parreirao2&color=f8efd4&style=for-the-badge&logo=GitHub&link=https://www.linkedin.com/in/diogo-parreirao-030006173/" alt="Static GitHub">

<p>I like creating cool and useful python scripts<br/> I hope you can find something useful in here.</p>
<a href="#" title="LinkedIn">
  <img src="https://img.shields.io/badge/-Linkedin-0e76a8?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/diogo-parreirao-030006173/" alt="LinkedIn"/></a>  

###### [Alternative Link](https://www.linkedin.com/in/diogo-parreirao-030006173/)
---

#  Current Projects:


## InfoHelper

InfoHelper is a C# Script that you can import to your Tabular Editor and use as a macro by right-clicking on any column and see it's specific profile analysis.

Currently the script works on columns of the type: Strings, Int64, DateTime and Boolean.
Each column type has a specific analysis based on it's type, and each type has a set of already created DAX Measures that you can easily copy/paste from the pop-up window and use to create as a new measure. These Measures already show their results, so that you can know what output to expect when creating them.

The script is created in a user-friendly code structure that you can easily edit and adapt to your liking. The code for each measure is written in DAX so that you don't need to know C# to add your own analysis, you can just type your DAX Measure!

### Features:
String Columns Analysis:

Calculates the count and percentage of blank rows.
Calculates the count and percentage of error rows.
Outputs column information including name, description, format string, data type, and visibility.

DateTime Columns Analysis:

Determines the first and last dates.
Calculates the earliest and latest dates.
Computes the number of unique days and distinct date count.
Counts occurrences for each day of the week.
Calculates the count and percentage of blank and error rows.
Outputs detailed column information and statistics.

Int64 Columns Analysis:

Calculates maximum, minimum, and range.
Computes average, sum, and distinct count.
Determines the count of non-null values and total rows.
Calculates median, standard deviation, variance, and percentiles.
Calculates the count and percentage of blank and error rows.
Outputs detailed column information and statistics.

### How to use:

- Open Tabular Editor and load your model.
- Click on C# Script
- Paste the Script code
- Click on +
- Name the Macro
- Select Column from the list and click OK

Run the Script:
The script will iterate through each selected column by simply:
- Right-Clicking a column
- Select Macros and then choose the new script

- Depending on the data type of each column, it will perform the respective analysis.
- The results will be displayed in a output window that can be copy/pasted anywhere you want.

### Get it here:
[Lastest Version](https://github.com/Parreirao2/Power-BI-Tools/tree/main/InfoHelper)


## Page Editor (for Power BI (.pbix) files)

This Python script provides a graphical user interface (GUI) to edit the ordinal values and names of pages within a Power BI report (.pbix) file.

### How to Use:
Open the Application: Run the script to open the Page Switcher GUI.
Select PBIX File: Click the "Select PBIX File" button to choose the Power BI file you want to edit. (at this point there will be a newly created .zip file in your folder, don't delete it or change anything inside it, as this is the .pbix file converted to a .zip and the script is reading it's JSON files)
Edit Page: Double-click on a page in the list to edit its ordinal value and name in the pop-up window. You can also change the Width and Height of the page, set it to hidden or unhidden and even choose the page type.
Search Box: Just type the name of the Table, Measure or Column, and the app will only display the pages and visuals which have these fields.
Delete Page: Click on the checkbox to select which page(s) you would like to Delete, then click on delete button on the bottom.
Duplicate Page: Click on the checkbox to select which page(s) you would like to Duplicate, then click on duplicate button on the bottom. (the new pages will always have the higest ordinal value available, meaning, the will always go to the bottom of the list)
Save Changes: Click the "Save Changes" button to save your edits. A new PBIX file will be created with '_ChangedOrdinality.pbix' appended to the original file name. (the reason why a new .pbix file is created is simply to prevent possible losses. You can open this new .pbix and check the changes yourself, and if you're happy with them, just save over the original .pbix file.)

### Important Notes:
Ensure the new PBIX file is not open when saving changes. Always keep backups of your original PBIX files before making any edits.

### Download
[Latest Version](https://github.com/Parreirao2/Power-BI-Tools/releases/tag/PageSwitcher)


## Sample Generator + SQL Tools

This script provides a user-friendly interface for SQL query analysis, CSV generation, and SQL CREATE TABLE statement generation. It combines the power of PyQt5 for the GUI, Faker for data generation, and regular expressions for SQL parsing and suggestions.

- Find specific words in a SQL query and provide suggestions. This could be useful on very large SQL Queries, by providing each line number and each statement where the word was found.
- Generate CSV files with random data of different sample types. You can choose to generate a .csv with as many rows as you'd like, and define which template to use from the following: Personel, Financial, Employee and Customer.
- Upload a CSV file and generate a SQL CREATE TABLE statement based on its contents. The script will automaticaly determine the datatype of each column and provide an already "ready to run" query.

### How to use:

Find Words:
- Use the first box to enter each word you want to search for, separated by commas ",".
- Use the second box to enter your Query
- Click on "Find Words"

Note: Currently Search Suggestions is a Work-In-Progress

Create Table:
- Click Upload CSV
- Profit.

Generate CSV:
- Use the first box to define how many rows you want your CSV file to have
- Choose the Sample type from the dropdown list
- Click Generate CSV
- Choose the location where you want to save this .csv


### Download
[Latest Version](https://github.com/Parreirao2/Power-BI-Tools/releases/tag/SQLTools)
