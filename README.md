# BioresourcesMarketInformationDashboard

## Bioresources market information

This is code for Ofwat's bioresources market information work. 

There are two key Python scripts: 

1. **Bioresources_market_information.py**: This is the main script to consolidate and format water companies' published bioresources market information. It is this script that generates the data that Ofwat uses to produce its [dashboard](https://www.ofwat.gov.uk/regulated-companies/markets/bioresources-market/bioresources-market-information/)

2. **Bioresources_market_info_functions.py**: This contains a number of bespoke functions. 

All of the outputs from the above scripts are saved in a SQL-lite database in an outputs folder