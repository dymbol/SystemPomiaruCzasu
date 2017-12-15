from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('race/list', views.race_list, name="race_list"),
    path('race/choose/<int:race_id>', views.choose_race, name="choose_race"),
    path('team/list', views.team_list, name="team_list"),
    path('results', views.results, name="results"),
    path('result/register', views.register_result, name="register_result"),
    path('change_track/<int:race_id>', views.change_track, name="change_track"),
    path('time_meter/<int:team_id>', views.time_meter, name="time_meter"),
    path('save_result/<int:team_id>/<int:track_id>/<int:_result>/<int:_fee>/<int:_taryfa>',
         views.save_result, name="save_result")

    #path('articles/2003/', views.special_case_2003),
    #path('articles/<int:year>/', views.year_archive),
    #path('articles/<int:year>/<int:month>/', views.month_archive),
    #path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
]
