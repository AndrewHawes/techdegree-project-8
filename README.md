# Profile Project
This is the project 8 for the Python Web Development Techdegree program.
It's a searchable and filterable mineral catalog.

- Users can search the catalog by name alone or by all fields.
- Users can filter minerals by starting letter, mineral group, color, and luster.

## Installation

1. Download the project and change into the project directory.
2. Create a new virtual environment 
    - Windows: `python -m venv env` 
    - Linux/Mac `python3 -m venv env`
3. Activate the virtual environment
    - Windows: `.\env\Scripts\activate`
    - Linux/Mac: `source env/bin/activate`
4. `pip install -r requirements.txt` to install the project dependencies.
   - Required JavaScript files are included with the download.
5. `python manage.py migrate` to initialize the database.
    - Mineral data will be loaded from migration files during database initialization.
6. `python manage.py runserver` to start the server on port 8000 (default).
7. Open [127.0.0.1:8000](127.0.0.1:8000) in your browser.
