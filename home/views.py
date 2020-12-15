from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request, user_id):
        u, created = UserProfile.objects.get_or_create(user=User.objects.get(id=user_id))
        context = {
            'user': u,
        }
        return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profile_form.html'

    def get(self, request, user_id):
        pr, created = UserProfile.objects.get_or_create(user=self.request.user)
        form = ProfileForm(instance=pr)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, user_id):
        if request.user.id != user_id:
            print('Forbidden!')
            return HttpResponseForbidden()
        pr, created = UserProfile.objects.get_or_create(user=self.request.user)
        form = ProfileForm(request.POST, request.FILES or None, instance=pr)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pr = form.save(commit=False)
        pr.save()

        return redirect(reverse_lazy('home:profile', args=[user_id]))

