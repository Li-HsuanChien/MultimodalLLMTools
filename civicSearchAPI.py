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


parser = argparse.ArgumentParser()

parser.add_argument("keyword")   

args = parser.parse_args()


url = f"https://www.civicsearch.org/api/search?keywords={args.keyword}&search_radius=30"
response = requests.get(url)

data = response.json()          
results = data["results"]

rows = []

for result in results:

    year, month, day = result["date"].split("-")
    dateformatted = f"{month}/{day}/{year}"

    county, state = map(str.strip, result["location"].split(","))

    video_url = f"https://youtu.be/{result['vid_id']}"

    state_and_county = f"{county}, {state}"

    rows.append([
        video_url,
        state,
        county,
        dateformatted,
        state_and_county
    ])


with open("data.csv", "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)