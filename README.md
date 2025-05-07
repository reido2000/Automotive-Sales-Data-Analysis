# Judul Project
`Automotive Sales Data Analysis`
## Repository Outline
`This project has 10 files.`

```
1. README.md - Overview of the project
2. P2M3_Reido_conceptual.ipynb - Notebook containing data processing with Python
3. P2M3_Reido_DAG - File to run the automation flow.
4. P2M3_Reido_DAG_Graph - Photo of the DAG Graph result
5. P2M3_Reido_DAG_Grid - Photo of the DAG Grid result
6. P2M3_Reido_data_clean - Cleaned dataset.
7. P2M3_Reido_data_raw - Dataset used.
8. P2M3_Reido_DDL - File containing SQL syntax to create tables in Postgres
9. P2M3_Reido_GX - Notebook containing data validation using Great Expectations.
```

## Problem Background
`The automotive industry is facing intense competition, therefore analysis is needed to understand consumer behavior and determine effective sales strategies.`

## Project Output
`The output of this project is a compelling visualization of the analysis results, rendered with the sophisticated capabilities of Kibana.`

## Data
`The data used in this project came from Kaggle. It has 16 columns and 5,000 rows`
```
Car_id - Unique identifier for each car in the dataset. 
Date - Date of the car sale transaction.
Customer Name - Name of the customer purchasing the car.
Gender - Gender of the customer
Annual Income - Annual income of the customer.
Dealer_Name - Name of the car dealer associated with the sale.
Company - Company or brand of the car.
Model - Model name of the car.
Engine - Specifications of the car's engine.
Transmission - Type of transmission in the car.
Color - Color of the car's exterior.
Price ($) - Listed price of the car for sale.
Dealer_No - Dealer identification number associated with the sale.
Body Style - Style or design of the car's body.
Phone - Contact phone number associated with the car sale
Dealer_Region - Geographic region or location of the car dealer.
```

## Method
`The methodology employed in this project leverages the robust automation capabilities of Airflow to orchestrate the analytical pipeline, culminating in insightful visualizations presented through the powerful data exploration platform, Kibana`

## Stacks
`This project uses the Python programming language with the following libraries`

```
1. pandas - used for reading the Kaggle dataset and cleaning.
2. numpy - used for numerical computing.
3. re - used for cleaning or transforming text data.
4. datetime - used when dataset contains date or time information.
5. airflow - used to automate data pipeline.
6. PostgresHook - used to interact with a PostgreSQL database.
7. Elasticsearch, helpers - Connect to Elasticsearch.
```

## Reference
`URL Dataset Raw : https://www.kaggle.com/datasets/missionjee/car-sales-report`
