from datetime import datetime
from datetime import timedelta

from django.contrib.auth.backends import UserModel
from django.test import TestCase
from oauth2_provider.admin import Application
from oauth2_provider.models import AccessToken
from unittest import mock

from api.models import Review


class APITest(TestCase):
    ADD_REVIEW_URL = '/api/review/add/'
    ADD_REVIEW_COMMENT_URL = '/api/review/comment/add/'
    GET_ALL_REVIEWS_URL = '/api/reviews/'

    def setUp(self):
        self.user = UserModel.objects.create(username='dummy', email='dummy@site.com')
        self.app = self._create_app(self.user)
        self.token = self._create_token(self.user)

    def tearDown(self):
        Review.objects.all().delete()

    def api_add_new_review_entity(self, payload=None, comment=False):
        response = self.client.post(
            self.ADD_REVIEW_URL if not comment else self.ADD_REVIEW_COMMENT_URL,
            HTTP_AUTHORIZATION=self.get_auth_header(self.token),
            data=payload,
        )
        return response

    def api_get_all_reviews(self):
        response = self.client.get(
            self.GET_ALL_REVIEWS_URL,
            HTTP_AUTHORIZATION=self.get_auth_header(self.token),
        )
        return response

    @staticmethod
    def _create_auth_header(token):
        return "Bearer {}".format(token)

    @staticmethod
    def _create_app(user):
        app = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris='https://localhost',
            name='dummy',
            user=user
        )
        return app

    def _create_token(self, user):
        access_token = AccessToken.objects.create(
            user=user,
            scope='read write',
            expires=datetime.now() + timedelta(seconds=300),
            token='secret-access-token-key',
            application=self.app
        )
        return access_token

    def get_auth_header(self, token):
        return self._create_auth_header(token)

    def test_add_review_without_authentication(self):
        payload = {
            'body': "New text body",
        }
        expected_response = {
            'detail': "Authentication credentials were not provided.",
        }
        response = self.client.post(
            '/api/review/add/',
            data=payload,
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(response.data, expected_response)

    def test_add_review_comment_without_authentication(self):
        # create review at first
        review_payload = {
            'body': "New text body",
        }
        expected_review_response = {
            'id': mock.ANY,
            'body': "New text body",
        }
        review_response = self.api_add_new_review_entity(review_payload)
        self.assertEqual(review_response.status_code, 201)
        self.assertDictEqual(review_response.data, expected_review_response)

        # create comment for review
        comment_payload = {
            'body': "New text body",
        }
        comment_expected_response = {
            'detail': "Authentication credentials were not provided.",
        }
        response = self.client.post(
            '/api/review/add/',
            data=comment_payload,
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(response.data, comment_expected_response)

    def test_add_review_without_body(self):
        response = self.api_add_new_review_entity()
        expected_response = {
            'body': [
                'This field is required.'
            ]
        }
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, expected_response)

    def test_add_review_with_body(self):
        payload = {
            'body': "New text body",
        }
        expected_response = {
            'id': mock.ANY,
            'body': "New text body",
        }
        response = self.api_add_new_review_entity(payload)
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response.data, expected_response)

    def test_add_comment_without_body(self):
        # create review at first
        review_payload = {
            'body': "New text body",
        }
        expected_review_response = {
            'id': mock.ANY,
            'body': "New text body",
        }
        review_response = self.api_add_new_review_entity(review_payload)
        self.assertEqual(review_response.status_code, 201)
        self.assertDictEqual(review_response.data, expected_review_response)

        # create comment for review
        comment_payload = {
            'review': review_response.data['id'],
        }
        comment_expected_response = {
            'body': [
                'This field is required.'
            ]
        }
        comment_response = self.api_add_new_review_entity(comment_payload, comment=True)
        self.assertEqual(comment_response.status_code, 400)
        self.assertEqual(comment_response.data, comment_expected_response)

    def test_add_comment_with_body(self):
        # create review at first
        review_payload = {
            'body': "New text body",
        }
        review_expected_response = {
            'id': mock.ANY,
            'body': "New text body",
        }
        review_response = self.api_add_new_review_entity(review_payload)
        self.assertEqual(review_response.status_code, 201)
        self.assertDictEqual(review_response.data, review_expected_response)

        # create comment for review
        comment_payload = {
            'body': "New review comment",
            'review': review_response.data['id']
        }
        comment_expected_response = {
            'id': mock.ANY,
            'body': "New review comment",
            'review': review_response.data['id'],
        }
        comment_response = self.api_add_new_review_entity(comment_payload, comment=True)
        self.assertEqual(comment_response.status_code, 201)
        self.assertDictEqual(comment_response.data, comment_expected_response)

    def test_create_comment_with_nonexistant_review_id(self):
        comment_payload = {
            'body': "New review comment",
            'review': 199
        }
        comment_expected_response = {
            'review': ['Invalid pk "199" - object does not exist.']
        }
        comment_response = self.api_add_new_review_entity(comment_payload, comment=True)
        self.assertEqual(comment_response.status_code, 400)
        self.assertDictEqual(comment_response.data, comment_expected_response)

    def test_get_reviews(self):
        # create first review
        review_payload = {
            'body': "New text body",
        }
        review_expected_response = {
            'id': mock.ANY,
            'body': "New text body",
        }
        review_response = self.api_add_new_review_entity(review_payload)
        self.assertEqual(review_response.status_code, 201)
        self.assertDictEqual(review_response.data, review_expected_response)

        # create comment for review
        comment_payload = {
            'body': "New review comment",
            'review': review_response.data['id']
        }
        comment_expected_response = {
            'id': mock.ANY,
            'body': "New review comment",
            'review': review_response.data['id'],
        }
        comment_response = self.api_add_new_review_entity(comment_payload, comment=True)
        self.assertEqual(comment_response.status_code, 201)
        self.assertDictEqual(comment_response.data, comment_expected_response)

        # get all reviews with pagination
        reviews_expected_response = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': review_response.data['id'],
                    'user': self.user.pk,
                    'post_date': mock.ANY,
                    'body': "New text body",
                    'answers': [
                        {
                            'user': self.user.pk,
                            'id': comment_response.data['id'],
                            'body': "New review comment"
                        }
                    ]
                }
            ],
        }
        reviews_response = self.api_get_all_reviews()
        self.assertEqual(reviews_response.status_code, 200)
        self.assertDictEqual(reviews_response.data, reviews_expected_response)
