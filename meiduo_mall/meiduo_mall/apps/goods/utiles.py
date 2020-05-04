def get_breadcrumb(category):
    breadcrumb = {
        'cat1': '',
        'cat2': '',
        'cat3': ''
    }

    if category.parent is None:
        breadcrumb['cat1'] = category.name
    elif category.parent.parent is None:
        breadcrumb['cat2'] = category.name
        breadcrumb['cat3'] = category.parent.name
    else:
        # 当前类别为三级
        breadcrumb['cat3'] = category.name
        cat2 = category.parent
        breadcrumb['cat2'] = cat2.name
        breadcrumb['cat1'] = cat2.parent.name

    return breadcrumb
