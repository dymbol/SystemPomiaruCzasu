from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('race/choose/<int:race_id>', views.choose_race, name="choose_race"),
    path('team/list', views.team_list, name="team_list"),
    path('results', views.results, name="results"),
    path('result/register', views.register_result, name="register_result"),
    path('race/<int:race_id>', views.race, name="race"),
    path('time_meter/<int:team_id>', views.time_meter, name="time_meter")
    #path('articles/2003/', views.special_case_2003),
    #path('articles/<int:year>/', views.year_archive),
    #path('articles/<int:year>/<int:month>/', views.month_archive),
    #path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
