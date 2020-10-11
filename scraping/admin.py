from django.contrib import admin
from scraping.models import Scraper, ScraperAdmin, ScraperLog, ScraperLogAdmin

admin.site.register(Scraper, ScraperAdmin)
admin.site.register(ScraperLog, ScraperLogAdmin)
