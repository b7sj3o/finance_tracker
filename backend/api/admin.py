from django.contrib import admin
from .models import User, Income, Expense, Category


@admin.register(Income, Expense)
class TransferingAdmin(admin.ModelAdmin):
    list_display = [
        "amount",
        "description_short",
        "category",
        "created_formatted",
        "updated_formatted",
    ]

    @admin.display(description="Description")
    def description_short(self, obj):
        return obj.description[:15] if len(obj.description) >= 15 else obj.description

    @admin.display(description="Created")
    def created_formatted(self, obj):
        return obj.created.strftime("%d:%m:%Y, %H:%M")

    @admin.display(description="Updated")
    def updated_formatted(self, obj):
        return obj.updated.strftime("%d:%m:%Y, %H:%M")


admin.site.register(User)
admin.site.register(Category)
