from .models import Category, Subcategory, SubSubcategory


def filter_context_processor(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.select_related('category').all()
    subsubcategories = SubSubcategory.objects.select_related('subcategory__category').all()
    return {'categories': categories, 'subcategories': subcategories, 'subsubcategories': subsubcategories}
