from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request, user_id):
        u = get_object_or_404(UserProfile, user=User.objects.get(id=user_id))
        context = {
            'user': u,
        }
        return render(request, self.template_name, context)


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profile_form.html'
    success_url = reverse_lazy('home:profile')

    def get(self, request, user_id):
        pr = get_object_or_404(UserProfile, id=user_id, user=self.request.user)
        form = ProfileForm(instance=pr)
        print(form)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, user_id=None):
        pr = get_object_or_404(UserProfile, id=user_id, user=self.request.user)
        form = ProfileForm(request.POST, request.FILES or None, instance=pr)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pr = form.save(commit=False)
        pr.save()

        return redirect(self.success_url)
