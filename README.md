# Opening hours
AWS Lambda/AWS API Gateway powered service, that converts restaurant working hours to human readable format

## Getting started

### Why AWS Lambda?

AWS Lambda is the event-driven serverless platform, provided by Amazon Web Services.
It allows running code without managing infrastructure.
[Details about AWS Lambda can be found here](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
AWS Lambda works fine for stateless apps without strict non-functional requirements for performance.
(So cold start is not an issue). It allows to concentrate on code, not system administration and helps to simplify software.

### Prerequisites

[Python3](https://www.python.org/downloads/) and [Virtualenv](https://virtualenv.pypa.io/en/stable/) are required to install and run this app
If you use python3 earlier than 3.4, make sure that [pip](https://pip.pypa.io/en/stable/installing/) is also installed

1. [Install aws-sam-cli to run AWS API Gateway and AWS Lambda locally](https://github.com/awslabs/aws-sam-cli/blob/develop/docs/installation.rst)

### Install

1. Clone this repo ```git clone git@github.com:andyudina/opening-hours-exercise.git```
2. Create python environment ```virtualenv env``` and activate it ```source ./env/bin/activate```
2. Install dependencies with pip ```pip3 install -r requirements.txt```

### Run tests

```python3 -m unittest discover tests```

### Run locally

1. Package code: ```python3 scripts/package.py build/opening_hours```
2. Start docker daemon for aws-sam-cli
3. Run app using aws-sam-cli ```sam local start-api```

Make sure that you have internet connection - needed to download docker image.

## Use app

Service accepts GET requests on one API Endpoint: */openinghours*

Query parameter "query" is required. The query is expected to be UTF-8 with BASE64 encoding.
So JSON with restaurant working hours should be base64 encoded and passed as GET parameter query.

**Successful response**
- Response code: 200 OK
- Response body:
```json
{ 
  "working_hours": {
    "type": "array",
    "items": {
      "type": "string",
      "description" : "Working hours for one day in human-readable format"
    }
  }
}
```

**If error occurred**
- Response code: 400 Bad request or 422 unprocessable entity
- Response body:
```json
{ 
  "error": "string", 
}
```

For example JSON request with opening hours:
```json
{  
   "monday":[  

   ],
   "tuesday":[  
      {  
         "type":"open",
         "value":36000
      },
      {  
         "type":"close",
         "value":64800
      }
   ],
   "wednesday":[  

   ],
   "thursday":[  
      {  
         "type":"open",
         "value":36000
      },
      {  
         "type":"close",
         "value":64800
      }
   ],
   "friday":[  
      {  
         "type":"open",
         "value":36000
      }
   ],
   "saturday":[  
      {  
         "type":"close",
         "value":3600
      },
      {  
         "type":"open",
         "value":36000
      }
   ],
   "sunday":[  
      {  
         "type":"close",
         "value":3600
      },
      {  
         "type":"open",
         "value":43200
      },
      {  
         "type":"close",
         "value":75600
      }
   ]
}
```
Should be passed in base64 format as:
/openinghours?query=eyJtb25kYXkiOiBbXSwgInR1ZXNkYXkiOiBbeyJ0eXBlIjogIm9wZW4iLCAidmFsdWUiOiAzNjAwMH0sIHsidHlwZSI6ICJjbG9zZSIsICJ2YWx1ZSI6IDY0ODAwfV0sICJ3ZWRuZXNkYXkiOiBbXSwgInRodXJzZGF5IjogW3sidHlwZSI6ICJvcGVuIiwgInZhbHVlIjogMzYwMDB9LCB7InR5cGUiOiAiY2xvc2UiLCAidmFsdWUiOiA2NDgwMH1dLCAiZnJpZGF5IjogW3sidHlwZSI6ICJvcGVuIiwgInZhbHVlIjogMzYwMDB9XSwgInNhdHVyZGF5IjogW3sidHlwZSI6ICJjbG9zZSIsICJ2YWx1ZSI6IDM2MDB9LCB7InR5cGUiOiAib3BlbiIsICJ2YWx1ZSI6IDM2MDAwfV0sICJzdW5kYXkiOiBbeyJ0eXBlIjogImNsb3NlIiwgInZhbHVlIjogMzYwMH0sIHsidHlwZSI6ICJvcGVuIiwgInZhbHVlIjogNDMyMDB9LCB7InR5cGUiOiAiY2xvc2UiLCAidmFsdWUiOiA3NTYwMH1dfQ==

And the response will be:
```json
{ 
  "working_hours": [
    "Monday: Closed",
    "Tuesday: 10 AM - 6 PM", 
    "Wednesday: Closed",
    "Thursday: 10 AM - 6 PM",
    "Friday: 10 AM - 1 AM",
    "Saturday: 10 AM - 1 AM",
    "Sunday: 12 PM - 9 PM"
  ]
}
