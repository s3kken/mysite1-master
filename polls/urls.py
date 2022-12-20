from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'polls'
urlpatterns = [
    path('user/<int:pk>/update_account/', views.UpdateDate.as_view(), name='update_account'),
    path('personal_account/', views.PersonalAccount.as_view(), name='personal_account'),
    path('', views.IndexView.as_view(), name='home_page'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register', views.RegisterUser.as_view(), name='register'),
]