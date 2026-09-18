from django.contrib import admin

from .models import Family, Member


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'family_name',
        'contact_number',
        'area',
        'pin_code',
        'created_at',
    )

    search_fields = (
        'family_name',
        'contact_number',
        'area',
        'pin_code',
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'age',
        'gender',
        'relation',
        'family',
        'created_at',
    )

    search_fields = (
        'name',
        'family__family_name',
    )

    list_filter = (
        'gender',
        'relation',
    )