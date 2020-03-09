from rest_framework.permissions import BasePermission

from bookshelf.users.models import User


class IsPartner(BasePermission):
    def has_permission(self, request, view):
        try:
            return User.objects.get(mobile_number=request.data['mobile_number']).is_partner
        except Exception as e:
            return False


class IsShopkeeper(BasePermission):
    def has_permission(self, request, view):
        try:
            return request.user.is_partner
        except Exception as e:
            return False
