### olympic athlete bio

- some athletes have height and/or weight unrecorded
- some athletes don't have their birthday recorded, or only shows some information like their birth yar and nothing else
- some athletes have their weight shown in a range rather than an absolute value
- birthday formatting is somewhat inconsistent (`DD-MM-YY`) or (`DD MMMMMM YYYY`), etc

### olympic athlete events
- in the beginning, some athletes have a `DNS` status, yet shows shome extra information

### olympics games
- start/end date and competition date in some countries are inconsistent, for instance, the 1928 Winter olympics lists their end date earlier than the end date shown in the competition date

## Paris

### athletes
- Not all height and weight data is recorded for each athlete
- Not all birth and/or residence data is recorded for each athlete

### medalists
- Not all athletes have a team associated with them (makes sense if their sport is individual only)

### noc
- AIN and USSR's country codes are used in place of their country names.

### teams
- Not all teams have a coach associated with them (makes sense if they're self-coached)

# How do we deal with wrong/unknown data?

For unknown data, depending on the kind of data listed (number or string), we would have to probably set specific values like unknown numbers as negative like -1 and unknown data that uses strings to show some kind of place holder like "N/A" to show that this specific piece of data is unavailable.

For data that doesn't have a specific format, we would have to choose one specific format to follow. For instance, we can convert all birthdays to "dd-Mon-yyyy". If some data is missing or unavailable, we would have to only list out the available information or choose "N/A". I chose this specific format to account for these edge cases.

# How would we incorporate the Paris data?

When inserting the Paris data into the main data files, we would first have to check if the record already exists in the main file. For instance, the athlete's name, gender, birthday, etc, in a record can be compared to the main file to see if it exists. If they're found to participate in the Paris Olympics with another country not listed in the main file, that country and country code should be added to their record. To generate an unique ID for newly added athletes, we can get the latest or largest code number in the existing data and increment it by 1 to create a new ID and avoid existing IDs. To handle Paris events' duplicates, we can do the same by matching event name to see if it already exists or needs new data entries.