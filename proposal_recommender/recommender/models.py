from django.db import models
from model_utils.models import TimeStampedModel
from dj_proposals_candidates.models import Candidate, Proposal
from model_utils.fields import StatusField
from model_utils import Choices
from htmlemailer import send_mail
import uuid


class Recommendation(TimeStampedModel):
    STATUS = Choices('draft', 'sent')
    title = models.CharField(max_length=255)
    status = StatusField()

    def __str__(self):
        return '{title}, {created}, {status}'.format(title=self.title, created=self.created, status=self.status)


class LinkToProposal(TimeStampedModel):
    recommendation = models.ForeignKey('RecommendationForCandidate', on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=False,
                            default=uuid.uuid4)
    has_been_visited = models.BooleanField(default=False)

    def mark_as_visited(self):
        self.has_been_visited = True
        self.save()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('recommender:redirect_to_proposal', kwargs={'uuid': self.uuid})


class RecommendationForCandidate(TimeStampedModel):
    STATUS = Choices('draft', 'sent')
    candidate = models.ForeignKey(Candidate, related_name='recommendations_for', on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, related_name='recommendations_for_candidate', on_delete=models.CASCADE)
    proposals = models.ManyToManyField(to=Proposal, through=LinkToProposal)
    status = StatusField()

    def __str__(self):
        return '{candidate}, {created}, {status}'.format(candidate=self.candidate.name, created=self.created, status=self.status)

    def send_recommendation(self):
        send_mail(
            "emails/mail",
            "Equipo ANTP <mysite@example.org>",
            [self.candidate.email],
            {
                "recommendation": self
            })
