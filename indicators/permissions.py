from rest_framework import permissions
from indicators import models


class IsUserTypeAuthenticated(permissions.BasePermission):

    # permission_classes = (
    #         permissions.IsAuthenticated,
    # )
    # authentication_classes = (BasicAuthentication, JSONWebTokenAuthentication)
    def has_permission(self, request, view):
        if request.user.is_authenticated:

            # allow all POST requests
            if request.user.user_type == models.ADMIN or request.user.user_type == models.CREATOR or request.user.user_type == models.TEACHER:
                return True
            elif request.user.user_type == 'basic':
                return False
        return True

        print('not auth')
        # return Response({
        #         "status": "failure",
        #         "message": "invalid data",
        #         "errors": 'invalid'
        #     }, status=status.HTTP_400_BAD_REQUEST)`


class IsAdminUser(permissions.BasePermission):

    # permission_classes = (
    #         permissions.IsAuthenticated,
    # )
    # authentication_classes = (BasicAuthentication, JSONWebTokenAuthentication)
    def has_permission(self, request, view):
        if request.user.is_authenticated() and request.user.is_staff():
            return True

        return False

        print('not auth')
        # return Response({
        #         "status": "failure",
        #         "message": "invalid data",
        #         "errors": 'invalid'
        #     }, status=status.HTTP_400_BAD_REQUEST)`
