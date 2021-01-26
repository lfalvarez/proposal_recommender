from django.db import models
from model_utils.models import TimeStampedModel
from dj_proposals_candidates.models import Candidate, Proposal
from model_utils.fields import StatusField
from model_utils import Choices


class Recommendation(TimeStampedModel):
    STATUS = Choices('draft', 'sent')
    title = models.CharField(max_length=255)
    status = StatusField()

    def __str__(self):
        return '{title}, {created}, {status}'.format(title=self.title, created=self.created, status=self.status)
    

class RecommendationForCandidate(TimeStampedModel):
    STATUS = Choices('draft', 'sent')
    candidate = models.ForeignKey(Candidate, related_name='recommendations_for', on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, related_name='recommendations_for_candidate', on_delete=models.CASCADE)
    proposals = models.ManyToManyField(to=Proposal, related_name='recommended_in')
    status = StatusField()

    def __str__(self):
        return '{candidate}, {created}, {status}'.format(candidate=self.candidate.name, created=self.created, status=self.status)
