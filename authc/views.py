from django.shortcuts import render
from django.views import View


class OpenView(View) :
    def get(self, request):
        return render(request, 'authz/main.html')
