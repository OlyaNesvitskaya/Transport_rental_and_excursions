# Transport_rental_and_excursions
The project consists of two independent applications.
One of them is the REST API, which implements business logic on top of the DBMS. Other provides an
interface for web users, which allows users to record information about services, clients and orders.

  # Quick Start
### Clone the repo:
* $ git clone https://github.com/OlyaNesvitskaya/transport_rental_and_excursions.git
* $ cd transport_rental_and_excursion/


### Run the project:
* docker-compose build
* docker-compose up


Navigate to http://localhost:5000/api/clients to see page of all clients through API  
Navigate to https://localhost:5009/my_app/clients to see page of all clients through APP

### Run tests in api container:
* docker exec -it <*CONTAINER ID*> /bin/bash
* python -m pytest

# Application Structure:

### Client Application

The ```App``` is served using a Flask blueprint at **/my_app/**

### Rest Api

The ```Api``` is served using a Flask blueprint at  **/api/** using Flask Restful class-based resource routing. 


| HTTP Method      | endpoints               | Action                                                     |
|------------------|-------------------------|------------------------------------------------------------|
| GET, POST        | /clients                | show all clients or create client                          |
| GET              | /clients_filtering      | show all clients about indicated date                      |
| GET, PUT, DELETE | /client/<client_id>     | retrieve( or update or delete) client about indicated id   |
| GET, POST        | /services               | show all services or create service                        |
| GET              | /services_filtering     | show all services about indicated date                     |   
| GET, PUT, DELETE | /service/<service_id>   | retrieve( or update or delete) service about indicated id  |
| GET, POST        | /orders                 | show all orders or create order                            |
| GET              | /orders_filtering       | show all orders about indicated date                       |  
| GET, PUT, DELETE | /order/<order_id>       | retrieve( or update or delete) order about indicated id    |

+ Example creating new client:
```
{
    "name": "Elena",
    "phone_number": "1537411724",
    "email": "ntraviss2@umn.edu"
}
```
+ Example creating new service:  
```
{
    "name": "Trip to blue lakes",
    "description": "very cool!!!!!!",
    "unit": "person",
    "price": 250
}
```
+ Example creating new order:  
```
{
    "client_id": 1,
    "services": [
        {
            "service_id": 1,
            "quantity": 10,
            "event_date": "2023-07-7"
        }
    ]
}
```