from django.core.management.base import BaseCommand, CommandError
from python_graphql_client import GraphqlClient
from dj_proposals_candidates.models import Territory, Proposal
from proposal_similarity_processor.BETO_search_engine import BETOSearchEngine
from proposal_similarity_processor.similarity_searcher import SimilaritySearcher
from proposal_similarity_processor.document import Document
from recommender.models import Recomendation


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

        for candidate in territory.candidates.all():
            possible_proposal_ids = []
            for commitment in candidate.commitments.all():
                docs = searcher.get_closest_doc(commitment.proposal.id, 4)
                for doc in docs:
                    not_the_same = doc != commitment.proposal.id
                    not_previous = doc not in possible_proposal_ids
                    not_previously_commited = not candidate.commitments.filter(proposal__id=doc).exists()
                    if not_the_same and not_previous and not_previously_commited:
                        possible_proposal_ids.append(doc)
            proposals = Proposal.objects.filter(id__in=possible_proposal_ids)
            recommendation = Recomendation.objects.create(title=territory.name,
                                                          candidate=candidate,
                                                          status=Recomendation.STATUS.draft)
            recommendation.proposals.set(proposals)
            print(recommendation)
