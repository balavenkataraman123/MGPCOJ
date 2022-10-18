from django.contrib import admin
from .models import *

admin.site.register(SiteUser)
admin.site.register(Problem)
admin.site.register(Submission)

