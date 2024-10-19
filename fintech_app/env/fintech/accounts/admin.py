from django.contrib import admin
from .models import SavingsGroup, Contribution, FinancialLiteracyResource, Article, Video, Quiz, Question

admin.site.register(SavingsGroup)
admin.site.register(Contribution)
admin.site.register(FinancialLiteracyResource)
admin.site.register(Article)
admin.site.register(Video)
admin.site.register(Quiz)
admin.site.register(Question)
