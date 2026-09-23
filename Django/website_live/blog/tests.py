from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse

from blog.forms import RegisterForm
from blog.models import User


class RegisterFormTests(TestCase):
    def test_register_form_exposes_expected_fields(self):
        form = RegisterForm()

        self.assertIn("username", form.fields)
        self.assertIn("email", form.fields)
        self.assertIn("password", form.fields)

    def test_register_form_saves_hashed_password(self):
        form = RegisterForm(
            data={
                "username": "valid_user",
                "email": "valid@example.com",
                "password": "StrongPass1!",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertNotEqual(user.password, "StrongPass1!")
        self.assertTrue(check_password("StrongPass1!", user.password))


class RegisterViewTests(TestCase):
    def test_register_page_renders_form_fields(self):
        response = self.client.get(reverse("blog:register"))

        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="password"')

    def test_register_post_creates_user(self):
        response = self.client.post(
            reverse("blog:register"),
            data={
                "username": "another_user",
                "email": "another@example.com",
                "password": "AnotherPass1!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="another_user").exists())
