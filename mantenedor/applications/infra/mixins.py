from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class PerfilAutorizadoMixin(UserPassesTestMixin):
    grupos_permitidos = []  # Debe ser una lista de nombres de grupos permitidos

    def test_func(self):
        return self.request.user.groups.filter(name__in=self.grupos_permitidos).exists()

    def handle_no_permission(self):
        return redirect('/')