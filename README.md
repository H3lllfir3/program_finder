# Program Finder
# Program Finder

## Web scrapper
 - scrap company name
 - create url on that platform
 - find in scope domain

## Data handler
 - check company name wheather exist to db or not (if not exist add it to db and notify through discord)
 - check company program beacause some company have many programs if not add it to db
 - check in scope if data was vary update it.
 - each time to add data to db
   1. sort data 
   2. create json pattern {'hackerone': {'dell': {'product1': 'URL', 'product1', 'url'}, 'apple'}
                           'intigrity': }

## Logger
 - log and notify every time program runs
 - log each program seperetly
 - log main link wheather the status code is 200 or not
 - log each level data extraction like [0]['companyHandler']

## Notify 
 - Notify every time program run
 - Notify if new programm add

------------------------------
 # flow
 1 - request to the endpoint
 2 - get the all programs
 3 - check the all program of each platform on db with new data
 4 - check for insert, update, delete
 5 - log each process
 6 - notify each process

---------------------------
# Todo:
check data field by field



 # Automation 
 -------------------------
 # programfinder
 # subdomain discoveri
 # portscanning
 # parameter finder
 # path finder
 # content finder