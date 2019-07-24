from rest_framework import permissions

from api.events.models import Event, MemberType


class EventPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Event):
        member = obj.members.get(user=request.user)

        if request.method in ['POST', 'UPDATE', 'PATCH']:
            if member.type != MemberType.GUEST:
                return True

        if request.method == 'DELETE':
            if member.type == MemberType.ADMINISTRATOR:
                return True

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return False
