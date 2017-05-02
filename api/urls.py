from django.conf.urls import include
from django.conf.urls import url

from api.views import AddComment
from api.views import AddReview
from api.views import GetReviews
from api.views import SignUp


urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    url(r'^sign-up/', SignUp.as_view(), name='api-sign-up'),
    url(r'^review/add/', AddReview.as_view(), name='api-review-add'),
    url(r'^review/comment/add/', AddComment.as_view(), name='api-comment-add'),
    url(r'^reviews/', GetReviews.as_view(), name='api-reviews-get'),

]
