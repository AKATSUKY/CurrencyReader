# CurrencyReader
This code is an small Python API Consumer that every day reads the currencies value from CurrencyLayer, and stores it into my AWS MariaDB Database.

It also demonstrates the results with a plot made in R, this Plot is an Line Chart with a few options for the user to filter and best view the data.

The Python API Consumer also is able to receive a parameter to load historical values. It reads all the currencies in the last 180 days. 

Results in http://santiagocloud.com