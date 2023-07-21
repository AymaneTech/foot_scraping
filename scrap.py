import requests
from bs4 import BeautifulSoup
import csv

match_date = input("Please enter a date in the following format MM/DD/YYYY: ")
page = requests.get(f"https://www.yallakora.com/Match-center/?date={match_date}")


def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []
    matches_details_lyaad = []
    matches_details_volley = []

    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(championship):
        championship_title = championship.find("h2").text.strip()
        all_matches = championship.find_all("li")
        numbers_of_matches = len(all_matches)

        for i in range(numbers_of_matches):
            # GET TEAMS NAMES
            team_A = all_matches[i].find("div", {"class": "teamA"}).text.strip()
            team_B = all_matches[i].find("div", {"class": "teamB"}).text.strip()

            # GET SCORE
            match_result = (
                all_matches[i]
                .find("div", {"class": "MResult"})
                .find_all("span", {"class": "score"})
            )
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            # GET MATCH TIME
            match_time = (
                all_matches[i]
                .find("div", {"class": "MResult"})
                .find("span", {"class": "time"})
                .text.strip()
            )

            # ADD MATCH INFO TO matches_details
            if " لكرة اليد" in championship_title:
                matches_details_lyaad.append(
                    {
                        "Championship Type": championship_title,
                        "First Team": team_A,
                        "Second Team": team_B,
                        "Match Time": match_time,
                        "Score": score,
                    }
                )
            if " للكرة الطائرة" in championship_title:
                matches_details_volley.append(
                    {
                        "Championship Type": championship_title,
                        "First Team": team_A,
                        "Second Team": team_B,
                        "Match Time": match_time,
                        "Score": score,
                    }
                )
            else:
                matches_details.append(
                    {
                        "Championship Type": championship_title,
                        "First Team": team_A,
                        "Second Team": team_B,
                        "Match Time": match_time,
                        "Score": score,
                    }
                )

    for championship in championships:
        get_match_info(championship)

    keys = matches_details[0].keys()
    if len(matches_details_lyaad) > 0:
        with open(
            r"C:\Users\aymane\OneDrive\Bureau\YallaKorraScraping\matches-lisr.csv",
            "w",
            newline="",
            encoding="utf-8",
        ) as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details_lyaad)

        print("File Kooorat lyaad created.")
    if len(matches_details_volley) > 0:
        with open(
            r"C:\Users\aymane\OneDrive\Bureau\YallaKorraScraping\matches-volley.csv",
            "w",
            newline="",
            encoding="utf-8",
        ) as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details_volley)

        print("File Kooorat volleycreated.")
    if len(matches_details) > 0:
        with open(
            r"C:\Users\aymane\OneDrive\Bureau\YallaKorraScraping\matches-foot.csv",
            "w",
            newline="",
            encoding="utf-8",
        ) as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(matches_details)

        print("File football created.")


main(page)
