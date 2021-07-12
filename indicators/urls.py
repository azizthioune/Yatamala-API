from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from . import views
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter()

urlpatterns = [

    # route pour l'authentification
    url(r'^auth/register/$', views.UserRegisterView.as_view()),
    url(r'^auth/registerbox/$', views.UserRegisterBoxView.as_view()),
    url(r'^auth/login/$', obtain_jwt_token),
    url(r'^auth/get-token', obtain_jwt_token),
    url(r'^auth/refresh-token', refresh_jwt_token),
    url(r'^auth/verify-token', verify_jwt_token),
    url(r'^auth/userupdate/(?P<pk>[0-9]+)/$',
        views.UserRetrieveUpdateView.as_view()),

    url(r'^auth/change-password/(?P<pk>[0-9]+)/$',
        views.ChangePasswordView.as_view()),
    #url(r'^me/$', views.UserRetrieveView.as_view()),
    url(r'^users/$', views.UserListView.as_view()),

    # route pour Projets
    url(r'^projets/$', views.ProjectsListCreateView.as_view()),
    url(r'^projets/projetById/(?P<pk>[0-9]+)/$',
        views.ProjectRetrieveView.as_view()),

    # route pour Indicateurs
    url(r'^indicateurs/$', views.IndicatorsListCreateView.as_view()),
    url(r'^indicateurs/update/(?P<pk>[0-9]+)/$',
        views.IndicatorsRetrieveUpdateView.as_view()),
    url(r'^indicateurs/remove/(?P<pk>[0-9]+)/$',
        views.IndicatorsDestroyView.as_view()),

    # route pour Indicateurs de suivi
    url(r'^indicateursuivi/$', views.IndicatorsSuiviListCreateView.as_view()),
    url(r'^indicateursuivi/update/(?P<pk>[0-9]+)/$',
        views.IndicatorsSuiviRetrieveUpdateView.as_view()),
    url(r'^indicateursuivi/remove/(?P<pk>[0-9]+)/$',
        views.IndicatorsSuiviDestroyView.as_view()),

    # route pour les annee
    url(r'^annee/$', views.AnneeListCreateView.as_view()),
    url(r'^annee/update/(?P<pk>[0-9]+)/$',
        views.AnneeRetrieveUpdateView.as_view()),
    url(r'^annee/remove/(?P<pk>[0-9]+)/$', views.AnneeDestroyView.as_view()),
]
