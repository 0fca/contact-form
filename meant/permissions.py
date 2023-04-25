from rest_framework.permissions import BasePermission


class AdminOnly(BasePermission):

    def has_permission(self, request, view):
        # Okay, this works. 
        # And what in case if we would like to add far more views than one and far more than there are admin only views? Bunch of ifs?
        # It is always better to enumarate what needs an elevated access and all other just default to False or True.
        # What's more it is always more clear in such notation to enumerate actions which need elevated access, so it is visible just by looking over here
        # So, to keep it clean - add a global variable with view.action name strings which need elevated access and iterate through it over here - if view.action 
        # is in there and the user is super user then you allow it, otherwise - True or False.
        if view.action == 'create':
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return view.action in ['list', 'retrieve', 'update', 'partial_update', ] and request.user.is_superuser
