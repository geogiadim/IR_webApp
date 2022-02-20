# Django web app for Information Retrieval project

### About
Search engine in order to submit queries and get most relevant documents from this <a href='https://zenodo.org/record/4311577#.YhJeuhuxVPp'>dataset</a>.

### Installation Guide 
___

1. Fork this project.
2. Clone this repository into a directory on your local machine.
3. Install a python virtual environment inside your new directory
    ```
    $ pip install virtualenv
    $ virtualenv -p python3 venv
    ```
    For Linux or Mac OS
    ```  
    $ virtualenv venv 
    ```
    For Windows
    ```
    $ virtualenv -p python3 venv
    ```
   
4. Activate the installed venv using below commands  
    For Linux:
    ```
    $ . venv/bin/activate
    ```
    For Windows:
    ```
    $ venv\Scripts\activate
    ```
  
### Requirements 
___
In the project directory, install the required packages inside your activated ```venv``` using
```
$ pip install -r requirements.txt
```
### Run
___
In order to run this Web app run below command inside your activated ```venv```
```
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```