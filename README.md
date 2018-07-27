# Chat Analyzer

## About
Chat Analyzer is a website that can analyze its users messages and produce statistics regarding their messaging habits such as positivity.
It can also find the owner of a given message and calculates best user match for a given user. 
### Built With
 [Django Web Framework](https://docs.djangoproject.com/en/2.0/)
### Prerequisites

This project requires the following libraries and frameworks to be installed:

* Django>=2.0
* scipy
* psycopg2
* nltk>=3.0
* numpy
* scikit_learn

### Usage


The data that is used to make predictions in the entire app is trained using supervised machine learning algorihtms. You can download the trained data from [here](https://drive.google.com/open?id=1hLbG181dw-FW4s1DUk7SQBZnSA3vcPti). 
After downloading the trained data, copy it under *analyzer/trained_data*.
Then specifiy the database that you want the app to use by editing the *settings.py* file under *chatanalyzer/*.
To populate the database use the command:
```
python manage.py populatedatabase
```

This will fill the database with sample users and messages

Then you can start the server and browse through the website with 
```
python manage.py runserver
```
The code that is used for training is under *analyzer/management/commands* and can be used with a different dataset.
