from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render, redirect
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Site(models.Model):
    GENDERS = [
        (1, 'Women'),
        (2, 'Men')
    ]
    TYPES = [
        (1, 'New'),
        (2, 'Sale')
    ]
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    last_scraped = models.DateTimeField()
    scrape_url = models.URLField()
    short_url = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    gender = models.IntegerField(choices=GENDERS)
    type = models.IntegerField(choices=TYPES)
    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ManyToManyField(User, through="UserSite")

    class Meta:
        db_table = 'sites'
        ordering = ['-last_scraped']

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.display_name, self.get_gender_display(), self.get_type_display())

    def toggle_status(self):
        if self.active:
            self.active = False
        else:
            self.active = True
        self.save()


class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'display_name', 'last_scraped', 'short_url', 'active', 'gender', 'type', 'site_actions')
    list_per_page = 20
    readonly_fields = ('last_scraped', 'site_actions')

    def toggle_status(self, request, object_id, *args, **kwargs):
        site = self.get_object(request, object_id)
        site.toggle_status()
        return redirect(request.META['HTTP_REFERER'])

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/status/', self.admin_site.admin_view(self.toggle_status), name='backend_site_toggle_active')
        ]
        return custom_urls + urls

    def site_actions(self, obj):
        if obj.active:
            name = 'Deactivate'
        else:
            name = 'Activate'
        return format_html('<a class="el-button" href={}>{}</a>',
                           reverse('admin:backend_site_toggle_active', kwargs={'object_id': obj.pk}),
                           name
                           )

    site_actions.short_description = "Change Status"
    site_actions.allow_tags = True


class Product(models.Model):
    title = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    sale_price = models.CharField(max_length=255)
    product_link = models.URLField()
    hq_image_filename = models.CharField(max_length=255)

    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-inserted_at']

    def __str__(self):
        return self.title

    @property
    def image_preview(self):
        if self.image_filename:
            return mark_safe('<img src="/images/{0}" width="100" height="150" />'.format(self.image_filename))
        else:
            return ""


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'title', 'image_preview', 'price', 'sale_price', 'product_link', 'get_gender')
    search_fields = ('title', 'price', 'url', 'sale_price')
    list_filter = ('site', 'site__gender')
    # list_display_links = ('product_link',)
    readonly_fields = ('image_preview',)
    list_per_page = 50

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

    def get_gender(self, obj):
        return obj.site.get_gender_display()

    get_gender.short_description = 'Gender'
    get_gender.admin_order_field = 'site__gender'


class UserSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_site'


class UserSiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'site')


class UserProfile(models.Model):
    GENDERS = [
        (1, 'Women'),
        (2, 'Men')
    ]
    gender = models.IntegerField(choices=GENDERS, null=True)
    birthday = models.DateField(null=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)

    class Meta:
        db_table = 'profile'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'birthday', 'country')
    list_filter = ('gender', 'birthday', 'country',)