import csv
import ParisMerge
from datetime import datetime
from hashmap import HashMap

# format "born" column
def format_born_date(str_date, comp_year: int = -1):
    # empty/missing dates
    if not str_date or not str(str_date).strip():
        return ""
    
    # convert date to string and remove whitespaces
    str_date = str(str_date).strip()
    
    # list expected formats
    formats = [
        '%d-%b-%y', # 10-Apr-99
        '%d-%b-%Y', # 10-Apr-1999
        '%d %B %Y', # 10 April 1999
        '%Y',       # 1999
        '%B %Y',    # April 1999
    ]
    
    # parsing using each expected format
    for fmt in formats:
        try:
            dt = datetime.strptime(str_date, fmt)
            # handle 2 digit years (past or future) by comparing to the current year
            y = dt.year
            if dt.year > datetime.now().year:
                y = dt.year - 100
            comp_num = comp_year - y
            # compares if the year chosen is bigger than the olympic year if passed
            # adjusts if needed
            if (comp_year > -1 and comp_num< 0):
                y = y - 100
            dt = dt.replace(year=y)
            # return date with the correct format
            return dt.strftime('%d-%b-%Y')
        # if fail, try the next format
        except ValueError:
            continue
    # return empty if all formats failed
    return ""

# open data to clean and write result to a results file
def clean_data(input_file, output_file, events : list = None):

    if (events is None): events = ParisMerge.read_csv("olympic_athlete_event_results.csv")
    events = HashMap.convert_from_list(events, None, "athlete_id", False)
    # open file for reading (with column headers)
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    # clean each row from the data using the function format_born_date for formatting
    for row in rows:
        
        # tries to compare an olympic year to athlete loaded year for validation
        e = events.find(row["athlete_id"])
        e_year = e["\ufeffedition"].split(" ")[0]
        
        row['born'] = format_born_date(row['born'], int(e_year))
    
    # open file to write the results
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# define the files
input_file = "olympic_athlete_bio.csv"
output_file = "new_olympic_athlete_bio.csv"
# execute the cleaning function
clean_data(input_file, output_file)