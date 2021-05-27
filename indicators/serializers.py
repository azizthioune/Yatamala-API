from rest_framework import serializers
from indicators.models import *


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

    def create(self, validated_data):

        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name',
                  'password', 'avatar', 'is_active')
        depth = 1

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            #avatar = validated_data['avatar'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        depth = 1

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            #avatar = validated_data['avatar'],
            is_active=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserVisiteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'user_permissions', 'groups', 'is_superuser', 'is_active', 'is_staff', 'password', 'date_joined',
            'last_login')


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        depth = 1

# Serializer for Projects


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projet
        fields = '__all__'


class ProjetGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = '__all__'
        depth = 1

# Serializer for Indicators


class IndicateurSerializer(serializers.ModelSerializer):
    nom_projet = serializers.ReadOnlyField(source='projet.nom')

    class Meta:
        model = Indicateur
        read_only_fields = ('id_indicateur', 'nom_projet')
        fields = '__all__'
        #fields = ('id', 'category_name', 'name',)


class IndicateurGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicateur
        fields = '__all__'
        depth = 1

# Serializer for Indicators follow up


class IndicateurSuiviSerializer(serializers.ModelSerializer):
    nom_indicateur = serializers.ReadOnlyField(source='indicateur.libelle')

    class Meta:
        model = Indicateursuivi
        read_only_fields = ('id_indicateursuivi', 'nom_indicateur')
        fields = '__all__'
        #fields = ('id', 'category_name', 'name',)


class IndicateurSuiviGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicateursuivi
        fields = '__all__'
        depth = 1

# Serializer for years


class AnneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annee
        fields = '__all__'


class AnneeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annee
        fields = '__all__'
        depth = 1
