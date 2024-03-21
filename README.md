# Weather Data

This repo was for experimenting with [Prefect](https://www.prefect.io/) as an orchestration tool for executing spark jobs with pyspark. The data is sourced from [Open Weather](https://openweathermap.org/) from their free plan. 

The data transformation is trivial, this experiment project was just to start building MLOps related applications focusing on ingestion and minimal data processing. I plan on incrementally building more substantive applications aiming towards more real world use cases.  


# Running locally

Sign up for a free account with Open Weather and retrieve the API key and set the value locally in a .env file in the repo with the name of "WEATHER_API_KEY" . 



```

## from project root

docker build -t weather-data-pyspark-prefect .

docker run weather-data-pyspark-prefect

```

The aggregated dataframe response will be written to console. 

