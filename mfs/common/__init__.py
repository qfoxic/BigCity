from django.contrib.auth.models import User
# Create super user root.
try:
    User.objects.create_superuser('root', 'wwwbnv@uke.nee', 'QAZqaz1983!@#$%^&*()_+')
except:
    pass