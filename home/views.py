from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            profile, created = UserProfile.objects.get_or_create(user=user)
            context = {
                'user': user,
                'profile': profile
            }
            return render(request, self.template_name, context)
        except:
            return HttpResponse('User does not exist')


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'profile_form.html'

    def get(self, request, user_id):
        if request.user.id == user_id:
            profile, created = UserProfile.objects.get_or_create(user=user_id)
            form = ProfileForm(instance=profile)
            context = {'form': form}
            return render(request, self.template_name, context)
        else:
            return HttpResponse('<p>You have no permission to edit this page</p>'
                                f'<a href={reverse_lazy("ads:all")}>Go back</a>')

    def post(self, request, user_id):
        if request.user.id != user_id:
            return HttpResponse('<p>You have no permission to edit this page</p>'
                                f'<a href={reverse_lazy("ads:all")}>Go back</a>')
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        form = ProfileForm(request.POST, request.FILES or None, instance=profile)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        profile = form.save(commit=False)
        profile.save()

        return redirect(reverse_lazy('home:profile', args=[user_id]))

