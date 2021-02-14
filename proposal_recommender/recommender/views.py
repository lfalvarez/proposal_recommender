from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from recommender.models import Recommendation, RecommendationForCandidate, LinkToProposal


class RecommendationDetailView(ListView):
    model = RecommendationForCandidate
    paginate_by = 5
    template_name='recommender/recommendation_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(recommendation__id=self.kwargs['pk'])
        return queryset


class RedirectToOriginalView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        link_to_proposal = get_object_or_404(LinkToProposal, uuid=kwargs['uuid'])
        link_to_proposal.mark_as_visited()
        return link_to_proposal.proposal.remote_url
