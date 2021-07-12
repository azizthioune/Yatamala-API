from rest_framework import serializers
from rest_framework.fields import CharField
from indicators.models import *


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class ChangePasswordSerializer(serializers.ModelSerializer):
    confirm_password = CharField(write_only=True)
    new_password = CharField(write_only=True)
    old_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password',
                  'old_password', 'new_password', 'confirm_password']

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
            raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
            raise serializers.ValidationError({'old_password': 'not found'})

        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError(
                {'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['confirm_password']:
            raise serializers.ValidationError(
                {'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['confirm_password'] and instance.check_password(validated_data['old_password']):
            # instance.password = validated_data['new_password']
            print(instance.password)
            instance.set_password(validated_data['new_password'])
            print(instance.password)
            instance.save()
            return instance
        return instance


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
                  'password', 'avatar', 'is_active', 'user_type', 'date_joined')
        depth = 1

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone'],
            user_type=validated_data['user_type'],
            avatar=validated_data['avatar'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'user_permissions', 'groups', 'is_superuser', 'is_active', 'is_staff', 'password', 'date_joined',
            'last_login')


class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'groups', 'is_superuser', 'password', 'date_joined',
            'last_login')


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


# class IndicateurSuiviSerializer(serializers.ModelSerializer):
#     nom_indicateur = serializers.ReadOnlyField(source='indicateur.libelle')

#     class Meta:
#         model = Indicateursuivi
#         read_only_fields = ('id_indicateursuivi', 'nom_indicateur')
#         fields = '__all__'
#         #fields = ('id', 'category_name', 'name',)


class IndicateurSerializer(serializers.ModelSerializer):
    nom_projet = serializers.ReadOnlyField(source='projet.nom')
    #indicateursuivi = IndicateurSuiviSerializer(many=True, read_only=True)

    class Meta:
        model = Indicateur
        read_only_fields = ('id_indicateur', 'nom_projet')
        fields = '__all__'
        #fields = ('id', 'category_name', 'name',)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projet
        fields = '__all__'


class ProjetGetSerializer(serializers.ModelSerializer):
    indicateurs = IndicateurSerializer(many=True, read_only=True)

    class Meta:
        model = Projet
        fields = '__all__'
        depth = 1

# Serializer for Indicators


class IndicateurGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicateur
        fields = '__all__'
        depth = 1

# Serializer for Indicators follow up


class IndicateurSuiviSerializer(serializers.ModelSerializer):
    # indicateur = serializers.SlugRelatedField(
    #     many=True, queryset=Indicateursuivi.objects.all(), slug_field='indicateur')
    #indicateur = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    libelle_indicateur = serializers.ReadOnlyField(source='indicateur.libelle')
    code_indicateur = serializers.ReadOnlyField(source='indicateur.code')

    class Meta:
        model = Indicateursuivi
        read_only_fields = ('id_indicateursuivi', 'nom_indicateur')
        fields = '__all__'
        #fields = ('id', 'category_name', 'name')

    # def to_representation(self, instance):
    #     self.fields['indicateur'] = IndicateurSerializer(read_only=True)
    #     return super(IndicateurSuiviSerializer, self).to_representation(instance)
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['indicateur'] = IndicateurSerializer(
    #         instance.indicateur).data
    #     return response


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
