from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    仅管理员可进行修改，其余用户可查看
    """

    def has_permission(self, request, view):
        # 对所有人允许安全的操作：GET、HEAD、OPTIONS请求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 仅管理员可进行其他操作
        return request.user.is_superuser
