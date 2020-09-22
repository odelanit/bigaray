from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views import View
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Site, Product, UserSite, UserProfile
from backend.serializers import UserSerializer


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            request.user.profile
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=request.user)
        content = {
            "data": {
                "username": request.user.username,
                "last_name": request.user.last_name,
                "last_login": request.user.last_login,
                "id": request.user.id,
                "gender": request.user.profile.gender,
                "first_name": request.user.first_name,
                "email": request.user.email,
                "country": request.user.profile.country,
                "birthday": request.user.profile.birthday
            }
        }
        return Response(content)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'meta': {
                'token': token.key
            },
            'data': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'last_login': user.last_login,
            }
        })


class UserCreateView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            username = validated_data.get('username')
            email = validated_data.get('email')
            password = validated_data.get('password')
            first_name = validated_data.get('first_name')
            last_name = validated_data.get('last_name')
            gender = validated_data.get('gender')
            birthday = validated_data.get('birthday')
            country = validated_data.get('country')
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            profile = UserProfile.objects.create(user=user, gender=gender, birthday=birthday, country=country)
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'user': {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "last_login": user.last_login,
                    "gender": profile.gender,
                    "country": profile.country,
                    "birthday": profile.birthday
                },
                'token': token.key
            })
        else:
            response = Response(serializer.errors)
            response.status_code = 400
            return response


class HomePageDataView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        page_number = int(request.GET.get('page', 0))
        site_type = request.GET.get('site_type', 0)

        user = request.user

        if user.is_anonymous:
            products = Product.objects.filter(site__type=site_type).order_by('?')
            paginator = Paginator(products, 60)
            page_obj = paginator.get_page(page_number)
            result = {
                'data': [model_to_dict(product) for product in page_obj.object_list]
            }
        else:
            offset = page_number * 60
            products = Product.objects.raw("SELECT products.* FROM products LEFT JOIN sites ON products.site_id = sites.id LEFT JOIN user_site us on sites.id = us.site_id WHERE us.user_id=%s AND sites.type=%s ORDER BY random() LIMIT 60 OFFSET %s", [user.id, site_type, offset])
            result = {
                'data': [model_to_dict(product) for product in products]
            }

        return Response(result)


class SiteListView(View):
    def get(self, request):
        sites = Site.objects.all().values('id', 'name', 'display_name', 'last_scraped',
                                          'scrape_url', 'short_url', 'active')
        site_list = list(sites)
        result = {
            'data': site_list
        }

        return JsonResponse(result)


class MyBrandsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sites = Site.objects.all().values('id', 'name', 'display_name', 'last_scraped',
                                          'scrape_url', 'short_url', 'gender', 'active')
        site_list = list(sites)
        user_sites = UserSite.objects.filter(user=request.user).values('id', 'site_id', 'user_id')
        user_site_list = list(user_sites)
        return Response({
            'sites': site_list,
            'my_profiles': user_site_list
        })


class ToggleUserSiteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = JSONParser().parse(request)

        data = payload.get('data')
        used = data.get('used')
        ids = data.get('ids')
        if not used:
            for pk in ids:
                UserSite.objects.create(user=request.user, site_id=pk)
        else:
            for pk in ids:
                UserSite.objects.filter(user=request.user, site_id=pk).delete()

        sites = Site.objects.all().values('id', 'name', 'display_name', 'last_scraped',
                                          'scrape_url', 'short_url', 'gender', 'active')
        site_list = list(sites)
        user_sites = UserSite.objects.filter(user=request.user).values('user_id', 'site_id')
        user_site_list = list(user_sites)
        return Response({
            'sites': site_list,
            'my_profiles': user_site_list
        })
