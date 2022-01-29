from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns  = [
    path('usevote/<str:pk>/' , views.usevote , name='usevote'),
    path('viewStats/<str:pk>/' , views.viewStats , name='viewStats'),
    path('adminviewStats/<str:pk>/' , views.adminviewStats , name='adminviewStats'),
    path('myProfile/' , views.myProfile , name='myProfile'),
    path('login/' , views.login_view , name='login'),
    path('register/' , views.registration_view , name='register'),
    path('logout/' , views.logout_view , name='logout'),
    path('' , views.home , name='home'),
    path('adminlogin/' , views.adminlogin , name='adminlogin'),
    path('adminlogout/' , views.adminlogout_view , name='adminlogout'),
    path('adminmenu/' , views.adminmenu , name='adminmenu'),   
    path('premiumpage/<str:username>/' , views.premiumpage , name='premiumpage'),
    path('adminaccounts/' , views.adminaccounts , name='adminaccounts'),  
    path('adminseeelection/' , views.adminseeelection , name='adminseeelection'), 
    path('admincreateelection/' , views.admincreateelection , name='admincreateelection'), 
    path('pagefailed/', views.pagefailed_view, name='pagefailed'),
    path('admincancel/' , views.admincancel , name='admincancel'),
    path('usevote_nonregistered/', views.usevote_nonregistered, name='usevote_nonregistered'),
    



    # Password reset links 
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='evote/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='evote/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='evote/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='evote/password_reset_complete.html'),
     name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)