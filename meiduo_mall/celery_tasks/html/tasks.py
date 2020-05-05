import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.dev')
import django
django.setup()
from django.template import loader
from django.conf import settings
from celery_tasks.main import celery_app
from goods.models import SKU

from goods.utiles import get_categories, get_goods_and_spec


@celery_app.task(name='generate_static_sku_detail_html')
def generate_static_sku_detail_html(sku_id):
    dict = get_categories()
    goods, specs, sku = get_goods_and_spec(sku_id)
    context = {
        'categories': dict,
        'goods': goods,
        'specs': specs,
        'sku': sku
    }

    template = loader.get_template('detail.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'goods/' + str(sku_id) + '.html')
    with open(file_path, 'w') as f:
        f.write(html_text)


if __name__ == '__main__':
    try:
        skus = SKU.objects.all()
    except Exception as e:
        raise e
    else:
        for sku in skus:
            print(sku.id)
            generate_static_sku_detail_html.delay(sku.id)
