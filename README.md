# Rock Merch Shop

## Overview
Rock Merch Shop is a Django-based web application designed for rock music fans to explore merchandise related to their favorite bands and albums.
The project allows users to browse items by categories and bands, view detailed item descriptions, rate products and more.

## Features
- **User Registration and Authentication**: Allows users to register, login and logout.
- **Product Catalog**: Users can view products categorized by band and genre.
- **Search Functionality**: Includes a search bar for users to find products.
- **Ratings**: Registered users can rate products with a 5-star rating system.
- **Admin Panel**: Administrators can add, edit, and delete products, categories, bands and manage user groups nad privileges.

## Technologies Used
- Django 5.0.3
- Python 3.12.2
- SQLite3
- HTML5, CSS3, JavaScript for front-end
- Bootstrap 5.3.0
- jQuery 3.6.0
- Django Widget Tweaks for form rendering

## Installation

1. Clone the repository:
```bash
git cline https://github.com/Charilaos1995/ITC_4214_Internet-Programming_Final_Project.git
```

2. Navigate to the project directory:
```bash
cd rock_merch_shop
```

3. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate # On Windows use 'venv\Scripts\activate'
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

5. Set up your .env file with your 'DJANGO_SECRET_KEY' and database settings.

6. Migrate the database:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Collect static files:
```bash
python manage.py collectstatic
```

9. Run the development server:
```bash
python manage.py runserver
```

## Deployment
- For deployment  instructions, refer to the [Django documentation](https://docs.djangoproject.com/en/5.0/howto/deployment/). 

## Contributing
Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
