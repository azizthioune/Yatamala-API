from django.shortcuts import render

from indicators.serializers import *
from indicators.models import *

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from indicatorsApi import settings
from rest_framework_jwt.settings import api_settings
#from decouple import config
#from api.utils import Utils as my_utils


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.

# Authentification views


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)


class UserRegisterBoxView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserBoxSerializer

    def post(self, request, *args, **kwargs):
        # users=User.objects.all();
        # print('the users are', users)
        # for u in users:
        #     if request.data['email']==u.email:
        #         print('user exist')

        serializer = UserBoxSerializer(data=request.data)
        # print('new user', request.data)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully created",
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        # users=User.objects.all();
        # print('the users are', users)
        # for u in users:
        #     if request.data['email']==u.email:
        #         print('user exist')

        serializer = UserSerializer(data=request.data)
        # print('new user', request.data)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        data = serializer.data
        data = UserBasicSerializer(data).data

        # print('data',data)
        # createing account activation code
        activation = AccountActivation.objects.create(
            user=User.objects.get(pk=data['id']))
        # send confirmation mail
        data_ = {
            'email': data['email'],
            'name': data['first_name'],
            'code': activation.code
        }

        # if not 'test' in sys.argv:
        #    mail_html = my_utils.confirmation_mail_html()
        #    mail_txt = my_utils.confirmation_mail_txt()
        #    activation_url = 'http://andu.volkeno-tank.com' + '/api/user/'+str(activation.code)+'/confirm/'

        # setting user name and activation btn in template
        #    mail_html = mail_html.replace('{{name}}', data['first_name'])
        #    mail_html = mail_html.replace('{{activation_url}}', activation_url)

        #    mail_txt = mail_txt.replace('{{name}}', data['first_name'])
        #    mail_txt = mail_txt.replace('{{activation_url}}', activation_url)
        # print(mail_txt)

        #    r = my_utils.send_email(request.data['email'], config('CONFIRMATION_MAIL_SUBJECT'), mail_html, mail_txt)
        # print('regiter mail', r.text)

        return Response({
            "status": "success",
            "message": "item successfully created",
            'data': data
        }, status=status.HTTP_201_CREATED)


class PasswordResetRequestView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        # get user using email
        # if user

        if 'email' not in request.data or request.data['email'] is None:
            return Response({
                "status": "failure",
                "message": "no email provided",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_ = User.objects.get(email=request.data['email'])
            # generate random code
            code_ = my_utils.get_random()
            # crete and save pr object
            PasswordReset.objects.create(
                user=user_,
                code=code_
            )

            if not 'test' in sys.argv:
                # template from utils
                html = my_utils.password_reset_mail_html()
                text = my_utils.password_reset_mail_txt()

                html = html.replace('{{first_name}}', user_.first_name)
                html = html.replace('{{last_name}}', user_.last_name)
                html = html.replace('{{reset_code}}', code_)

                text = text.replace('{{first_name}}', user_.first_name)
                text = text.replace('{{last_name}}', user_.last_name)
                text = text.replace('{{reset_code}}', code_)

                # print('regiter mail', text)

                # send mail to user
                r = my_utils.send_email(request.data['email'], config(
                    'PASSWORD_RESET_MAIL_SUBJECT'), html, text)
                # print('password mail', r.text)

        except User.DoesNotExist:
            # print('sen error mail')
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": "success",
            "message": "item successfully saved ",
        }, status=status.HTTP_201_CREATED)


class PasswordResetView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        if 'code' not in request.data or request.data['code'] is None:
            return Response({
                "status": "failure",
                "message": "no code provided",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        if 'email' not in request.data or request.data['email'] is None:
            return Response({
                "status": "failure",
                "message": "no email provided",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        if'new_password' not in request.data or 'new_password_confirm' not in request.data or request.data['new_password'] is None or request.data['new_password'] != request.data['new_password_confirm']:
            return Response({
                "status": "failure",
                "message": "non matching passwords",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        user_ = User.objects.get(email=request.data['email'])
        code_ = request.data['code']
        if user_ is None:
            return Response({
                "status": "failure",
                "message": "no such item",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        passReset = PasswordReset.objects.filter(
            user=user_, code=code_, used=False).order_by('-date_created').first()
        # print(passReset)
        if passReset is None:
            return Response({
                "status": "failure",
                "message": "no passwordRequest founded",
                "error": "not such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() >= passReset.expiration:
            return Response({
                "status": "failure",
                "message": "expired",
                "error": "expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        user_.set_password(request.data['new_password'])
        user_.save()
        passReset.used = True
        passReset.date_used = timezone.now()
        passReset.save()

        return Response({
            "status": "success",
            "message": "item successfully saved",
        }, status=status.HTTP_201_CREATED)


# retrieve all users
class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserBasicSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.user.email)

        if not user:
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_400_BAD_REQUEST)

        data = UserBasicSerializer(user).data

        return Response({
            "status": "success",
            "message": "item successfully created",
            "data": data
        }, status=status.HTTP_200_OK)

# For edit a user


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserPutSerializer

    def get(self, request, *args, **kwargs):

        user = User.objects.get(id=kwargs['pk'])
        serializer = UserSerializer(user)
        data = serializer.data

        return Response({
            "status": "success",
            "message": "items successfully retrieved.",
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        try:
            user = User.objects.get(id=kwargs['pk'])
            # print('the user to edit is', user)
        except User.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserPutSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully update",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.all()

        if user is None:
            return Response({
                "status": "failure",
                "message": "not user found",
                "count": 0,
                "nb_user_active": 0
            }, status=status.HTTP_404_NOT_FOUND)

        count = user.count()
        serializer = UserSerializer(user, many=True)
        return Response({

            "status": "success",
            "message": "items successfully retrieved.",
            "count": count,
            "data": serializer.data,

        }, status=status.HTTP_200_OK)


# vue pour les projets


class ProjectsListCreateView(generics.ListCreateAPIView):

    queryset = Projet.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):

        serializer = ProjectSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": serializer.errors,
                "error": "erreur"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        items = Projet.objects.all()
        serializer = ProjectSerializer(items, many=True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": items.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# project by id
class ProjectRetrieveView(generics.RetrieveAPIView):

    queryset = Projet.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):

        try:
            projet = Projet.objects.get(id_projet=kwargs['pk'])
        except Projet.DoesNotExist:
            response = {
                "status": "failure",
                "message": "no such item",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        data = ProjetGetSerializer(projet).data

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "data": data
        }, status=status.HTTP_200_OK)


# vue pour les indicateurs


class IndicatorsListCreateView(generics.ListCreateAPIView):

    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer

    def post(self, request, *args, **kwargs):

        serializer = IndicateurSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": serializer.errors,
                "error": "erreur"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        items = Indicateur.objects.all()
        serializer = IndicateurSerializer(items, many=True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": items.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# Modification indicateurs


class IndicatorsRetrieveUpdateView(generics.RetrieveUpdateAPIView):

    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer

    def get(self, request, *args, **kwargs):

        try:
            indicateur = Indicateur.objects.get(pk=kwargs['pk'])
        except Indicateur.DoesNotExist:
            response = {
                "status": "failure",
                "message": "no such item",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        data = IndicateurGetSerializer(indicateur).data

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        try:
            indicateur = Indicateur.objects.get(id_indicateur=kwargs['pk'])
        except Indicateur.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        indicator_data = {
            'code': request.data['code'],
            'libelle': request.data['libelle'],
            'niveau': request.data['niveau'],
            'unite': request.data['unite'],
            'nature': request.data['nature'],
            'calcul': request.data['calcul'],
            'reference': request.data['reference'],
            'cible': request.data['cible'],
            'valeur': request.data['valeur'],
            'datemaj': request.data['datemaj'],
            'description': request.data['description'],
            'updated': request.data['updated'],
        }

        serializer = IndicateurSerializer(
            indicateur, data=indicator_data, partial=True)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully update",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# Supprimer indicateur
class IndicatorsDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer

    def post(self, request, *args, **kwargs):
        indicateur = Indicateur.objects.get(id_indicateur=kwargs['pk'])

        if not indicateur:
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_400_BAD_REQUEST)

        indicateur.delete()
        return Response({
            "status": "success",
            "message": "item successfully deleted",
        }, status=status.HTTP_200_OK)


# vue pour les indicateurs de suivi


class IndicatorsSuiviListCreateView(generics.ListCreateAPIView):

    queryset = Indicateursuivi.objects.all()
    serializer_class = IndicateurSuiviSerializer

    def post(self, request, *args, **kwargs):

        serializer = IndicateurSuiviSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": serializer.errors,
                "error": "erreur"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        items = Indicateursuivi.objects.all()
        serializer = IndicateurSuiviSerializer(items, many=True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": items.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# Modification indicateurs de suivi


class IndicatorsSuiviRetrieveUpdateView(generics.RetrieveUpdateAPIView):

    queryset = Indicateursuivi.objects.all()
    serializer_class = IndicateurSuiviSerializer

    def get(self, request, *args, **kwargs):

        try:
            indicateursuivi = Indicateursuivi.objects.get(pk=kwargs['pk'])
        except Indicateursuivi.DoesNotExist:
            response = {
                "status": "failure",
                "message": "no such item",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        data = IndicateurSuiviGetSerializer(indicateursuivi).data

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        try:
            indicateursuivi = Indicateursuivi.objects.get(
                id_indicateursuivi=kwargs['pk'])
        except Indicateursuivi.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        indicatorsuivi_data = {
            'valeur': request.data['valeur'],
            'datemaj': request.data['datemaj'],
            'observation': request.data['observation'],
            'updated': request.data['updated'],
        }

        serializer = IndicateurSuiviSerializer(
            indicateursuivi, data=indicatorsuivi_data, partial=True)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully update",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# Supprimer indicateur de suivi
class IndicatorsSuiviDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Indicateursuivi.objects.all()
    serializer_class = IndicateurSuiviSerializer

    def post(self, request, *args, **kwargs):
        indicateursuivi = Indicateursuivi.objects.get(
            id_indicateursuivi=kwargs['pk'])

        if not indicateursuivi:
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_400_BAD_REQUEST)

        indicateursuivi.delete()
        return Response({
            "status": "success",
            "message": "item successfully deleted",
        }, status=status.HTTP_200_OK)


# vue pour les annee


class AnneeListCreateView(generics.ListCreateAPIView):

    queryset = Annee.objects.all()
    serializer_class = AnneeSerializer

    def post(self, request, *args, **kwargs):

        serializer = AnneeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": serializer.errors,
                "error": "erreur"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        items = Annee.objects.all()
        serializer = AnneeSerializer(items, many=True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": items.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

# Modification annee


class AnneeRetrieveUpdateView(generics.RetrieveUpdateAPIView):

    queryset = Annee.objects.all()
    serializer_class = AnneeSerializer

    def get(self, request, *args, **kwargs):

        try:
            annee = Annee.objects.get(pk=kwargs['pk'])
        except Annee.DoesNotExist:
            response = {
                "status": "failure",
                "message": "no such item",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        data = IndicateurSuiviGetSerializer(annee).data

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        try:
            annee = Annee.objects.get(
                id_annee=kwargs['pk'])
        except Annee.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        annee_data = {
            'code': request.data['code'],
            'observation': request.data['observation'],
            'resume': request.data['resume'],
            'updated': request.data['updated'],
        }

        serializer = AnneeSerializer(
            annee_data, data=annee_data, partial=True)

        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": "invalid data",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully update",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


# Supprimer annee
class AnneeDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Annee.objects.all()
    serializer_class = AnneeSerializer

    def post(self, request, *args, **kwargs):
        annee = Annee.objects.get(
            id_annee=kwargs['pk'])

        if not annee:
            return Response({
                "status": "failure",
                "message": "no such item",
            }, status=status.HTTP_400_BAD_REQUEST)

        annee.delete()
        return Response({
            "status": "success",
            "message": "item successfully deleted",
        }, status=status.HTTP_200_OK)
