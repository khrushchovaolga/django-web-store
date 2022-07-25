from rest_framework import permissions

#Разрешение для админа
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

#Разрешение для редактирования статьи самим создателем ДАНОГО обьекта
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Запросы для чтения даных (get, head, options)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user