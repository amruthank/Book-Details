from django.db import models

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length = 50)
    isbn = models.CharField(max_length = 50)
    numberOfPages = models.IntegerField(default=1)
    publisher = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)
    released = models.DateField(null = True, blank = True)

    def __str__(self):
        return "The book %s is created on %s."%(self.name, self.released)


class Author(models.Model):
    book = models.ForeignKey(Book, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)

    def __str__(self):
        return "%s %s is the author of the book %s."% (self.first_name, self.last_name, self.book.name)

