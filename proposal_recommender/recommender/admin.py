from django.contrib import admin
from recommender.models import Recommendation, RecommendationForCandidate
from recommender.celery import send_mails_to


def send_recommendations(modeladmin, request, queryset):
    for rec in queryset:
        send_mails_to(rec)
send_recommendations.short_description = "Mandar las recomendaciones"

class RecommendationAdmin(admin.ModelAdmin):
    actions = [send_recommendations]


admin.site.register(Recommendation, RecommendationAdmin)


class RecommendationForCandidateAdmin(admin.ModelAdmin):
    pass

admin.site.register(RecommendationForCandidate, RecommendationForCandidateAdmin)
