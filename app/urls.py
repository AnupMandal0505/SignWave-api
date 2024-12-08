
from django.urls import path
from .views import audio_to_text, get_user,signin,signout,signup,calling,contact_us,payment,create_video_call,save_address,point,otp


urlpatterns = [
    path("get_user",get_user.GetUser, name="get_user"),
    path("update_profile",get_user.UpdateProfileAPI.as_view(), name="update_profile"),
    path('signup', signup.SignupAPI.as_view(), name='signup'),
    path('login', signin.LoginAPI.as_view(), name='login'),
    path('logout', signout.LogoutAPI.as_view(), name='login'),
    path('audio', audio_to_text.AudioToTextAPI.as_view(), name='audio'),
    path('call', calling.CallingAPI.as_view(), name='call'),
    path("contact",contact_us.ContactAPI.as_view(),name = "contact"),
    path("payment",payment.PaymentAPI.as_view(),name = "payment"),
    path("save_address",save_address.SaveAddressAPI.as_view(),name = "save_address"),
    path("get_point",point.PointRecords, name="get_point"),
    path("create_call",create_video_call.CreateCallAPI.as_view(),name = "create_call"),
    path('update_call/<int:id>/',create_video_call.CreateCallAPI.as_view(),name='update_call'),  # For updating calls
    # path('update_address',save_address.SaveAddressAPI.as_view(),name='update_address'),  # For updating calls
    path("user_verify",otp.user_verify, name="user_verify"),
    path("account_create_successful",otp.account_create_successful, name="account_create_successful"),
]


