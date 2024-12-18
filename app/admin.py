from django.contrib import admin

from app.models import Profile, Main_page, Summary, Full_report, Payment_history, Id, \
    Commission_structure, Website, Player_report, Payment_history2, Promo_code

# Register your models here.
admin.site.register(Profile)
admin.site.register(Main_page)
admin.site.register(Summary)
admin.site.register(Full_report)
admin.site.register(Payment_history)
admin.site.register(Id)
admin.site.register(Commission_structure)
admin.site.register(Website)
admin.site.register(Player_report)
admin.site.register(Payment_history2)
admin.site.register(Promo_code)
