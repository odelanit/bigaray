from django.urls import path, include

from backend.views import SiteListView, HomePageDataView, CustomAuthToken, ProfileView, MyBrandsView, \
    ToggleUserSiteView, UserCreateView

urlpatterns = [
    path('api/', include('rest_framework.urls')),
    path('api/sessions', CustomAuthToken.as_view()),
    path('api/me', ProfileView.as_view()),
    path('api/users', UserCreateView.as_view()),
    path('api/sites', SiteListView.as_view()),
    path('api/homepage-data', HomePageDataView.as_view()),
    path('api/my-profiles', MyBrandsView.as_view()),
    path('api/toggle-users-sites', ToggleUserSiteView.as_view())
]
