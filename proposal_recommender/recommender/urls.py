from django.urls import path

from proposal_recommender.recommender.views import (
    RecommendationDetailView,
    RedirectToOriginalView,
)

app_name = "recommender"
urlpatterns = [
    path("<int:pk>", view=RecommendationDetailView.as_view(), name="redirect"),
    path('show/<uuid:uuid>', view=RedirectToOriginalView.as_view(), name='redirect_to_proposal')
]
