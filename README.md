README: CS50 Final Project for David Sissman

COVID in Florida for Collier

Brief Description: My website presents a concise summary of current COVID data that are most interesting for residents of Collier County FL.

Background: The Florida Department of Health provides lots of information daily about COVID case counts, hospitalizations, deaths, tests, and more every day. But there are 70 counties in Florida, and the most legible data comes out in PDF format every day. For far Southwest Florida, which is moderately populated, we can easily be affected by some major population centers to our east and north. I wanted to make it easier to look at the summary data every day.

Mechanics: This website uses Python, Pandas, Flask, and Javascript to go through the following processes:

1) Checks an existing file called COVIDFL.csv to find out over which dates the program needs to run.

2) Goes to an open data source at the University of South Florida which has already compiled tables of COVID data by county. There are 67 counties, plus "Unknown." This incorporates a number of steps to make sure that the right data exists.

3) For each date not already in COVIDFL.csv, it gets the appropriate file (zipped or CSV), opens it, parses the data, and appends it to the COVIDFL.csv file. In the data file, each day shows the cumulative numbers.

4) Groups data into the 8 most relevant regions to Collier County residents: Collier County, Lee County, South Florida (Miami-Dade, Broward, Palm Beach), Tampa (Hillsborough, Pinellas), Orlando (Orange, Osceola, Polk), Jacksonville (St. Johns, Duval), Rest of Florida, and the entire state.

5) For the last day reported, calculates the relevant statistics: changes in cases, hospitalizations, deaths, and tests, as well as percent positive tests.

6) For the prior 7 days, calculates the 7-day average for each of the relevant metrics.

7) Formats all of the calculated data into two lists of strings that are passed to an HTML template.

8) Presents the data in HTML in an easy-to-read format.

9) If the data has not been updated in a while, it presents an alert to the user.

Thoughts for improvement:
conditional formatting of the table cells so it's easier to see which areas are doing well or not
calculating as % of population
show the peak number and date for each item.
