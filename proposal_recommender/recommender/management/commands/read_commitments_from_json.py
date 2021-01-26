from django.core.management.base import BaseCommand, CommandError
from dj_proposals_candidates.models import Proposal, Candidate, Commitment
import json
import datetime as dt
import re


class Command(BaseCommand):
    help = 'Lee un json con los compromisos y carga esto en la BD'

    def add_arguments(self, parser):
        parser.add_argument('json_file_name', nargs=1, type=str)

    def handle(self, *args, **options):
        json_file_name = options['json_file_name'][0]
        with open(json_file_name) as json_file:
            data = json.load(json_file)
            for commitments_dict in data['results']:
                p = re.compile(r"api\/propuestas\/(?P<id>\d+)/\?format")
                m = p.search(commitments_dict['proposal'])
                proposal_id = int(m.group('id'))
                
                p2 = re.compile(r'api\/candidatos\/(?P<slug>[\w-]+)/\?format')
                m2 = p2.search(commitments_dict['candidate'])
                candidate_original_slug = m2.group('slug')

                candidate = Candidate.objects.get(profile_path__contains=candidate_original_slug)
                proposal = Proposal.objects.get(id=proposal_id)
                commitment = Commitment.objects.create(candidate=candidate, proposal=proposal)
                print(commitment)
