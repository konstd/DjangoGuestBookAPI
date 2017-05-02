import datetime
from django.contrib.auth.models import User

from rest_framework import serializers

from api.models import Review
from api.models import ReviewComment


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        response = super(SignUpSerializer, self).to_representation(instance)
        if 'password' in response:
            response['password'] = '********'
        return response


class AddReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'body')
        read_only_fields = ('id', )

    def to_internal_value(self, data):
        data = super(AddReviewSerializer, self).to_internal_value(data)
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        data['user'] = user
        return data


class AddReviewCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewComment
        fields = ('id', 'body', 'review')
        read_only_fields = ('id', )

    def to_internal_value(self, data):
        data = super(AddReviewCommentSerializer, self).to_internal_value(data)
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        data['user'] = user
        return data


class GetReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'user', 'post_date', 'body', 'answers')
        read_only_fields = ('id', 'user', 'post_date', 'body', 'answers')

    answers = serializers.SerializerMethodField()
    post_date = serializers.SerializerMethodField()

    def get_answers(self, instance):
        return list(ReviewComment.objects.get_all_answers(instance.pk).values('id', 'user', 'body'))

    def get_post_date(self, instance):
        epoch = datetime.datetime.utcfromtimestamp(0)
        timestamp = int((instance.post_date.replace(tzinfo=None) - epoch).total_seconds())
        return timestamp
