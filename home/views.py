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
        user, created = UserProfile.objects.get_or_create(user=User.objects.get(id=user_id))
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profile_form.html'

    def get(self, request, user_id):
        pr, created = UserProfile.objects.get_or_create(user=self.request.user)
        form = ProfileForm(instance=pr)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, user_id):
        if request.user.id != user_id:
            print('Forbidden!')
            return HttpResponseForbidden()
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        form = ProfileForm(request.POST, request.FILES or None, instance=profile)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        profile = form.save(commit=False)
        profile.save()

        return redirect(reverse_lazy('home:profile', args=[user_id]))

