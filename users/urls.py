from django.urls import path
from .views import RegisterView, CustomLoginView, LogoutView, ConfigurateView, ProfileView
from .forms import LoginForm
app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, next_page='/users/profile/<str:username>/',
                                           template_name='users/login.html',
                                           authentication_form=LoginForm), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('configurate/', ConfigurateView.as_view(), name='configurate'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile')
]
