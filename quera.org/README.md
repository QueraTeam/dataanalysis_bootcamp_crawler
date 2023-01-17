# Quera Magnet Scraper
A web scraper to find all the offered jobs in [Quera Magnet](https://quera.org/magnet/jobs).

## Requirements
- Python 3.6+
- `beautifulsoup4`
- `requests`

## How it works?
The scraper uses `beautifulsoup` to parse the html of each page and extract the job information. It then saves the information in a `json` file.

## Output Format
The output is a `json` file with the following format:
```json
{
    "jobs": [
        {
            "title": "استخدام Senior Back-end Developer (Python)",
            "url": "https://quera.org//magnet/jobs/69rqj",
            "date": "۵ دی ۱۴۰۱،‏ ۹:۲۷",
            "company": "Raika Research",
            "location": "تهران",
            "level": "Senior",
            "type": "تمام وقت",
            "salary": "حقوق ۳۵,۰۰۰,۰۰۰ تا ۴۰,۰۰۰,۰۰۰",
            "remote": "امکان دورکاری",
            "technologies": ["Python", "Django"],
            "sub_technologies": ["Linux"]

        },
        {
            "title": "استخدام تحلیلگر داده",
            "url": "https://quera.org//magnet/jobs/6xqj",
            "date": "۱۸ آذر ۱۴۰۱،‏ ۲۰:۳۷",
            "company": "Quera",
            "location": "تهران",
            "level": "Junior",
            "type": "پروژه‌ای",
            "salary": "حقوق ۱۵,۰۰۰,۰۰۰ تا ۲۰,۰۰۰,۰۰۰",
            "remote": "امکان دورکاری",
            "technologies": ["Python", "Data Analysis"],
            "sub_technologies": ["SQL"]
        }
    ]
}
```
