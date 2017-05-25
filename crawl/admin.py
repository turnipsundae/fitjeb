from django.contrib import admin

from crawl.models import Workout, Benchmark, Crawled

# Register your models here.
admin.site.register(Workout)
admin.site.register(Benchmark)
admin.site.register(Crawled)
