from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Group)
admin.site.register(Contest)
admin.site.register(ContestWinner)
admin.site.register(ContestFinalist)
admin.site.register(GroupRole)
admin.site.register(State)
admin.site.register(City)
admin.site.register(RawContact)
admin.site.register(GroupToken)
admin.site.register(RawParticipant)
admin.site.register(RawSchool)
admin.site.register(RawProject)
admin.site.register(Category)
admin.site.register(ProjectCategory)
admin.site.register(TokenUses)


