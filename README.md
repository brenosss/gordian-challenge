## Challenge

#### Seatmap Availability Exercise:

Write a python script that parses the example seatmap response (OTA_AirSeatMapRS.xml) and return a JSON object that lists the seats with the next properties:

	- Type (Seat, Kitchen, Bathroom, etc)
	- Seat id (17A, 18A)
	- Seat price
	- Cabin class
	- Availability

And any other properties you might find interesting or useful.

The output json format is not defined, so feel free to choose whatever you think best represents the information

## How to use:

#### required python3.8 

run:

> python3 airseatmap.py

 To see the options run

> python3 airseatmap.py -h

#### Output Format:

```json
[
    {
        "Layout": "AB EF",
        "Rows": [
            {
                "CabinType": "First",
                "Seats": [
                    {
                        "Summary": {
                            "AvailableInd": "false",
                            "SeatNumber": "1A"
                        }
                    },
                    {
                        "Summary": {
                            "AvailableInd": "false",
                            "SeatNumber": "1B"
                        }
                    },
		...
```
or to export in a flat format use:

> python3 airseatmap.py --flat

```json
    {
        "CabinType": "First",
        "Summary": {
            "AvailableInd": "false",
            "SeatNumber": "1A"
        }
    },
    {
        "CabinType": "First",
        "Summary": {
            "AvailableInd": "false",
            "SeatNumber": "1B"
        }
    },
    ...

```

#### Output File:


> python3 irseatmap.py --output-file test.json

#### Or print the result:

> python airseatmap.py --print

#### Extra fields:

- Pass a list of extra fields to be extract like ColumnNumber, ExitRowInd, PlaneSection, Status

> python airseatmap.py --extra-fields BulkheadInd Features

#### Or use "full" to extract all fields

> python airseatmap.py --full
