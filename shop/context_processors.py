from .models import Category


def categories(request):
    """
    Retrieve all categories that have no parent category
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}
