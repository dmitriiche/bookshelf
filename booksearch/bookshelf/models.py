from django.db import models
import uuid


class Author(models.Model):
    name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=300)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=200, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=400)
    description = models.TextField(blank=True, null=True, default='')
    image_file = models.FileField(blank=True, null=True, upload_to="pictures/")
    image_url = models.URLField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Save only books with unique id
        if not Book.objects.filter(google_id=self.google_id).exists():
            super(Book, self).save(*args, **kwargs)


