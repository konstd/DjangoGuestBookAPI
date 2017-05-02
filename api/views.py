from rest_framework import generics
from rest_framework import permissions

from api.serializers import AddReviewSerializer
from api.serializers import AddReviewCommentSerializer
from api.serializers import GetReviewsSerializer
from api.serializers import User
from api.serializers import SignUpSerializer

from api.models import Review
from api.models import ReviewComment
from api.paginators import StandardResultsSetPagination
from api.permissions import IsAuthenticatedOrCreate


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all().order_by('post_date')
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate, )


class AddReview(generics.CreateAPIView):
    queryset = Review.objects.all().order_by('post_date')
    serializer_class = AddReviewSerializer
    permission_classes = (permissions.IsAuthenticated, )


class AddComment(generics.CreateAPIView):
    queryset = ReviewComment.objects.all().order_by('post_date')
    serializer_class = AddReviewCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GetReviews(generics.ListAPIView):
    queryset = Review.objects.all().order_by('post_date')
    serializer_class = GetReviewsSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (permissions.IsAuthenticated, )
