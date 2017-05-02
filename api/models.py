from api import mixins
from api.managers import ReviewManager


class Review(mixins.ReviewMixin):
    pass


class ReviewComment(mixins.ReviewMixin):
    review = mixins.models.ForeignKey(Review, related_name='review_comments')

    objects = ReviewManager()
