from django.contrib import admin
from blog.models import  Blog
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe
# Register your models here.

class BlogAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'





class BlogAdmin(admin.ModelAdmin):
    model = Blog
    list_display = ["title","created_at","get_image"]
    prepopulated_fields = {"slug":("title",)}
    form = BlogAdminForm
    readonly_fields = ("get_image",)

    def get_image(self,obj):
        return mark_safe(f"<img src='{obj.image.url}' width='100px' height='100px'>")        

    get_image.short_description = "Image"

admin.site.register(Blog,BlogAdmin)