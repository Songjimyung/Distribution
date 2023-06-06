from rest_framework import permissions 



'''
작성자:장소은
내용: 관리자 외에는 ReadOnly만 허용하는 권한
작성일:2023.06.06
'''
class IsAdminUserOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user and request.user.is_admin
