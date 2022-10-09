from django.contrib import admin


class TrackingModelAdmin(admin.ModelAdmin):
    readonly_fields = [
        'id',
    ]
    ordering = [
        '-created_at'
    ]

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            self.do_before_save_new_model(request, obj, form, change)

        if hasattr(obj, 'modified_by'):
            obj.modified_by = request.user

        obj.save()

    def do_before_save_new_model(self, request, obj, form, change):
        obj.created_by = request.user

    # def has_delete_permission(self, request, obj=None):
    #     return False


class StateHistoryAdminInline(admin.TabularInline):
    fields = [
        'old_value',
        'new_value',
        'note',
        'changed_at',
        'changed_by',
    ]
    autocomplete_fields = [
        'changed_by'
    ]
    extra = 0
    ordering = [
        '-id'
    ]
