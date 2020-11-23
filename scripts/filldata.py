import base64
import csv
import random
from django.contrib.auth.models import User

from ads.models import Ad, Comment, Fav

# pipenv run python manage.py runscript filldata


def run():
    models = [Ad, Comment, Fav]
    for model in models:
        model.objects.all().delete()

    print('Creating users...')
    users = [
        {
            'username': 'johnwick',
            'firstname': 'John',
            'lastname': 'Wick',
            'email': 'jw@mail.com',
            'is_staff': 0
        },
        {
            'username': 'brucewayne',
            'firstname': 'Bruce',
            'lastname': 'Wayne',
            'email': 'bw@mail.com',
            'is_staff': 0
        },
        {
            'username': 'jasonbourne',
            'firstname': 'Jason',
            'lastname': 'Bourne',
            'email': 'jb@mail.com',
            'is_staff': 0
        },
        {
            'username': 'jamesbond',
            'firstname': 'James',
            'lastname': 'Bond',
            'email': 'jb7@mail.com',
            'is_staff': 0
        },
    ]
    for user in users:
        User.objects.get_or_create(username=user['username'],
                                   first_name=user['firstname'],
                                   last_name=user['lastname'],
                                   email=user['email'],
                                   is_staff=user['is_staff'])
    print('Users created!')

    print('Creating ads...')
    fhand = open('home/management/commands/ads.csv')
    reader = csv.reader(fhand)
    next(reader)

    for row in reader:
        title = row[0]
        price = row[1]
        text = row[2]
        content_type = row[3]

        ad = Ad.objects.create(
            title=title,
            price=price,
            text=text,
            owner=random.choice(User.objects.all()),
            content_type=content_type
        )
        ad.save()
    print('Ads created!')

    images = {
        'Bicycle': 'ads/static/bike.jpg',
        'Car': 'ads/static/car.jpg',
        'Crib': 'ads/static/crib.jpg',
        'Phone': 'ads/static/phone.jpg',
        'Coat': 'ads/static/coat.jpg',
        'Book': 'ads/static/book.jpg',
        'Cat': 'ads/static/cat.jpg',
        'Lamp': 'ads/static/lamp.jpg',
    }

    for title, pic in images.items():
        with open(pic, "rb") as imageFile:
            bytearr = imageFile.read()
            ad = Ad.objects.get(title=title)
            ad.picture = bytearr
            ad.save()

    print('All data filled in!')
