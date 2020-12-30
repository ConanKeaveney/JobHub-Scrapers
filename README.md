# Web Scraper Service

## Debugging

start debugger:

```
docker-compose run -p 5000:80 web-scraper python -m pdb run.py
```

set breakpoint:

```
import pdb; pdb.set_trace()
```

pdb commands:

- [Pdb](https://www.digitalocean.com/community/tutorials/how-to-use-the-python-debugger)

## Usage

All responses will have the form

```json
{
  "data": "Mixed type holding the content of the response",
  "message": "Description of what happened"
}
```

http://localhost:5000/api/scrapers/

### List all job postings

'GET /postings'

**Responses**

- '200 OK' on success

```json
{
  "message": "Success",
  "data": [
    {
      "sig": [
        {
          "title": "Options Sales Trader",
          "location": "Dublin, Ireland",
          "category": "Trading",
          "post date": "2018-09-06T09:30:15.760Z",
          "description": "The Options Sales desk is responsible for generating and handling orders from external counterparties.  Starting in 2015 our business has continued to grow and now we are looking for a new options sales...",
          "experience": "Experienced",
          "url": "https://careers.sig.com/job/SUSQA004Y1249"
        },
        {
          "title": "Quantitative Trader - 2020 Programme",
          "location": "Dublin, Ireland",
          "category": "Trading",
          "post date": "2019-09-03T19:31:00.348Z",
          "description": "Overview Are you someone who constantly strives to be the best? We are looking for top graduates with a mathematical mind-set who are ambitious, driven, and determined to succeed in a top-performing, ",
          "experience": "Recent Graduate/Student",
          "url": "https://careers.sig.com/job/SUSQA004Y4449"
        }
      ],
      "google": "more jobs"
    }
  ]
}
```

### Lookup specific company postings

'GET /postings/<identifier>'

**Responses**

- '404 Not Found' If the company does not exist in listings
- '200 OK' on success

```json
[
  {
    "identifier": "sig",
    "jobs": [
      {
        "title": "Software Engineer",
        "location": "Dublin",
        "category": "SWE",
        "post date": "01/02/2019",
        "job description": "A job description blah blah blah",
        "experience level": "Junior",
        "job post url": "https://careers.sig.com/job/SUSQA004Y1335/Software-Engineer"
      }
    ]
  }
]
```

### Run Scrapers(currently for testing purposes)

'POST /postings/

**Responses**

- '201 OK' on success

```json
{
  "message": "Jobs Added",
  "data": {
    "sig": [
      {
        "title": "Options Sales Trader",
        "location": "Dublin, Ireland",
        "category": "Trading",
        "post date": "2018-09-06T09:30:15.760Z",
        "description": "The Options Sales desk is responsible for generating and handling orders from external counterparties.  Starting in 2015 our business has continued to grow and now we are looking for a new options sales...",
        "experience": "Experienced",
        "url": "https://careers.sig.com/job/SUSQA004Y1249"
      },
      {
        "title": "Quantitative Trader - 2020 Programme",
        "location": "Dublin, Ireland",
        "category": "Trading",
        "post date": "2019-09-03T19:31:00.348Z",
        "description": "Overview Are you someone who constantly strives to be the best? We are looking for top graduates with a mathematical mind-set who are ambitious, driven, and determined to succeed in a top-performing, ",
        "experience": "Recent Graduate/Student",
        "url": "https://careers.sig.com/job/SUSQA004Y4449"
      },
      {
        "title": "Trading Internship (Offcyle) - 2020",
        "location": "Dublin, Ireland",
        "category": "Trading",
        "post date": "2019-09-03T19:31:00.348Z",
        "description": "Overview Our Trading Internship is the perfect opportunity for high performing students interested in a quantitative role within the financial markets. The internship provides a unique opportunity to ",
        "experience": "Recent Graduate/Student",
        "url": "https://careers.sig.com/job/SUSQA004Y4451"
      },
      {
        "title": "Trading Summer Internship - 2020",
        "location": "Dublin, Ireland",
        "category": "Trading",
        "post date": "2019-09-03T19:31:00.348Z",
        "description": "Overview Our Trading Summer Internship is the perfect opportunity for high performing students interested in a quantitative role within the financial markets. The internship provides a unique opportun",
        "experience": "Recent Graduate/Student",
        "url": "https://careers.sig.com/job/SUSQA004Y4450"
      }
    ],
    "google": "more jobs"
  }
}
```
