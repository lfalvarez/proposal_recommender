from django.core.management.base import BaseCommand, CommandError
from python_graphql_client import GraphqlClient
from dj_proposals_candidates.models import Territory
from proposal_similarity_processor.BETO_search_engine import BETOSearchEngine
from proposal_similarity_processor.similarity_searcher import SimilaritySearcher
from proposal_similarity_processor.document import Document


class ProposalDocument(Document):
    def __init__(self, proposal):
        self.id = proposal.id
        self.content = proposal.title
        self.proposal = proposal


class Command(BaseCommand):
    help = 'crea recomendaciones para todos los candidatos'

    def add_arguments(self, parser):
        parser.add_argument('territory_name', nargs=1, type=str)

    def handle(self, *args, **options):
        territory_name = options['territory_name'][0]
        territory = Territory.objects.get(name=territory_name)
        searcher = SimilaritySearcher(BETOSearchEngine)
        for proposal in territory.proposals.all():
            proposal_doc = ProposalDocument(proposal)
            searcher.add_document(proposal_doc)
