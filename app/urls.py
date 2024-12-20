from . import views
from django.urls import path

urlpatterns = [
    path('index/', views.index, name='index'),
    path('f404/', views.f404, name='f404'),
    path('login1/', views.login1, name='login1'),
    path('register1/', views.register1, name='register1'),
    path('terms/', views.terms, name='terms'),
    path('faq/', views.faq, name='faq'),
    path('admin/', views.admin, name='admin'),
    path('approve_user/<str:uid>/', views.approve_user, name='approve_user'),
    path('account/', views.account, name='account'),
    path('aff_links/', views.aff_links, name='aff_links'),
    path('commission_structure/', views.commission_structure, name='commission_structure'),
    path('contacts/', views.contacts, name='contacts'),
    path('full_report/', views.full_report, name='full_report'),
    path('media/', views.media, name='media'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('playerreport/', views.playerreport, name='playerreport'),
    path('promocode/', views.promocode, name='promocode'),
    path('statistics/', views.statistics, name='statistics'),
    path('summary/', views.summary, name='summary'),
    path('test/', views.test, name='test'),
    path('webpages/', views.webpages, name='webpages'),
    path('cookies/', views.cookies, name='cookies'),
    path('news/', views.news, name='news'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('reset/', views.reset, name='reset'),
    # path('reset_password/<uid>/<token>/', views.reset_password, name='reset_password'),
    path('reset_password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password')

]
