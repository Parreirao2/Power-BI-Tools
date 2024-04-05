foreach (var column in Selected.Columns)
{
if (column.DataType == TabularEditor.TOMWrapper.DataType.String)  
{ 
    
foreach(var c in Selected.Columns)
{  
    var _blankRowsCount =
    EvaluateDax("CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISBLANK(" + c.DaxObjectFullName + "))");
    var _percentageBlanks =
    EvaluateDax("FORMAT(DIVIDE(CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISBLANK(" + c.DaxObjectFullName + ")), CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "))), \"0%\")");
    var _errorRowsCount =
    EvaluateDax("CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISERROR(" + c.DaxObjectFullName + "))");
    var _percentageErrors =
    EvaluateDax("FORMAT(DIVIDE(CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISERROR(" + c.DaxObjectFullName + ")), CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "))), \"0%\")");

    var _result = 
    "\nInformation:" + Environment.NewLine +
    "\n   Name: " + c.Name + Environment.NewLine +
    "\n   Description: " + c.Description + Environment.NewLine +
    "\n   FormatString: " + c.FormatString + Environment.NewLine +
    "\n   DataType: " + c.DataType + Environment.NewLine +
    "\n   IsHidden: " + c.IsHidden + Environment.NewLine + Environment.NewLine +
    "\n   Blank Rows: " + _blankRowsCount +  Environment.NewLine +
    "\n   Blanks (%): " + _percentageBlanks +  Environment.NewLine + 
    "\n   Rows with Error: " + _errorRowsCount +  Environment.NewLine +
    "\n   Errors (%): " + _percentageErrors +  Environment.NewLine +  Environment.NewLine;
   
_result.ToString().Output(); 
}
}
if (column.DataType == TabularEditor.TOMWrapper.DataType.DateTime)
{
foreach(var c in Selected.Columns)
{    
    var _firstdate = 
    EvaluateDax("FirstDate(" + c.DaxObjectFullName + ")");
    var _lastdate =
    EvaluateDax("LastDate(" + c.DaxObjectFullName + ")");
    var _earliestDate =
    EvaluateDax("MIN(" + c.DaxObjectFullName + ")");   
    var _latestDate =
    EvaluateDax("MAX(" + c.DaxObjectFullName + ")");
    var _numberOfDays =
    EvaluateDax("COUNTROWS(VALUES(" + c.DaxObjectFullName + "))");  
    var _distinctDateCount =
    EvaluateDax("DISTINCTCOUNT(" + c.DaxObjectFullName + ")");    
    var _countSun =
    EvaluateDax("COUNTROWS(FILTER(" + Selected.Table.DaxObjectFullName + ", WEEKDAY("  + c.DaxObjectFullName + ") = 1))");
    var _countMon =
    EvaluateDax("COUNTROWS(FILTER(" + Selected.Table.DaxObjectFullName + ", WEEKDAY("  + c.DaxObjectFullName + ") = 2))");
    var _countTue =
    EvaluateDax("COUNTROWS(FILTER(" + Selected.Table.DaxObjectFullName + ", WEEKDAY(" + c.DaxObjectFullName + ") = 3))");
    var _countWed =
    EvaluateDax("COUNTROWS(FILTER(" + Selected.Table.DaxObjectFullName + ", WEEKDAY(" + c.DaxObjectFullName + ") = 4))");
    var _countThu =
    EvaluateDax("COUNTROWS(FILTER(" + Selected.Table.DaxObjectFullName + ", WEEKDAY(" + c.DaxObjectFullName + ") = 5))");
    var _countFri =
    EvaluateDax("COUNTROWS(FILTER(" + Selected.Table.DaxObjectFullName + ", WEEKDAY(" + c.DaxObjectFullName + ") = 6))");
    var _countSat =
    EvaluateDax("COUNTROWS(FILTER(" + Selected.Table.DaxObjectFullName + ", WEEKDAY(" + c.DaxObjectFullName + ") = 7))");
    var _blankRowsCount =
    EvaluateDax("CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISBLANK(" + c.DaxObjectFullName + "))");
    var _percentageBlanks =
    EvaluateDax("FORMAT(DIVIDE(CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISBLANK(" + c.DaxObjectFullName + ")), CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "))), \"0%\")");
    var _errorRowsCount =
    EvaluateDax("CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISERROR(" + c.DaxObjectFullName + "))");
    var _percentageErrors =
    EvaluateDax("FORMAT(DIVIDE(CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISERROR(" + c.DaxObjectFullName + ")), CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "))), \"0%\")");

    var _result = 
    "\nInformation:" + Environment.NewLine +
    "\n   Name: " + c.Name + Environment.NewLine +
    "\n   Description: " + c.Description + Environment.NewLine +
    "\n   FormatString: " + c.FormatString + Environment.NewLine +
    "\n   DataType: " + c.DataType + Environment.NewLine +
    "\n   IsHidden: " + c.IsHidden + Environment.NewLine + 
    Environment.NewLine +
    
    "\n   Blank Rows: " + _blankRowsCount +  Environment.NewLine +
    "\n   Blanks (%): " + _percentageBlanks +  Environment.NewLine + 
    "\n   Rows with Error: " + _errorRowsCount +  Environment.NewLine +
    "\n   Errors (%): " + _percentageErrors +  Environment.NewLine +
    Environment.NewLine + 
 
    "\nAnalysis:" + Environment.NewLine +
    "\n   First Date: " + _firstdate + Environment.NewLine +
    "      Description: Earliest date in the selected column" + Environment.NewLine +
    "      DAX Measure: MIN('" + Selected.Table.Name + "'[" + c.Name + "])" + Environment.NewLine + Environment.NewLine +

    "\n   Last Date: " + _lastdate + Environment.NewLine +
    "      Description: Latest date in the selected column" + Environment.NewLine +
    "      DAX Measure: LASTDATE('" + Selected.Table.Name + "'[" + c.Name + "])" + Environment.NewLine + Environment.NewLine +

    "\n   Earliest Date: " + _earliestDate + Environment.NewLine +
    "      Description: Minimum date value in the entire table" + Environment.NewLine +
    "      DAX Measure: MIN('" + Selected.Table.Name + "'[" + c.Name + "])" + Environment.NewLine + Environment.NewLine +

    "\n   Latest Date: " + _latestDate + Environment.NewLine +
    "      Description: Maximum date value in the entire table" + Environment.NewLine +
    "      DAX Measure: MAX('" + Selected.Table.Name + "'[" + c.Name + "])" + Environment.NewLine + Environment.NewLine +

    "\n   Number of Days: " + _numberOfDays + Environment.NewLine +
    "      Description: Count of unique days in the selected column" + Environment.NewLine +
    "      DAX Measure: COUNTROWS(VALUES('" + Selected.Table.Name + "'[" + c.Name + "]))" + Environment.NewLine + Environment.NewLine +

    "\n   Distinct Date Count: " + _distinctDateCount + Environment.NewLine +
    "      Description: Count of distinct dates in the selected column" + Environment.NewLine +
    "      DAX Measure: DISTINCTCOUNT('" + Selected.Table.Name + "'[" + c.Name + "])" + Environment.NewLine + Environment.NewLine +

    "\n   Day of Week Distribution: " + _countSun + " (Sun), " + _countMon + " (Mon), " + _countTue + " (Tue), " + _countWed + " (Wed), " + _countThu + " (Thu), " + _countFri + " (Fri), " + _countSat + " (Sat)" + Environment.NewLine +
    "      Description: Count of occurrences for each day of the week in the selected column" + Environment.NewLine +
    "      DAX Measure: COUNTROWS(FILTER('" + Selected.Table.Name + "', WEEKDAY('" + Selected.Table.Name + "'[" + c.Name + "]) = 1)) & \" (Sun), \" "+  Environment.NewLine + Environment.NewLine;
                    
_result.ToString().Output();
}
}
if (column.DataType != TabularEditor.TOMWrapper.DataType.String &&
    column.DataType != TabularEditor.TOMWrapper.DataType.Boolean &&
    column.DataType != TabularEditor.TOMWrapper.DataType.DateTime)
{
 
foreach(var c in Selected.Columns)
{
    var _max = 
    EvaluateDax("MAX(" + c.DaxObjectFullName + ")");
    var _min = 
    EvaluateDax("MIN(" + c.DaxObjectFullName + ")");
    var _range =
    EvaluateDax(_max + " - " + _min);
    var _avg = 
    EvaluateDax("ROUND(AVERAGE(" + c.DaxObjectFullName + "),2)");
    var _sum = 
    EvaluateDax("SUM(" + c.DaxObjectFullName + ")");
    var _dist = 
    EvaluateDax("DISTINCTCOUNT(" + c.DaxObjectFullName + ")");
    var _count =
    EvaluateDax("COUNT(" + c.DaxObjectFullName + ")");
    var _countrows = 
    EvaluateDax("FORMAT( COUNTROWS (" + Selected.Table.DaxObjectFullName + "), \"#,##0\" )");
    var _median =
    EvaluateDax("MEDIANX(" + Selected.Table.DaxObjectFullName + "," + c.DaxObjectFullName + " )");
    var _stdev =
    EvaluateDax("ROUND(STDEV.P(" + c.DaxObjectFullName + " ),2)");
    var _variance =
    EvaluateDax("ROUND(VAR.P(" + c.DaxObjectFullName + " ),2)");
    var _25Perc = 
    EvaluateDax("PERCENTILEX.INC(" + Selected.Table.DaxObjectFullName +", "  + c.DaxObjectFullName +  ", 0.25)");
    var _75Perc =
    EvaluateDax("PERCENTILEX.INC(" + Selected.Table.DaxObjectFullName +", "  + c.DaxObjectFullName +  ", 0.75)");
    var _cv = 
    EvaluateDax("DIVIDE(" + _stdev + ", " + _avg + ", 0)");
    var _blankRowsCount =
    EvaluateDax("CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISBLANK(" + c.DaxObjectFullName + "))");
    var _percentageBlanks =
    EvaluateDax("FORMAT(DIVIDE(CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISBLANK(" + c.DaxObjectFullName + ")), CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "))), \"0%\")");
    var _errorRowsCount =
    EvaluateDax("CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISERROR(" + c.DaxObjectFullName + "))");
    var _percentageErrors =
    EvaluateDax("FORMAT(DIVIDE(CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "), ISERROR(" + c.DaxObjectFullName + ")), CALCULATE(COUNTROWS(" + Selected.Table.DaxObjectFullName + "))), \"0%\")");

    var _result = 
    "\nInformation:" + Environment.NewLine +
    "\n   Name: " + c.Name + Environment.NewLine +
    "\n   Description: " + c.Description + Environment.NewLine +
    "\n   FormatString: " + c.FormatString + Environment.NewLine +
    "\n   DataType: " + c.DataType + Environment.NewLine +
    "\n   IsHidden: " + c.IsHidden + Environment.NewLine +
    "\n   Summarization: " + c.SummarizeBy + Environment.NewLine +
   Environment.NewLine +
    
    "\n   Blank Rows: " + _blankRowsCount +  Environment.NewLine +
    "\n   Blanks (%): " + _percentageBlanks +  Environment.NewLine + 
    "\n   Rows with Error: " + _errorRowsCount +  Environment.NewLine +
    "\n   Errors (%): " + _percentageErrors +  Environment.NewLine +
   Environment.NewLine + 
  
    "\nAnalysis:" + Environment.NewLine +
    "\n   Count: " + _count +  Environment.NewLine +" (Total count of non-null values)" + Environment.NewLine +
    "      DAX Measure: COUNT(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + ")" + Environment.NewLine + Environment.NewLine +
    "\n   Sum: " + _sum +  Environment.NewLine +" (Total sum of values)" + Environment.NewLine +
    "      DAX Measure: SUM(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + ")" + Environment.NewLine + Environment.NewLine +
    "\n   Avg: " + _avg +  Environment.NewLine +" (Average value, rounded to 2 decimal places)" + Environment.NewLine +
    "      DAX Measure: ROUND(AVERAGE(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + "), 2)" + Environment.NewLine + Environment.NewLine +
    "\n   Max: " + _max +  Environment.NewLine +" (Maximum value)" + Environment.NewLine +
    "      DAX Measure: MAX(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + ")" + Environment.NewLine + Environment.NewLine +
    "\n   Min: " + _min +  Environment.NewLine +" (Minimum value)" + Environment.NewLine +
    "      DAX Measure: MIN(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + ")" + Environment.NewLine + Environment.NewLine +
    "\n   Range: " + _range + Environment.NewLine + " (Range between the maximum and minimum values)" + Environment.NewLine +
    "      DAX Measure: MAX(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + ") - MIN(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + ")" + Environment.NewLine + Environment.NewLine +
    "\n   Distinct: " + _dist + Environment.NewLine + " (Count of distinct values)" + Environment.NewLine +
    "      DAX Measure: DISTINCTCOUNT(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + ")" + Environment.NewLine + Environment.NewLine +
    "\n   CountRows: " + _countrows + Environment.NewLine + " (Number of rows in the table)" + Environment.NewLine +
    "      DAX Measure: FORMAT(COUNTROWS(" + "'"+Selected.Table.Name+"'" + "), \"#,##0\")" + Environment.NewLine + Environment.NewLine +
    "\n   Median: " + _median + Environment.NewLine + " (Median value)" + Environment.NewLine +
    "      DAX Measure: MEDIANX(" + "'"+Selected.Table.Name+"'" + ", " + "'"+Selected.Table.Name+"'["+c.Name+"]" + ")" + Environment.NewLine + Environment.NewLine +
    "\n   Standard Deviation: " + _stdev + Environment.NewLine + " (Standard deviation of values, rounded to 2 decimal places)" + Environment.NewLine +
    "      DAX Measure: ROUND(STDEV.P(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + "), 2)" + Environment.NewLine + Environment.NewLine +
    "\n   Variance: " + _variance + Environment.NewLine + " (Variance of values, rounded to 2 decimal places)" + Environment.NewLine +
    "      DAX Measure: ROUND(VAR.P(" + "'"+Selected.Table.Name+"'["+c.Name+"]" + "), 2)" + Environment.NewLine + Environment.NewLine +
    "\n   25th Percentile: " + _25Perc + Environment.NewLine + " (25th percentile to understand the distribution of values)" + Environment.NewLine +
    "      DAX Measure: PERCENTILEX.INC(" + "'"+Selected.Table.Name+"'" + ", " + "'"+Selected.Table.Name+"'["+c.Name+"]" + ", 0.25)" + Environment.NewLine + Environment.NewLine +
    "\n   75th Percentile: " + _75Perc + Environment.NewLine + " (75th percentile to understand the distribution of values)" + Environment.NewLine +
    "      DAX Measure: PERCENTILEX.INC(" + "'"+Selected.Table.Name+"'" + ", " + "'"+Selected.Table.Name+"'["+c.Name+"]" + ", 0.75)" + Environment.NewLine + Environment.NewLine +
    "\n   Coefficient of Variation: " + _cv + Environment.NewLine + " (Measures the relative variability of the data, expressed as a percentage of the mean.)" + Environment.NewLine +
    "      DAX Measure: DIVIDE(" + _stdev + Environment.NewLine + ", " + _avg + ", 0)" + Environment.NewLine;
 
    _result.ToString().Output();
}
}
}


