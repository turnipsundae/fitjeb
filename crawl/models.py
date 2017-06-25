from django.db import models

# Create your models here.
class Workout(models.Model):
    """Workout represents one WOD page. May contain duplicates."""
    __tablename__ = 'workouts'

    title = models.CharField(max_length=255)
    description = models.TextField()
    uom = models.CharField(max_length=255)
    link = models.URLField(max_length=255, help_text="URL to the WOD page")
    date = models.DateField()
    created_on = models.DateTimeField("Created on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "<Workout(title='%s', description='%s')>" % (self.title, self.description)

class Benchmark(models.Model):
    """
    Benchmark represents the min, max and average Rx'd results for
    a Workout.
    """
    __tablename__ = 'benchmark'

    workout = models.ForeignKey(Workout)
    gender = models.CharField(max_length=255)
    min_age = models.IntegerField(null=True)
    avg_age = models.IntegerField(null=True)
    max_age = models.IntegerField(null=True)
    min_score = models.DecimalField(max_digits=10, decimal_places=2)
    avg_score = models.DecimalField(max_digits=10, decimal_places=2)
    max_score = models.DecimalField(max_digits=10, decimal_places=2)
    total_rxd = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    uom = models.CharField(max_length=255)

    def __str__(self):
        return "%s, %s %s" % (self.gender, self.avg_score, self.uom)
        
    def __repr__(self):
        return "<Benchmark('%s, %s %s')>" % (self.gender, self.avg_score, self.uom)

class Crawled(models.Model):
    """
    Workouts that have been crawled, success or failure.
    """
    __tablename__ = 'crawled'

    link = models.URLField(max_length=255, help_text="The URL to the WOD page")
    date = models.DateField()
    success = models.CharField(max_length=255)
    crawled_on = models.DateTimeField("Crawled on", auto_now_add=True)
    updated_on = models.DateTimeField("Updated on", auto_now=True)
    
    def __str__(self):
        return "%s %s" % (self.date, self.success)
        
    def __repr__(self):
        return "<Crawled('%s %s')>" % (self.date, self.success)
