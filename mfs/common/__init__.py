from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from mfs.common.constants import ADMIN_GROUP

# Create super user root.
try:
    grp, _ = Group.objects.get_or_create(name=ADMIN_GROUP)
    usr = get_user_model().objects.create_superuser('root@mfs.com', 'root@mfs.com', 'QAZqaz1983!@#$%^&*()_+')
    usr.groups.add(grp)
except:
    pass