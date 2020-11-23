from django.urls import reverse
from factory import django
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import Ad


class AdFactory(django.DjangoModelFactory):
    class Meta:
        model = Ad

    title = 'Phone'
    price = 5000
    text = 'Brand new phone, color black'
    content_type = 'image/jpeg'
    picture = 'static/phone.jpg'


class TestAd(TestCase):

    def setUp(self):
        self.ad = AdFactory.build()

    def tearDown(self):
        pass

    def test_str(self):
        print(f'testing {self.__class__.__name__}: {self.test_str.__name__}')
        self.assertEqual(str(self.ad), 'Phone')

    def test_get_likes(self):
        print(f'testing {self.__class__.__name__}: {self.test_get_likes.__name__}')
        self.assertEqual(self.ad.get_likes(), 0)


class TestListView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345678qwerty')
        self.response = self.client.get(reverse('ads:all'))

    def test_index(self):
        print(f'testing {self.__class__.__name__}: {self.test_index.__name__}')
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'ads/ad_list.html')
        self.assertContains(self.response, 'There are no ads')
        self.assertQuerysetEqual(self.response.context['ad_list'], [])

    def test_favs(self):
        print(f'testing {self.__class__.__name__}: {self.test_favs.__name__}')

        self.client.login(username='testuser', password='12345678qwerty')
        self.assertTrue('favorites' in self.response.context)

    def test_menu(self):
        print(f'testing {self.__class__.__name__}: {self.test_menu.__name__}')
        self.assertContains(self.response, 'Login')
        self.client.login(username='testuser', password='12345678qwerty')
        response = self.client.get('/')
        self.assertContains(response, 'Logout')
        self.client.logout()


class TestCreateView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345678qwerty')
        self.ad = AdFactory.build(owner=self.user)
        self.url = reverse('ads:ad_create')

    def test_post(self):
        print(f'testing {self.__class__.__name__}: {self.test_post.__name__}')

        self.client.login(username='testuser', password='12345678qwerty')
        self.client.post(self.url,
                         {'title': self.ad.title, 'text': self.ad.text, 'price': self.ad.price})
        response = self.client.get(reverse('ads:all'))

        with self.subTest():
            self.assertContains(response, 'class="card')
            self.assertContains(response, 'btn-success')
            self.assertContains(response, self.ad.title)
            self.assertQuerysetEqual(response.context['ad_list'], ['<Ad: Phone>'])

    def test_permissions(self):
        print(f'testing {self.__class__.__name__}: {self.test_permissions.__name__}')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='12345678qwerty')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

