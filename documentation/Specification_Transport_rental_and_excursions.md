# Transport rental and excursions

**Vision**

&nbsp;&nbsp;&nbsp;&nbsp;"Transport rental and excursions" is web-application which allows users to record information about sevices, clients
and orders.

_Application should provide:_
* Storing services, clients and orders in a database;
* Display list of services;
* Updating the list of services (adding, editing, removing);
* Display list of clients;
* Updating the list of clients (adding, editing, removing);
* Display list of orders;
* Updating the list of orders (adding, editing, removing);
* Display number of the orders for clients and services;
* Filtering by date for orders and clients;
* Filtering by price for services.

**1. Orders**

**1.1 Display list of orders**

The mode is designed to view the orders list and if it's possible to display the number of orders for a specified
period of time.

_**Main scenario**_:

* User selects item “Orders”;
* Application displays list of Orders.

![Orders_list.jpg](static%2FOrders_list.jpg)

Pic. 1.1 View the Orders list.  

The list displays the following columns:  

* Order number – unique order number;
* Order date – date of adding order;
* Client name – unique client name;
* Total price – total price of order. The total price is calculated as the sum of each services in the order;
* Actions – possibility edit or delete order.


_**Filtering by order_date:**_

* In the order list view mode, the user sets a date filter and presses the refresh list button (to the
right of the date entry field);
* The application will display a form to view the list of orders according to the indicated date. 

**_Restrictions:_**

* Start date of the period should be less than end date of the period;
* If start date is blank, then filtering by end date only.
* If end date is blank, then filtering by start date only.
* Updating data after selecting the filtering conditions is carried out by pressing the “Refresh” button.

**1.2 Add order**  

_**Main scenario:**_

* User clicks the “Add” button in the orders list view mode;
* Application displays form to enter order data;
* User enters order data and presses “Save” button;
* If any data is entered incorrectly, error messages is displaying;
* If entered data is valid, then record is adding to database;
* If new order record is successfully added, then list of orders with added records is displaying.

_**Cancel operation scenario:**_

* User clicks the “Add” button in the order list view mode;
* Application displays form to enter order data;
* User enters order data and presses “Cancel” button;
* Data don’t save in database, then list of orders records displays to user.
* If the user selects the menu item "Orders”, ”Clients” or "Services", the data will not be saved to the
database.

![Add_order.jpg](static%2FAdd_order.jpg)

Pic. 1.2 Add order.

`+` This button allows to add new string to enter data.  
`x` This button allows to remove corresponding string.

_Field is filled automatically:_  

* Date - date of adding order;
* Price – price for unit of service.
* Unit - unit of service, for example, for rent - hour, for excursion - price per person.  

When adding a order, the following details are entered:

* Client – client’s phone number;
* Goods – service's name;
* Number – number of units of ordered service;
* Total price - total services price. For every service in order total price is calculated as the number multiplied by price.
* Event date - date of providing service.

_Aggregate function:_ Total price = Number * Price.

_Constraints for data validation:_  

* Number – number, minimum=1;
* Event date – date in format yyyy-mm-dd should be greater than or equal to current date.


**1.3 Edit order**  

_**Main scenario:**_

* User clicks the “Edit” button in the orders list view mode;
* Application displays form to enter order data;
* User enters order data and presses “Save” button;
* If any data is entered incorrectly, incorrect data messages are displayed;
* If entered data is valid, then edited data is added to database;
* If order record is successfully edited, then list of orders with changed record is displaying.

_**Cancel operation scenario:**_

* User clicks the “Edit” button in the order list view mode;
* Application displays form to enter order data;
* User enters order data and presses “Cancel” button;
* Data don’t save in database, then list of orders records displays to user.
* If the user selects the menu item "Orders”, ”Clients” or "Services", the data will not be saved to the
database and the corresponding form with updated data will be opened.

![Edit_order.jpg](static%2FEdit_order.jpg)

Pic. 1.2 Edit order.

**1.4 Removing the order**  

_**Main scenario:**_

* The user, while in the list of orders, presses the "Delete" button in the selected order;
* If the order can be removed, a confirmation dialog is displayed;
* The user confirms the removal of the order;
* Record is deleted from database;
* If error occurs, then error message displays;
* If order record is successfully deleted, then list of orders without deleted records is displaying.

 ![Delete_order.jpg](static%2FDelete_order.jpg)

Pic. 1.4 Delete order dialog.

_**Cancel operation scenario:**_

* User is in display mode of orders list and press “Delete” button;
* Application displays confirmation dialog “Please confirm delete order?”;
* User press “Cancel” button;
* List of orders without changes is displaying. 


**2. Clients**

**2.1 Display list of Clients**

The mode is designed to view the clients list and if it's possible to display the number of clients for a specified
period of time.

_**Main scenario:**_

* User selects item “Clients”;
* Application displays list of clients.

![clients_list.jpg](static%2Fclients_list.jpg)

Pic 2.1 View the clients list.

The list displays the following columns:

* Number – unique client number;
* Name – client’s name;
* Date – client’s date registration;
* Phone_number – client’s phone number;
* Number of orders - client’s number of orders.

_**Filtering by date:**_

* In the clients list view mode, the user sets a date filter and presses the refresh list button (to the
right of the date entry field);
* The application will display a form to view the list of orders with updated data. 

**_Restrictions:_**

* Start date of the period should be less than end date of the period;
* If start date is blank, then filtering by end date only.
* If end date is blank, then filtering by start date only.
* Updating data after selecting the filtering conditions is carried out by pressing the “Refresh” button.

**2.2 Add client**

_**Main scenario:**_

* User clicks the “Add” button in the clients list view mode;
* Application displays form to enter client data;
* User enters client’s data and presses “Save” button;
* If any data is entered incorrectly, error messages is displaying;
* If entered data is valid, then record adds to database;
* If new client record is successfully added, then list of clients with added records is displaying.

_**Cancel operation scenario:**_

* User clicks the “Add” button in the clients list view mode;
* Application displays form to enter client’s data;
* User enters client’s data and presses “Cancel” button;
* Data don’t save in database, then list of clients records is displaying to user.
* If the user selects the menu item "Orders”, ”Clients” or "Services", the data will not be saved to the
database.

![Add_client.jpg](static%2FAdd_client.jpg)

Pic. 2.2 Add client.

When adding a client, the following details are entered:

* Name – client’s name;
* Phone_number – client’s phone number;
* Email – client’s email.

_**Constraints for data validation:**_

* Name – maximum length of 100 characters;
* Phone_number – unique, consist 12 digits in format XXXXXXXXXX;
* Email – maximum length of 40 characters.

**2.2 Edit client**

_**Main scenario:**_

* User clicks the “Edit” button in the clients list view mode;
* Application displays form to enter client data;
* User enters client’s data and presses “Save” button;
* If any data is entered incorrectly, error messages is displaying;
* If entered data is valid, then edited data adds to database;
* If new client record is successfully edited, then list of clients with changed record is displaying.

_**Cancel operation scenario:**_

* User clicks the “Edit” button in the clients list view mode;
* Application displays form to enter clients data;
* User enters clients data and presses “Cancel” button;
* Data don’t save in database, then list of clients records is displaying to user.
* If the user selects the menu item "Orders”, ”Clients” or "Services", the data will not be saved to the
database.

![Edit_client.jpg](static%2FEdit_client.jpg)

Pic. 2.2 Edit client.

**2.4 Removing client**

_**Main scenario:**_

* The user, while in the list of clients mode, presses the "Delete" button in the selected client line;
* Application displays confirmation dialog “Please confirm delete client?”;
* The user confirms the removal of the client;
* Record is deleted from database;
* If error occurs, then error message displays;
* If client record is successfully deleted, then list of clients without deleted record is displaying.
* 
![Delete_client.jpg](static%2FDelete_client.jpg)

Pic. 2.4 Delete client dialog.

_**Cancel operation scenario:**_

* User is in display mode of clients list and press “Delete” button;
* Application displays confirmation dialog “Please confirm delete client?”;
* User press “Cancel” button;
* List of clients without changes is displaying.

**3. Services**

**3.1 Display list of services**

The mode is designed to view the services list and if it's possible to display the number of services with a specified
prices.

**_Main scenario:_**

* User selects item “Services”;
* Application displays list of services.

![services_list.jpg](static%2Fservices_list.jpg)

Pic. 3.1 View the services list.

The list displays the following columns:

* Number – unique service's number;
* Name – service's name;
* Description – service's description;
* Unit - unit of service, for example, for rent - hour, for excursion - price per person;
* Price – price for unit of service;
* Number of orders – service’s number of orders.

**_Filtering by price:_**

* In the service list view mode, the user sets a price filter and presses the refresh list button (to the
right of the price entry field);
* The application will display a form to view the list of services with updated data. 

**3.2 Add service**

**_Main scenario:_**

* User clicks the “Add” button in the services list view mode;
* Application displays form to enter service data;
* User enters service data and presses “Save” button;
* If any data is entered incorrectly, then error messages is displaying;
* If entered data is valid, then record is adding to database;
* If new service is successfully added, then list of services with added records is displaying.

**_Cancel operation scenario:_**

* User clicks the “Add” button in the services list view mode;
* Application displays form to enter service data;
* User enters service data and presses “Cancel” button;
* Data don’t save in database, then list of services is displaying to user.
* If the user selects the menu item "Orders”, ”Clients” or "Services", the data will not be saved to the
database.

![Add_service.jpg](static%2FAdd_service.jpg)

Pic. 3.2 Add service

When adding a service, the following details are entered:

* Name - service's name;
* Description – service’s description;
* Unit - unit of service, for example, for rent - hour, for excursion - price per person;
* Price – price for unit of service.

_Constraints for data validation:_

* Name – unique, maximum length of 100 characters;
* Description – maximum length of 1000 characters;
* Unit - maximum length of 20 characters;
* Price – whole number bigger than null.

**3.3 Edit service**

**_Main scenario:_**

* User clicks the “Edit” button in the services list view mode;
* Application displays form to enter service data;
* User enters service data and presses “Save” button;
* If any data is entered incorrectly, then error message is displaying;
* If entered data is valid, then edited data is added to database;
* If service record is successfully edited, then list of service with added records is displaying.

**_Cancel operation scenario:_**

* User clicks the “Edit” button in the services list view mode;
* Application displays form to enter service data;
* User enters service data and presses “Cancel” button;
* Data don’t save in database, then list of services records is displaying to user.
* If the user selects the menu item "Orders”, ”Clients” or "Services", the data will not be saved to the database
and.

![Edit_service.jpg](static%2FEdit_service.jpg)

Pic. 3.3 Edit service.

3.4 Removing the service

Main scenario:

* The user, while in the list of service mode, presses the "Delete" button in the selected service line;
* Application displays confirmation dialog “Please confirm delete service?”;
* The user confirms the removal of the service;
* Record is deleted from database;
* If error occurs, then error message displays;
* If service record is successfully deleted, then list of services without deleted record is displaying.

 Cancel operation scenario:

* User is in display mode of services list and press “Delete” button;
* Application displays confirmation dialog “Please confirm delete service?”;
* User press “Cancel” button;
* List of services without changes is displaying.

![Delete_service.jpg](static%2FDelete_service.jpg)

Pic. 3.4 Delete service dialog.


