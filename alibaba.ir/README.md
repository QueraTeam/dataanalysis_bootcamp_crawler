# About the Alibaba site:
    Alibaba site is one of the largest online travel ticket purchase sites,
    which includes international and domestic flight tickets, trains, hotels, tours, etc.
# Purpose:
    The purpose of building this project is to extract all this information and use it statistically,
    finally reaching the best options needed by the user for ordering.

# Site: 
    alibaba.ir

# how to use:
    go to the main file and write:

    ```python
    from tools.data import TOUR

    ```
    tour class has options for search and works on Firefox 

    ```python
    
    TOUR('firefox',
    origin = 'تهران',
    destination = 'کیش' ,
    departure_date = '2023-02-25',
    return_date = '2023-03-15',
    rooms = 1,
    persons = 1)
    ```
