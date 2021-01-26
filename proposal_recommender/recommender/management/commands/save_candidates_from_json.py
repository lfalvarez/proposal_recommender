from django.core.management.base import BaseCommand, CommandError
from dj_proposals_candidates.models import Territory, Candidate
from django.utils.text import slugify
import json


class Command(BaseCommand):
    help = 'Lee un json con los candidatos y carga esto en la BD'

    def add_arguments(self, parser):
        parser.add_argument('territory_name', nargs=1, type=str)
        parser.add_argument('json_file_name', nargs=1, type=str)

    def handle(self, *args, **options):
        json_file_name = options['json_file_name'][0]
        territory_name = options['territory_name'][0]
        territory, created = Territory.objects.get_or_create(name=territory_name, remote_id=1)
        with open(json_file_name) as json_file:
            data = json.load(json_file)
            for candidate_dict in data:
                Candidate.objects.create(name=candidate_dict['name'],
                                         profile_path=candidate_dict['get_absolute_url'],
                                         img_url=candidate_dict['get_absolute_url'],
                                         nickname=slugify(candidate_dict['name']),
                                         territory=territory)