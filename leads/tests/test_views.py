from django.http import response
from django.test import TestCase
from django.shortcuts import reverse
# Create your tests here.

class LandingPageTest(TestCase):

    def test_status_code(self):
        #TO Do some sort of test
        response = self.client.get(reverse('landing-page'))
        # print(response.content)  Way to display all content in page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response , 'landing_page.html')