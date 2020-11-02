from django.contrib import admin
from scraping.models import Scraper, ScraperAdmin

admin.site.register(Scraper, ScraperAdmin)
