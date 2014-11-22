from django.contrib.auth import get_user_model
# Create super user root.
try:
    get_user_model().objects.create_superuser('root', 'wwwbnv@uke.nee', 'QAZqaz1983!@#$%^&*()_+')
except:
    pass