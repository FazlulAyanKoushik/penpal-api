from django.contrib import admin
from document.models import Document

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'document_type', 'status', 'created_at', 'updated_at')
    list_filter = ('document_type', 'status', 'author')
    search_fields = ('title', 'description', 'content')
    ordering = ('-updated_at',)


admin.site.register(Document, DocumentAdmin)
