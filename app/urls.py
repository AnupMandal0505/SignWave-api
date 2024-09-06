
from django.urls import path
from .views import audio_to_text, get_user,signin,signout,chatbot,signup

urlpatterns = [
    path("get_user/",get_user.GetUser, name="get_user"),
    path('signup', signup.SignupAPI.as_view(), name='signup'),
    path('login', signin.LoginAPI.as_view(), name='login'),
    path('logout', signout.LogoutAPI.as_view(), name='login'),
    path('att', audio_to_text.AudioToTextAPI.as_view(), name='att'),
    path('chatbot', chatbot.ChatbotAPI.as_view(), name='chatbot'),
]

