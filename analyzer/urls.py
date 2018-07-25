from django.urls import path
from analyzer import views

app_name = 'analyzer'
urlpatterns = [
    path('', views.StatisticsView.as_view(), name='statistics'),
    path('suggestFriends/', views.SuggestFriendsView.as_view(), name='suggest_friends'),
    path('findOwner/', views.FindOwnerView.as_view(), name='find_owner'),
    path('currentUser/', views.CurrentUserStatsView.as_view(), name='current_user'),
    path('currentUser/<str:username>/<str:chart_name>/', views.ChartView.as_view(), name = 'chart' ),
    path('findOwnerResult/' , views.FindOwnerResultView.as_view(), name = 'find_owner_result')
]
