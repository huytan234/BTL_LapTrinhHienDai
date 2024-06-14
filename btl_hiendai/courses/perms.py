from rest_framework import permissions


class PaymentOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, payment):
        return super().has_permission(request, view) and request.user == payment.user
        # if not request.user.is_authenticated:
        #     return False
        # return request.user == obj.user


class AdminOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False
