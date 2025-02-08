from django.contrib import admin
from .models import CarMake, CarModel


# CarModelInline class to display CarModel within CarMake admin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
    fields = (
        'name',
        'type',
        'year',
    )


# Custom admin for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'car_make',
        'type',
        'year'
    )
    search_fields = (
        'name',
        'car_make__name',
    )
    list_filter = (
        'car_make',
        'type',
        'year',
    )
    ordering = ('year',)


# Custom admin for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
    )
    search_fields = ('name',)
    inlines = [CarModelInline]


# Register models with their respective admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
