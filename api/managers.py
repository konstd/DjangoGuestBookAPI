from django.db.models import Manager


class ReviewManager(Manager):
    def get_all_answers(self, pk):
        return self.filter(review=pk).all().order_by('post_date')
