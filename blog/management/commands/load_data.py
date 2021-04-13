import json
import re

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ...models import Post

User = get_user_model()
USER = User.objects.get(id=1)


class Command(BaseCommand):
    help = "Loading blog posts into database."

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):
        list_of_files = options.get('files')
        if list_of_files:
            for file_name in list_of_files:
                with open(file_name, encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        post, created = Post.objects.get_or_create(title=item['title'], author=USER)
                        post.body = item['body']
                        post.status = 'published'
                        matchs = re.findall('(django|python 3|flask|docker)', item['title'], re.I)
                        if matchs:
                            for m in matchs:
                                post.tags.add(m)

                        if not post.body:
                            post.body = 'Future post.'
                            post.status = 'draft'
                        else:
                            post.body = re.sub(r'src\s*=\s*"(.+?)"', r'src="https://www.fullstackpython.com\1"', post.body)

                        post.save()
