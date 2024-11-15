from django.db import models
from django.contrib.auth.models import User  # This is a builtIn model provided by the Django itself
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    # In the below, we like to have a function for no of ratings Here the self will refer the current movie. So if we
    # call this function with the movie then the self will be the movie itself. We need to get the ratings first,
    # and then we have to check how many total no of ratings are there for that specific Movie
    def no_of_ratings(self):
        ratings = Rating.objects.filter(movie=self)  # Here we are selecting all the ratings on our database
        return len(ratings)

    def avg_rating(self):
        sums = 0
        ratings = Rating.objects.filter(movie=self)  # Here we are selecting all the ratings on our database
        for rating in ratings:
            sums += rating.stars
        if len(ratings) > 0:
            return sums / len(ratings)
        else:
            return 0



class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # For which movie we are giving the rating
    # In the above on_delete=models.CASCADE means if we have a rating for a movie which don't exist in the
    # database then it will break our application, So whenever the Movie model is removed then we will
    # cascade the rating and remove it as well
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Which user is giving rating for which movie?
    # In the above, The User model we are referring to is the builtIn model User provided by the Django itself.
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'movie'),)  # If we already have a rating for a specific movie by one user
        # and if you like to create a new rating for the same movie with the same user, then it will be
        # rejected because we have here the unique_together field
        index_together = (('user', 'movie'),)
        # indexes = [models.Index(fields=['user', 'movie'])] => This is the updated version from Django-5, which is v5
