from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from home.models import UserProfile
from .forms import CreateForm, CommentForm
from .models import Ad, Comment, Fav
from .owner import OwnerListView, OwnerDetailView, OwnerDeleteView


class AdListView(OwnerListView):
    model = Ad
    template_name = 'ads/ad_list.html'

    def get(self, request):

        search = request.GET.get("search", False)
        if search:
            query = Q(title__contains=search)
            query.add(Q(text__contains=search), Q.OR)
            ads = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else:
            ads = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the post_list
        for obj in ads:
            obj.natural_updated = naturaltime(obj.updated_at)

        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_ads.values('id')
            favorites = [row['id'] for row in rows]

        ctx = {'ad_list': ads, 'search': search, 'favorites': favorites}

        return render(request, self.template_name, ctx)


class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

    def get(self, request, pk):
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('updated_at')
        comment_form = CommentForm()
        context = {
            'ad': ad,
            'comments': comments,
            'comment_form': comment_form,
            'comments_count': len(comments)
        }
        return render(request, self.template_name, context)


class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_detail')

    def get(self, request):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)


class AdUpdateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:ad_detail')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        ad = form.save(commit=False)
        ad.save()

        return redirect(self.success_url)


class AdDeleteView(OwnerDeleteView):
    model = Ad


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/comment_delete.html"

    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        print("Add PK", pk)
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav.objects.get_or_create(user=request.user, ad=ad)
        fav.save()  # In case of duplicate key
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        print("Delete PK", pk)
        ad = get_object_or_404(Ad, id=pk)
        Fav.objects.filter(user=request.user, ad=ad).delete()
        return HttpResponse()
