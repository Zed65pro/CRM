Django Project Setup
This guide provides step-by-step instructions to set up a Django project with Django REST framework and MySQL.

Prerequisites
Python (>=3.7)
Pipenv
MySQL database server

Setup
1. Clone the repository
>git clone https://github.com/your-username/your-django-project.git
>cd your-django-project

2. Set up virtual environment (Windows)
>python -m venv venv
- for Windows
>venc/Scripts/activate 
- for Linux
>venv/bin/activate

3. Install Dependencies
>pip install -r requirements.txt
- (Special step) For windows (for mysqlclient error mitigation)
>pip install mysqlclient-1.4.6-cp37-cp37m-win_amd64.whl
- Otherwise
>pip install mysqlclient

3. Create a MySQL Database

Create a MySQL database for your Django project.
>CREATE DATABASE your_database_name;

4. Configure Database Settings
Update your database configuration
- Create .env file
Use .env.example as an example to fill the details

5. Apply Migrations
>python manage.py makemigrations
>python manage.py migrate

6. Create Superuser (Optional)
>python manage.py createsuperuser

7. Run the Development Server
>python manage.py runserver

Additional Configuration
Adjust other settings in yourproject/settings.py as needed.

Contribution
Feel free to contribute to this project. Submit a pull request or open an issue if you have any suggestions or improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.