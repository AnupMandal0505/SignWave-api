
from django.urls import path
from .views import audio_to_text, get_user,signin,signout,chatbot,signup,calling,contact_us

urlpatterns = [
    path("get_user",get_user.GetUser, name="get_user"),
    path("users",get_user.ListUsers, name="list_users"),
    path('signup', signup.SignupAPI.as_view(), name='signup'),
    path('login', signin.LoginAPI.as_view(), name='login'),
    path('logout', signout.LogoutAPI.as_view(), name='login'),
    path('audio', audio_to_text.AudioToTextAPI.as_view(), name='audio'),
    path('chatbot', chatbot.ChatbotAPI.as_view(), name='chatbot'),
    path('call', calling.CallingAPI.as_view(), name='call'),
    path("contact",contact_us.ContactAPI.as_view(),name = "contact"),

]

