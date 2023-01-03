from .models import Anime


def recent_anime_list(request):
    recent_list = Anime.objects.all().order_by('-creation_date')[:8]
    return {'recent_anime_list': recent_list}


def epic_anime_list(request):
    epic_list = Anime.objects.all().order_by('-views')[:8]
    return {'epic_anime_list': epic_list}


def featured_anime(request):
    anime = Anime.objects.order_by('-creation_date')

    featured_anime_list = None
    if anime:
        featured_anime_list = anime[0]

    return {'featured_anime': featured_anime_list}
