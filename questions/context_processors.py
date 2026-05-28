from .sidebar_cache import get_best_members, get_popular_tags


def sidebar(request):
    return {
        'sidebar_popular_tags': get_popular_tags(),
        'sidebar_best_members': get_best_members(),
    }
