from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    #Main and Home Urls
    path("", views.Accounting_Society, name="Accounting_Society"),
    path("home/", views.Home, name='Home'),
    path("home/Attendance/", views.attendance, name='attendance'),
    path("home/Event/", views.EventPage, name='event'),
    path('home/User_profile/', views.profile, name='User_profile'),
    path("home/User_profile/logout", views.Log_out, name='logout'),
    path('home/suggestion_list/', views.suggestion_list, name='suggestion_list'),
  
    #Attendance Urls
    path('home/Attendance/update_attendance/', views.update_attendance_status, name='update_attendance_status'),
    path('home/Attendance/delete_attendance/<str:a_id>/', views.delete_attendance, name="delete_attendance"),
    path('home/Attendance/delete_event/<str:z_id>', views.delete_event, name="delete_event"),
    path("home/Attendance/give_feedback/", views.feedback_update, name='feedback_status'),
    path("home/Attendance/backtohome/", views.returnhome, name='backtohome'),
    path("home/Attendance/Event/backtohome/", views.returnhome, name='backtohome'),
    
    #Event Urls
    path('home/Event/event_booking/', views.Event_Table, name='Book_Event'),
    path('home/Event/backtohome/', views.returnhome, name='backtohome'),
    path('home/Event/Attendance/backtohome/', views.returnhome, name='backtohome'),
    path('home/Event/event_booking/update_join_event/<str:event_id>', views.update_join_event, name="update_join_event"),
    path('home/Event/event_booking/backtohome', views.returnhome, name='backtohome'),
    
    #Profile 
    path('home/User_profile/backtohomeprofile/', views.backtohomeprofile, name="backtohomeprofile"),
    path('home/User_profile/Update_profile/', views.profile_view, name="Update_profile"),
    path('home/User_profile/Update_profile/backEditProfile', views.backEditProfile, name="backEditProfile"),
    path('home/User_profile/Activities/backtoActivities', views.backActivities, name="backtoActivities"),
    path('home/User_profile/delete_User/<str:s_id>', views.delete_User, name="delete_User"),
    path('home/User_profile/User_suggestion/', views.suggestion_personal, name="suggestion_personal"),
    path('home/User_profile/User_suggestion/delete_suggestion/<str:suggestion_id>', views.delete_suggestion, name="delete_suggestion"),
    path('home/User_profile/User_suggestion/edit_suggestion/', views.update_suggestion_comment, name='update_suggestion_comment'),
    path('home/User_profile/User_suggestion/backEditProfile', views.backEditProfile, name="backEditProfile"),


    #Suggestion
    path('home/suggestion_list/backtohome/', views.returnhome, name='backtohome'),
    path('home/User_profile/User_suggestion/add_suggestion', views.add_suggestion, name='add_suggestion'),
    ]


urlpatterns += staticfiles_urlpatterns()


