# product-Backend
 - It is an product details application

# Technologies Used
 - Django 
 - Mongodb


## Getting started
To get started with Logging, follow these steps:

- Clone the repository to your local machine
- Install the required packages listed in requirements.txt
- Set up your mongodb database and create a collection for storing logs or you can you this command `python manage.py migarte`
- Start the Djnago application using `make run` or  `python manage.py runserver`


## Note
- All requests must have Authorization token in headers # optinal 
- To install all packages using `make install` or `pip install -r requirements.txt`
- after creating task you have to run command `python manage.py property_data {task_id}`