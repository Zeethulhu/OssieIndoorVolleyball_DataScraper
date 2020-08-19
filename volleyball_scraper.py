import bs4
import hashlib
import re
import requests
from datetime import datetime


# TODO: Add method to save to Cloudant
# TODO: Add method to diff compare html
# TODO: Remove the dynamic content from html scrap (eg. "We have X guests online") DONE
# TODO: Write tests in pytest


class VolleyballLadder:
    """
    Scrapes Volleyball website and returns the output in
    various formats.


    Properties
     - Competition name. Breadcrumb. Name eg. Monday Mens
     - Page hash
     - Date Scraped
     - Line diffs
     - List of Divisions
       - Division list contains list of teams and score
     - Headline
     - GameDay
     - Results for Week X of 52
    """

    def __init__(self, url):
        self.url = url
        self.html = self.get()
        self.headline = self.saveHeadline()
        self.competition_name = self.saveCompName()
        self.scrape_time = self.saveScrapeDate()
        self.gameday = self.saveGameDay()
        self.html_hash = self.saveHash()
        self.ladder = self.saveLadder()
        self._id = self.gen_id()

    def get(self):
        """ Gets the HTML of the Volleyball ladder web page """
        res = requests.get(self.url)

        # Testing for 404 or bad connection
        res.raise_for_status()

        # Removing dynamic content. Which is the "We have X guests online"
        # This allows reliable Hash check for updates to site.
        mySoup = bs4.BeautifulSoup(res.text, "lxml")
        mySoup.find("div", string=re.compile(r"(.*) We have(.*)\d{1,3} guests(.*)online")).decompose()

        return str(mySoup)

    def gen_id(self):
        dateTimeObj = datetime.now()
        time_str = dateTimeObj.strftime("%Y%m%d%H%M%S%s")
        #TODO: Finish this func. Add milliseconds

        return "ladder:" + time_str


    def saveHash(self):
        """ return hash for the HTML text. Compared with future scrapes to
        idetify changes and updates to the site """

        return hashlib.sha224(self.html.encode("utf-8")).hexdigest()

    def saveCompName(self):
        """ Gets the competition name. Which usually contain day of the week.
        Eg. 'Monday Mens', 'Wednesday Mixed', 'Wednesday 2 A Side' """

        mySoup = bs4.BeautifulSoup(self.html, "html.parser")
        comp_name = mySoup.find(
            "span",
            class_="box-3",
            string=re.compile("monday|tuesday|wednesday|thursday", re.IGNORECASE),
        )

        return comp_name.string

    def saveScrapeDate(self):
        """ Records a date time string for when data was scraped """

        dateTimeObj = datetime.now()
        return dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")

    def savePageDiffs(self):
        #TODO
        pass

    def saveLadder(self):
        """ Returns list of dictionaries. Each list item is a division. Each
        division contains dict items for each team with team name, score, rank
        """

        def getDivisions(html_text):
            """ Returns a list of Divisions found in HTML """

            mySoup = bs4.BeautifulSoup(html_text, "html.parser")

            strong_text = mySoup.findAll("strong")

            div_group = []

            for x in strong_text:
                matched = re.search(r"div(.*)$", x.text, re.IGNORECASE)
                if matched:
                    div_group.append(matched.group(0))

            return div_group

        def getLadders(html_text):

            mySoup = bs4.BeautifulSoup(html_text, "html.parser")
            tables = mySoup.findAll("table")

            results = []

            for table in tables:
                keys = ("Rank", "TeamName", "Score")

                rows = table.find_all("tr")

                table_results = []

                for row in rows:
                    vals = [i.text.strip() for i in row.find_all("td")]
                    table_results.append(dict(zip(keys, vals)))

                table_results_trim = [i for i in table_results if i.get("TeamName") != ""]

                results.append(table_results_trim)

            return results

        divisions = getDivisions(self.html)
        ladders = getLadders(self.html)

        divisions_ladders = []

        for division, ladder in zip(divisions, ladders):
            ladder_collection = {}
            ladder_collection[division] = ladder

            divisions_ladders.append(ladder_collection)

        return divisions_ladders

    def saveHeadline(self):
        """ Gets the healine test which often contains news, announcements,
        and the date the games the ladder applies to """

        soup = bs4.BeautifulSoup(self.html, "html.parser")
        heading = (str(soup.find(class_="headline").text).replace("\n", " ")).strip(
            " \t\n\r"
        )
        return str(heading)

    def saveGameDay(self):
        """ Records the day of the week the games are played on """

        mySoup = bs4.BeautifulSoup(self.html, "lxml")

        title = mySoup.find("title").string

        match = re.search(
            "monday|tuesday|wednesday|thursday|friday", title, re.IGNORECASE
        )
        return match.group()


class VolleyballRoster:
    """
    Scrapes Volleyball website and returns the output in
    various formats.

    Properties
     - Page hash
     - Date Scraped
     - Line diffs
     - List of Roster times (eg. 6:45pm, 7:30pm)
       - Roster list contains list of teams and opponent
     - Headline
     - GameDay
    """

    def __init__(self, url):
        self.url = url
        self.html = self.get()
        self.headline = self.saveHeadline()
        self.scrape_time = self.saveScrapeDate()
        self.gameday = self.saveGameDay()
        self.html_hash = self.saveHash()
        self.roster = self.saveRoster()
        self._id = self.gen_id()


    def get(self):
        """ Gets the HTML of the Volleyball ladder web page """
        res = requests.get(self.url)

        # Testing for 404 or bad connection
        res.raise_for_status()

        # Removing dynamic content. Which is the "We have X guests online"
        # This allows reliable Hash check for updates to site.
        mySoup = bs4.BeautifulSoup(res.text, "lxml")
        mySoup.find("div", string=re.compile(r"(.*) We have(.*)\d{1,3} guests(.*)online")).decompose()

        return str(mySoup)


    def gen_id(self):
        dateTimeObj = datetime.now()
        time_str = dateTimeObj.strftime("%Y%m%d%H%M%S%L")

        return "roster:" + time_str


    def saveHash(self):
        """ return hash for the HTML text. Compared with future scrapes to
        idetify changes and updates to the site """

        return hashlib.sha224(self.html.encode("utf-8")).hexdigest()


    def saveHeadline(self):
        """ Gets the healine test which often contains news, announcements,
        and the date the games the ladder applies to """

        soup = bs4.BeautifulSoup(self.html, "html.parser")
        heading = (str(soup.find(class_="headline").text).replace("\n", " ")).strip(
            " \t\n\r"
        )
        return str(heading)

    def saveGameDay(self):
        """ Records the day of the week the games are played on """

        mySoup = bs4.BeautifulSoup(self.html, "lxml")

        title = mySoup.find("title").string

        match = re.search(
            "monday|tuesday|wednesday|thursday|friday", title, re.IGNORECASE
        )
        return match.group()


    def saveScrapeDate(self):
        """ Records a date time string for when data was scraped """

        dateTimeObj = datetime.now()
        return dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")


    def savePageDiffs(self):
        #TODO
        pass


    def saveRoster(self):

        def trimTableJunk(html_text):
            ''' Removing undesirable tables and HTML. This includes a 'VS' column
            in the HTML table with the data we want '''

            mySoup = bs4.BeautifulSoup(html_text, "html.parser")

            timetables = mySoup.find(class_="article")

            while timetables.find("td", rowspan="9"):
                timetables.find("td", rowspan="9").decompose()

            return str(timetables)

        def getTimes(html_text):
            mySoup = bs4.BeautifulSoup(html_text, "html.parser")

            def is_strong_time(tag):
                test1 = (tag.name == 'strong') or (tag.name == 'b')

                if tag.string is None:
                    regex_test = False
                else:
                    regex_test = re.search(r'\d{1,2}[\.\:]\d{2}|\dpm', tag.string)

                return test1 and regex_test

            return [time.string for time in mySoup.find_all(is_strong_time)]
            #return article_class.find_all(is_strong_time)

        def getRosters(html_text):
            mySoup = bs4.BeautifulSoup(html_text, "html.parser")
            tables = mySoup.findAll("table")
            results = []

            def test_unwanted_values(table_value):
                '''returns true if unwanted value'''
                return (table_value.get("Team-A") == "") or \
                       (table_value.get("Team-B") == "") or \
                       (table_value.get("Team-A") == "Team A") or \
                       (table_value.get("Team-B") == "Team B")

            for table in tables:
                keys = ("Team-A", "Team-B")
                rows = table.find_all("tr")
                table_results = []
                for row in rows:
                    vals = [i.text.strip() for i in row.find_all("td")]
                    table_results.append(dict(zip(keys, vals)))

                table_results_trim = [i for i in table_results if not test_unwanted_values(i)]
                results.append(table_results_trim)
            return results

        cleaned_html = trimTableJunk(self.html)

        roster_times = getTimes(cleaned_html)
        roster_games = getRosters(cleaned_html)

        rosters = []

        for time_slot, games in zip(roster_times, roster_games):
            roster_collection = {}
            roster_collection[time_slot] = games

            rosters.append(roster_collection)

        return rosters

if __name__ == "__main__":

    import pprint

    pp = pprint.PrettyPrinter(indent=4)

    MondayLadder = VolleyballLadder(
        url="http://ossieindoorbeachvolleyball.com.au/monday-mens"
    )

    print(MondayLadder.url)
    # print(MondayLadder.html)
    print(MondayLadder.headline)
    print(MondayLadder.gameday)
    print(MondayLadder.competition_name)
    print(MondayLadder.scrape_time)
    print(MondayLadder.html_hash)
    print(MondayLadder.ladder)


    pp.pprint(MondayLadder.__dict__)


    mondayroster = VolleyballRoster(
        url="http://ossieindoorbeachvolleyball.com.au/monday"
    )

    print(mondayroster.url)
    # print(MondayLadder.html)
    print(mondayroster.headline)
    print(mondayroster.gameday)
    print(mondayroster.scrape_time)
    print(mondayroster.html_hash)
    print(mondayroster.roster)

    pp.pprint(mondayroster.__dict__)
