This project will scrape Ossie Indoor Beach Volleyball website and save the ladder and roster to a NoSQL database.
The data can then be used for tracking team progress.
And for retrieving the Roster through a REST API. (allowing for programmatic access).

Intended Technologies
 - IBM Cloud Functions
 - IBM Cloudant DB

Files
volleyball_scraper.py - Classes for web scraping Ladders and Roster
compare_and_update.py - Compares current site with latest DB entry, and updates if different
database_queries.py - Queries the database and returns List of teams, Team history, Roster, Ladder
match_maker_auto.py - Roster contains abbreviated names. Makes best guess to match Roster team name with Ladder team names.
match_maker_manual.py - Roster contains abbreviated names. Makes best guess to match Roster team name with Ladder team names.


# OssieIndoorVolleyball_DataScraper
