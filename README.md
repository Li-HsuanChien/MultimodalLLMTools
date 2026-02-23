<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

* Python 3.8+
* CivicSearch API access
* `requirements.txt` installed

---

### Installation

1. Create python virtual environment

```sh
python -m venv venv
```

2. Activate virtual environment

**Windows**

```sh
venv\Scripts\activate
```

**Mac / Linux**

```sh
source venv/bin/activate
```

3. Install script requirements

```sh
pip install -r requirements.txt
```

---

### Usage

You can run the script using **either direct keywords** OR a **keyword file**.

---

### Option 1 — Direct Keywords

Provide one or more keywords directly:

```sh
python civicSearchAPI.py --keywords AI housing tax --datapath data.csv
```

Example:

```sh
python civicSearchAPI.py --keywords AI budget climate --datapath output.csv
```

---

### Option 2 — Keyword File

Provide a `.txt` file containing keywords (one per line):

Example `keywords.txt`:

```txt
AI
housing
budget
climate change
tax
```

Run:

```sh
python civicSearchAPI.py --keywordfilepath keywords.txt --outputpath data.csv
```

---

### Output

The script will append results to the specified CSV file:

```txt
data.csv
```

Each row contains:

```txt
youtube_url, state, county, date, full_location
```

---

### Notes

* You must provide **either** `--keywords` **or** `--keywordfilepath`
* You cannot use both at the same time
* Existing videos in the CSV will not be duplicated

---

<p align="right">(<a href="#readme-top">back to top</a>)</p>
