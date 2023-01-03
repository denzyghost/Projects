from django.urls import path, reverse_lazy
from .views import Home, HomeAnime, AnimeDetails, SearchAnime, UserProfile, CreateAccount, PrivacyPolicy
from django.contrib.auth import views as auth_view

app_name = 'anime'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('animes/', HomeAnime.as_view(), name='homeanimes'),
    path('animes/<int:pk>', AnimeDetails.as_view(), name='animedetails'),
    path('search-anime/', SearchAnime.as_view(), name='searchanime'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('user-profile/<int:pk>', UserProfile.as_view(), name='userprofile'),
    path('create-account/', CreateAccount.as_view(), name='createaccount'),
    path('change-password/', auth_view.PasswordChangeView.as_view(
        template_name='user-profile.html',
        success_url=reverse_lazy('anime:homeanimes')),
         name='changepassword'),
    path('privacy-policy/', PrivacyPolicy.as_view(), name='privacypolicy'),
    ]