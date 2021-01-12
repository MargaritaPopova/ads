from os import path
import csv
import random
from django.contrib.auth.models import User

from ads.models import Ad, Comment, Fav
from core.models import UserProfile
from mixer.backend.django import mixer

# pipenv run python manage.py runscript filldata

AVATAR_DIR = ''
ADPIC_DIR = 'ads/static/'


def delete_all():
    models = [User, Ad, Comment, Fav, UserProfile]
    for model in models:
        model.objects.all().delete()


def create_ads():
    print('Creating ads...')
    fhand = open('core/management/commands/ads.csv')
    reader = csv.reader(fhand)
    next(reader)
    for row in reader:
        title, price, text, fulldesc, content_type = row

        ad = Ad.objects.create(
            title=title,
            price=price,
            text=text,
            fulldesc=fulldesc,
            owner=random.choice(User.objects.all()),
            content_type=content_type
        )
        ad.save()

    images = {
        'Bicycle': path.join(ADPIC_DIR, 'bike.jpg'),
        'Car': path.join(ADPIC_DIR, 'car.jpg'),
        'Crib': path.join(ADPIC_DIR, 'crib.jpg'),
        'Phone': path.join(ADPIC_DIR, 'phone.jpg'),
        'Coat': path.join(ADPIC_DIR, 'coat.jpg'),
        'Book': path.join(ADPIC_DIR, 'book.jpg'),
        'Cat': path.join(ADPIC_DIR, 'cat.jpg'),
        'Lamp': path.join(ADPIC_DIR, 'lamp.jpg'),
    }
    for title, pic in images.items():
        with open(pic, "rb") as imageFile:
            bytearr = imageFile.read()
            ad = Ad.objects.get(title=title)
            ad.picture = bytearr
            ad.save()
    print('Ads created!')


def create_user_profiles():
    print('Creating user profiles...')
    users = User.objects.all()
    for user in users:
        UserProfile.objects.create(
            home_address='123 Elm street',
            phone_number='384783745875',
            user=user
        )
    print('User profiles created!')


def create_users():
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


def create_comments():
    print('Creating comments...')
    ads = Ad.objects.all()
    users = User.objects.all()
    for ad in ads:
        for _ in range(random.randint(3, 8)):
            mixer.blend(Comment,
                        text=mixer.faker.sentence(nb_words=random.randint(5, 15)),
                        ad=ad,
                        owner=random.choice(users)
                        )
    print('Comments created!')


def run():
    delete_all()
    create_users()
    create_user_profiles()
    create_ads()
    create_comments()
    print('All data filled in!')
