from django.core.management.base import BaseCommand, CommandError
from dj_proposals_candidates.models import Territory, Proposal
#from proposal_similarity_processor.BETO_search_engine import BETOSearchEngine
#from proposal_similarity_processor.similarity_searcher import SimilaritySearcher
from proposal_similarity_processor.document import Document
#from recommender.models import Recomendation
import json
import datetime as dt


class ProposalDocument(Document):
    def __init__(self, proposal):
        self.id = proposal.id
        self.content = proposal.title
        self.proposal = proposal


class Command(BaseCommand):
    help = 'Lee un json con las propuestas y carga esto en la BD'

    def add_arguments(self, parser):
        parser.add_argument('territory_name', nargs=1, type=str)
        parser.add_argument('json_file_name', nargs=1, type=str)

    def handle(self, *args, **options):
        json_file_name = options['json_file_name'][0]
        territory_name = options['territory_name'][0]
        territory, created = Territory.objects.get_or_create(name=territory_name, remote_id=1)
        with open(json_file_name) as json_file:
            data = json.load(json_file)
            for proposal_dict in data['results']:
                date_time_obj = dt.datetime.strptime(proposal_dict['created'], '%Y-%m-%dT%H:%M:%S.%fZ')
                data_keys = proposal_dict['data'].keys()
                if 'solution' in data_keys:
                    solution = proposal_dict['data']['solution']
                if 'solution_at_the_end' in data_keys:
                    solution = proposal_dict['data']['solution_at_the_end']
                proposal, created = Proposal.objects.get_or_create(territory=territory,
                                    remote_id=proposal_dict['id'],
                                    title=proposal_dict['title'],
                                    description=solution,
                                    created=date_time_obj,
                                    votes=proposal_dict['nro_supports']
                                    )
                print(proposal.description)
