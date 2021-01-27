from django.contrib import admin
from recommender.models import Recommendation, RecommendationForCandidate


class RecommendationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recommendation, RecommendationAdmin)


class RecommendationForCandidateAdmin(admin.ModelAdmin):
    pass

admin.site.register(RecommendationForCandidate, RecommendationForCandidateAdmin)


from htmlemailer import send_mail

send_mail(
	"emails/mail",
	"My Site <mysite@example.org>",
	["you@recipient.com"],
	{
		"my_message": "Hello & good day to you!"
	})
