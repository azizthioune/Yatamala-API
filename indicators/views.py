from django.shortcuts import render

from indicators.serializers import *
from indicators.models import *

from rest_framework import generics, permissions, status
from rest_framework.response import Response


# Create your views here.

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
