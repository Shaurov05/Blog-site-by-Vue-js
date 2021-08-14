# Blog application using Django and Vue js

#### Download the code to your PC, unpack the zip and move inside the folder.

#### 1. Create a new Python Virtual Environment:
```
python3 -m venv venv
```

#### 2. Activate the environment and install all the Python/Django dependencies:

```
source ./venv/bin/activate
pip install -m ./requirements.txt
```

### 3. Create a Postgres database named "blogsite"
Go to <strong>settings.py</strong> file and replace the password used in the database section with your own custom password.


#### 4. Apply the migrations as usual.
```
python manage.py makemigations
python manage.py migrate
```

#### 5. Install the Vue JS dependencies:
```
cd Blog-site-by-Vue-js/frontend
npm install
```

#### 6. Run Vue JS Development Server:
```
npm run serve
```

#### 7. Run Django's development server:
```
python manage.py runserver
```
