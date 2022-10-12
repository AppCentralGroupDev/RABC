from django.contrib.auth.models import Group, Permission , User
import sys

# creates admin group
g1 = Group.objects.create(name='admin')
g1.save()

# add admin to admin group
u1 = User.objects.get(username='admin')
u1.groups.add(g1)
u1.save()
