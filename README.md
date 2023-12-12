# budget-tracker
a budget tracker

## how to run server
1. make a virtual environment if you don't have it
``
python -m venv .venv
``

2. activate the virtual environment
```
on windows
.venv\Scripts\activate

on linux
source .venv/bin/activate
```

3. install django ``pip install django``
4. go to the directory with manage.py ``cd BudgetTracker``
5. set up the database (only do this at beginning or if you edited the models.py file)
```
python manage.py makemigrations
python manage.py migrate
````
6. run
``python manage.py runserver``
 
