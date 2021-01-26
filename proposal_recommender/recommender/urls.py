from django.urls import path

from proposal_recommender.recommender.views import (
    RecommendationDetailView,
)

app_name = "recommender"
urlpatterns = [
    path("<int:pk>", view=RecommendationDetailView.as_view(), name="redirect"),
]
