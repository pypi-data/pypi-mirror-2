from django.db import models
from django.contrib.auth.models import User

class UserOpenID(models.Model):
    user = models.ForeignKey(User, related_name='openids')
    uri = models.CharField(max_length=255, blank=False, null=False)
    insert_date = models.DateTimeField(null=False, blank=False, auto_now_add=True, editable=False)
    last_modified = models.DateTimeField(null=False, blank=False, auto_now=True, editable=False)
