import time

from django import template
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase
from urlcrypt.lib import generate_login_token, decode_login_token, encode_token, secret_key_f, base64url_encode
from urlcrypt.conf import URLCRYPT_LOGIN_URL
from urlcrypt import rsa

class UrlCryptTests(TestCase):
    
    def setUp(self):
        super(UrlCryptTests, self).setUp()
        self.test_user = User.objects.create_user('test', 'test@malinator.com', 'test')
    
    def test_login_token(self):
        token = generate_login_token(self.test_user, u'/users/following')
        data = decode_login_token(token)
        self.assertEquals(data['user_id'], self.test_user.id)
        self.assertEquals(data['url'], u'/users/following')
    
    def test_rsa(self):
        assert rsa.decrypt(rsa.encrypt("test")) == "test"
        assert rsa.decrypt(rsa.encrypt("test"*100)) == "test"*100
    
    def test_login_token_failed_hax0r(self):
        fake_token = 'asdf;lhasdfdso'
        response = self.client.get(reverse('urlcrypt_redirect', args=(fake_token,)))
        self.assertRedirects(response, URLCRYPT_LOGIN_URL)
        
        fake_token = base64url_encode(encode_token([str(self.test_user.id), reverse('urlcrypt_test_view'), str(int(time.time()))], secret_key_f))
        response = self.client.get(reverse('urlcrypt_redirect', args=(fake_token,)))
        self.assertRedirects(response, URLCRYPT_LOGIN_URL)
            
    def assert_login_url(self, encoded_url, expected_url):
        response = self.client.get(expected_url)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(encoded_url)
        self.assertRedirects(response, expected_url)
        response = self.client.get(expected_url)
        self.assertEquals(response.status_code, 200)
        
    def test_url_encoded_template_tag(self):
        
        text = """
        {% load urlcrypt_tags %}
        {% encoded_url test_user urlcrypt_test_view %}
        """
        t = template.Template(text)
        c = template.Context({'test_user': self.test_user})
        encoded_url = t.render(c).strip()
        self.assert_login_url(encoded_url, reverse('urlcrypt_test_view'))
    
    def test_url_encoded_template_tag_with_args(self):
        
        text = """
        {% load urlcrypt_tags %}
        {% encoded_url test_user urlcrypt_test_view_username test_user.username %}
        """
        t = template.Template(text)
        c = template.Context({'test_user': self.test_user})
        encoded_url = t.render(c).strip()
        self.assert_login_url(encoded_url, reverse('urlcrypt_test_view_username', args=(self.test_user.username,)))
    
    def test_encode_url_string_template_tag(self):
        text = """
        {% load urlcrypt_tags %}
        {% encode_url_string test_user some_url %}
        """
        some_url = 'http://testserver%s' % reverse('urlcrypt_test_view_username', args=(self.test_user.username,))
        t = template.Template(text)
        c = template.Context({'test_user': self.test_user, 'some_url': some_url})
        encoded_url = t.render(c).strip()
        self.assert_login_url(encoded_url, reverse('urlcrypt_test_view_username', args=(self.test_user.username,)))
     
