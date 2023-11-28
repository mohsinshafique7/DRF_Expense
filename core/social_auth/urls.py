from django.urls import path

from .views import TwitterSocialAuthView

urlpatterns = [
    # path('google/', GoogleSocialAuthView.as_view()),
    # path('facebook/', FacebookSocialAuthView.as_view()),
    path('twitter/', TwitterSocialAuthView.as_view(), name='twiiter'),
]
