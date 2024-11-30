from django.contrib import admin

from app.models import Profile,Main_page, Summary,Full_report,Payment_history


# Register your models here.
admin.site.register(Profile)
admin.site.register(Main_page)
admin.site.register(Summary)
admin.site.register(Full_report)
admin.site.register(Payment_history)