from goods.models import SKU, SKUImage, SKUSpecification, GoodsSpecification, SpecificationOption, GoodsCategory, \
    GoodsChannel
from django.http import JsonResponse
from collections import OrderedDict


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


def get_goods_and_spec(sku_id):
    try:
        sku = SKU.objects.get(id=sku_id)
        sku.images = SKUImage.objects.filter(sku=sku)
    except Exception as e:
        return JsonResponse({
            'code': 400,
            'errmsg': '访问数据库失败'
        })
    sku_specs = SKUSpecification.objects.filter(sku=sku).order_by('spec_id')

    sku_key = []

    for spec in sku_specs:
        sku_key.append(spec.option_id)

    goods = sku.goods
    skus = SKU.objects.filter(goods=goods)

    dict = {}
    for temp_sku in skus:
        s_specs = SKUSpecification.objects.filter(sku=temp_sku).order_by('spec_id')

        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        dict[tuple(key)] = temp_sku.id

    specs = GoodsSpecification.objects.filter(goods=goods).order_by('id')

    for index, spec in enumerate(specs):
        key = sku_key[:]
        spec_options = SpecificationOption.objects.filter(spec=spec)

        for option in spec_options:
            key[index] = option.id
            option.sku_id = dict.get(tuple(key))

        spec.spec_options = spec_options

    return goods, specs, sku


def get_categories():
    # =====================生成上面字典格式数据=======================
    # 第一部分: 从数据库中取数据:
    # 定义一个有序字典对象
    categories = OrderedDict()

    # 对 GoodsChannel 进行 group_id 和 sequence 排序, 获取排序后的结果:
    channels = GoodsChannel.objects.order_by('group_id',
                                             'sequence')

    # 遍历排序后的结果: 得到所有的一级菜单( 即,频道 )
    for channel in channels:
        # 从频道中得到当前的 组id
        group_id = channel.group_id

        # 判断: 如果当前 组id 不在我们的有序字典中:
        if group_id not in categories:
            # 我们就把 组id 添加到 有序字典中
            # 并且作为 key值, value值 是 {'channels': [], 'sub_cats': []}
            categories[group_id] = {
                'channels': [],
                'sub_cats': []
            }

        # 获取当前频道的分类名称
        cat1 = channel.category

        # 给刚刚创建的字典中, 追加具体信息:
        # 即, 给'channels' 后面的 [] 里面添加如下的信息:
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })

        # 根据 cat1 的外键反向, 获取下一级(二级菜单)的所有分类数据, 并遍历:
        cat2s = GoodsCategory.objects.filter(parent=cat1)
        # cat1.goodscategory_set.all()
        for cat2 in cat2s:
            # 创建一个新的列表:
            cat2.sub_cats = []
            cat3s = GoodsCategory.objects.filter(parent=cat2)
            # 根据 cat2 的外键反向, 获取下一级(三级菜单)的所有分类数据, 并遍历:
            for cat3 in cat3s:
                # 拼接新的列表: key: 二级菜单名称, value: 三级菜单组成的列表
                cat2.sub_cats.append(cat3)
            # 所有内容在增加到 一级菜单生成的 有序字典中去:
            categories[group_id]['sub_cats'].append(cat2)
        return categories
