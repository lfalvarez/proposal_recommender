from django.shortcuts import render
from django.views.generic.list import ListView
from recommender.models import Recommendation, RecommendationForCandidate


class RecommendationDetailView(ListView):
    model = RecommendationForCandidate
    paginate_by = 5
    template_name='recommender/recommendation_detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(recommendation__id=self.kwargs['pk'])
        return queryset

