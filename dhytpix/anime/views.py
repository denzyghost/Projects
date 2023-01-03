from .models import Anime, User
from django.shortcuts import render, redirect, reverse
from .forms import CreateAccountForm, FormPrivacyPolicy
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(ListView):
    template_name = 'home.html'
    model = Anime

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('anime:homeanimes')
        else:
            return super().get(request, *args, **kwargs)


class HomeAnime(ListView):
    template_name = 'home-anime.html'
    model = Anime


class AnimeDetails(DetailView):
    template_name = 'anime-details.html'
    model = Anime

    def get(self, request, *args, **kwargs):
        anime = self.get_object()
        anime.views += 1
        anime.save()

        try:
            user = request.user
            user.historic_animes.add(anime)
        except:
            pass

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnimeDetails, self).get_context_data(**kwargs)
        # self.get_object()
        animes_relacionados = self.model.objects.filter(category=self.get_object().category)[0:5]
        context["animes_relacionados"] = animes_relacionados
        return context


class SearchAnime(LoginRequiredMixin, ListView):
    template_name = "search-anime.html"
    model = Anime

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = self.model.objects.filter(name__icontains=termo_pesquisa)
            return object_list
        else:
            return None


class UserProfile(LoginRequiredMixin, UpdateView):
    template_name = "user-profile.html"
    model = User
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('anime:homeanimes')


class CreateAccount(FormView):
    template_name = 'create-account.html'
    form_class = CreateAccountForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('anime:login')


class PrivacyPolicy(FormView):
    template_name = 'privacy-policy.html'
    form_class = FormPrivacyPolicy

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = User.objects.filter(email=email)
        if usuarios:
            return reverse('anime:login')
        else:
            return reverse('anime:createaccount')


# Errors
def error_404(request, exception):
    return render(request, 'error-404.html')
