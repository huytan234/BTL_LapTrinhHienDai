from django.contrib import admin
from django.template.response import TemplateResponse

from .models import User, Service, Bill, Payment, ResidentFamily, AccessCard, Apartment, Contract, TuDo, Package, Feedback, SurveyForm, \
    SurveyQuestion, SurveyResponse
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.html import mark_safe
from django.urls import path
from django.db.models import Count, Sum


class MyCourseAdminSite(admin.AdminSite):
    site_header = 'Quản lí chung cư'

    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()

    def course_stats(self, request):
        total_paid_invoices = Payment.objects.filter(status='pass').aggregate(total_paid=Count('id'))['total_paid']
        course_stats = Payment.objects.select_related('bill').prefetch_related('bill__service').all()

        return TemplateResponse(request, 'admin/stats.html', {
            'total_paid_invoices': total_paid_invoices,
            'course_stats': course_stats
        })


admin_site = MyCourseAdminSite(name='MyAdmin')


class MyUserSite(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'role']
    search_fields = ['username', 'description']


class MyServiceSite(admin.ModelAdmin):
    list_display = ['id', 'name', 'priceService']
    search_fields = ['name', 'description']


admin_site.register(User, MyUserSite)
admin_site.register(Service, MyServiceSite)
admin_site.register(Bill)
admin_site.register(Payment)
admin_site.register(ResidentFamily)
admin_site.register(AccessCard)
admin_site.register(Apartment)
admin_site.register(Contract)
admin_site.register(TuDo)
admin_site.register(Package)
admin_site.register(Feedback)
admin_site.register(SurveyForm)
admin_site.register(SurveyQuestion)
admin_site.register(SurveyResponse)


