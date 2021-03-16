# coding challenge
The `docker-compose` file defines three services.
* **postgres:** Postgres database accessible on port 5432
* **backend:** a FastAPI web service running on port 8000
* **import:** an import script that reads the file `GlobalLandTemperaturesByCity.csv` from the `./data` folder (mounted volume) and imports it to the Postgres database table `land_temperatures`

The choice of FastAPI was motivated by my own curiosity about the framework as well as the problem requirements. It was indicated, that the front- and backend would be rather separated, so a deep support for a templating system was not required. The fact that FastAPI autogenerates its documentation as Swagger specs makes it very interesting for teams working in multiple languages (swagger specs can be used for unit tests).

Worktime: ~8 hours

There is only a single endpoint `/city_land_temperatures` accepting
* `GET` for fetching multiple entries in a date range
* `POST` for creating a single new entry
* `PATCH` for updating a single entry

For a detailed documentation of the endpoints and the expected payloads start the service and check out the docs at http://0.0.0.0:8000/docs where test requests can be made as well.

## Disclaimer
This is a toy setup. There are a lot of features missing like:
* separate non superuser database user
* proper data modeling (city + date is not unique identifier)
* data migration setup
* ...



## How To Run this
The `Makefile` serves as an abstraction layer to make clearer how to setup and run the services.

### starting the database and backend
```
make setup
```
Now the documentation of the endpoints can be found at http://0.0.0.0:8000/docs.

### running the import
To run the import of the file [GlobalLandTemperaturesByCity.csv](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data?select=GlobalLandTemperaturesByCity.csv) place the csv file in the `./data` folder and run
```
make import
```

### clean up
To stop the services and remove the containers run
```
make teardown
```

## Examples

### a) entry whose city has the highest AverageTemperature since the year 2000

```
from datetime import date
import requests

url = "http://0.0.0.0:8000/city_land_temperatures"
params = {
    "date_from": "2000-01-01",
    "date_to": str(date.today()),
    "sort_order": "desc",
    "limit": 1
}
res = requests.get(url, params=params)
highest_since_2000 = res.json()[0]
```

### b) add new entry based on last response:

```
today = date.today()
previous_month = (today.month - 1) if (today.month - 1) else 12
previous_month_date = date.today().replace(month=previous_month, day=1)

average_temperature = highest_since_2000["average_temperature"] or 0
payload = {
    "date": str(previous_month_date),
    "city": highest_since_2000["city"],
    "country": highest_since_2000["country"],
    "average_temperature": average_temperature + 0.1,
    "average_temperature_uncertainty": highest_since_2000["average_temperature_uncertainty"],
    "latitude": highest_since_2000["latitude"],
    "longitude": highest_since_2000["longitude"]
}
res = requests.post(url, json=payload)
```

### c) update `average_temperature` from first response:

```
average_temperature = highest_since_2000["average_temperature"] or 0
payload = {
    "date": highest_since_2000["date"],
    "city": highest_since_2000["city"],
    "country": highest_since_2000["country"],
    "average_temperature": average_temperature - 2.5,
    "average_temperature_uncertainty": highest_since_2000["average_temperature_uncertainty"],
    "latitude": highest_since_2000["latitude"],
    "longitude": highest_since_2000["longitude"]
}

res = requests.patch(url, json=payload)
print(res.json())
```
