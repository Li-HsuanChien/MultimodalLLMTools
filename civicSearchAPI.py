"""
civic search own api: https://www.civicsearch.org/api/search?keywords=AI&search_radius=30
Response format:
 ```json
    {
        location_counts: [
            [
                [
                    "(Countyname-statename)", 
                    "(county Name, STATECODE)"
                ], 
                (entries count)
            ], 
                ...
        ],
        matched_meeting_counts:	{ 
            "(month_YYYY-MM)": (Meeting counts)
        },
        meeting_counts:	{ 
            "(past month_YYYY-MM)": (count), 
            ..., 
            (state_Statename): (count),
            ...
        },
        num_places:	(place count),
        num_results: (meeting transcript count),
        num_snippets: (word match count),
        places:	[],
        points_of_interest:	[],
        related_keywords:	[],
        results:[
            {
            date:"(YYYY-MM-DD)",
            distance: 0,
            has_approximate_timings: (bool)
            location: "(county Name, STATECODE)",
            location_query_id: "(Countyname-statename)",
            snippets:
                [
                    { text: "(snippet text)", topic_id: (topic id), timestamp: (timestamp in seconds) },
                    ...
                ],
            title:	"(Video Title)"
            vid_id:	"(Video ID)"
            viewCount:	(view count)
                
            }, 
            ...
        ],
        summary: "",
        topic_counts: []
    }
 
 ```
 
Sample response(truncated):

```json
{
        location_counts: [
            [
                [
                    "norwalk-connecticut", 
                    "Norwalk, CT"
                ], 
                4
            ], 
            ...
        ],
        matched_meeting_counts:	{ 
            "month_2026-02": 102
        },
        meeting_counts:	{ 
            "month_2024-11": 1967,
            ... 
            "state_Massachusetts": 2705,
            ...
        },
        num_places:	626,
        num_results: 102,
        num_snippets: 974,
        places:	[],
        points_of_interest:	[],
        related_keywords:	[],
        results:[
            {
            date:"2026-02-18",
            distance: 0,
            has_approximate_timings: false
            location: "Beaufort County, SC",
            location_query_id: "beaufort-south-carolina",
            snippets:
                [
                    { text: "", topic_id: -1, timestamp: 2331.0 },
                    ...
                ],
            title:	"CONVERGE 2026 Lowcountry Economic Development Summit - February 18, 2026"
            vid_id:	"Cd_hDIROV7U"
            viewCount:	101
                
            }, 
            ...
        ],
        summary: "",
        topic_counts: []
    }

```
    

"""

import requests
import csv
import argparse
import os

from datetime import date

def fetch_and_parse(url, existing_ids, rows_to_append):

    response = requests.get(url)

    if response.status_code != 200:

        print(f"Request failed: {url}")
        return


    data = response.json()

    results = data.get("results", [])


    for result in results:

        vid_id = result["vid_id"]

        if vid_id in existing_ids:
            continue


        year, month, day = result["date"].split("-")

        dateformatted = f"{month}/{day}/{year}"


        county, state = map(str.strip, result["location"].split(","))


        video_url = f"https://youtu.be/{vid_id}"

        state_and_county = f"{county}, {state}"


        rows_to_append.append([
            video_url,
            state,
            county,
            dateformatted,
            state_and_county
        ])


        existing_ids.add(vid_id)

def process_keyword(keyword, csv_file):

    existing_ids = set()


    if os.path.exists(csv_file):

        with open(csv_file, newline="", encoding="utf-8") as f:

            reader = csv.reader(f)

            for row in reader:

                vid_id = row[0].split("/")[-1]

                existing_ids.add(vid_id)
    else:
        print(f"Error: {csv_file} not found, Terminating")
        exit()


    rows_to_append = []


    currentyear = date.today().year
    currentmonth = date.today().month


    for year in range(2024, currentyear + 1):

        if year == currentyear:
            months = range(1, currentmonth + 1)
        else:
            months = range(1, 13)

        for month in months:
            originalmonthcount = len(rows_to_append)
            url = (
                f"https://www.civicsearch.org/api/search?"
                f"keywords={keyword}"
                f"&start_date={year}-{month:02d}-01"
                f"&end_date={year}-{month:02d}-31"
            )


            print(f"fetching for {keyword} during {year}-{month:02d}")


            fetch_and_parse(
                url,
                existing_ids,
                rows_to_append
            )
            if len(rows_to_append) - originalmonthcount == 0:
                print(f"No new entries for {keyword} during {year}-{month:02d}\n")
            else:
                print(f"fetched {len(rows_to_append) - originalmonthcount} new (not in outputfile) rows for {keyword} during {year}-{month:02d}\n")


    with open(csv_file, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerows(rows_to_append)


    print(f"{keyword}: {len(rows_to_append)} rows added for keyword {keyword}\n")

    return len(rows_to_append)


def load_keywords(filepath):

    keywords = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:

                keyword = line.strip()

                if keyword:  

                    keywords.append(keyword) 
            return keywords
    else:

        print(f"Error: {filepath} not found, Terminating")
        exit()
    



def process_keywords(keyword_list, csv_file):
    counter = 0

    for keyword in keyword_list:
        counter += process_keyword(keyword, csv_file)


    print(f"A total of {counter} rows added, program stopping")
    
def main():

    parser = argparse.ArgumentParser()


    group = parser.add_mutually_exclusive_group(required=True)


    group.add_argument(
        "--keywords",
        nargs="+",
        help="Keywords provided directly"
    )


    group.add_argument(
        "--keywordfilepath",
        help="Path to txt file containing keywords"
    )


    parser.add_argument(
        "--outputpath",
        required=True,
        help="CSV output path"
    )


    args = parser.parse_args()


    if args.keywords:
        if args.keywordfilepath:
            print("error: argument --keywordfilepath: not allowed with argument --keywords, using keywords only")
        keyword_list = args.keywords
    else:
        keyword_list = load_keywords(
            args.keywordfilepath
        )


    print(f"{len(keyword_list)} keywords loaded")


    process_keywords(
        keyword_list,
        args.outputpath
    )


if __name__ == "__main__":

    main()