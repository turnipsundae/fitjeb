from django.db import models

# Create your models here.
class Workout(models.Model):
    """Workout represents one WOD page. May contain duplicates."""
    __tablename__ = 'workouts'

    title = models.CharField(max_length=255)
    description = models.TextField()
    uom = models.CharField(max_length=255)
    link = models.URLField(max_length=255, help_text="URL to the WOD page")
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Workout(title='%s', description='%s')>" % (self.title, self.description)
