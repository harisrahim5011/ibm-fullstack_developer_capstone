from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
# Inline for CarModel to display it inside the CarMake admin
class CarModelInline(admin.TabularInline):  # Or admin.StackedInline if you prefer a stacked layout
    model = CarModel
    extra = 1  # Number of empty forms to display in the admin
    fields = ( 'name', 'type', 'year',)  # You can choose which fields to display

# Custom admin for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'car_make', 'type', 'year')  # Fields to display in the list view
    search_fields = ('name', 'car_make__name')  # Enable search on car make name and model name
    list_filter = ('car_make', 'type', 'year')  # Enable filtering by these fields
    ordering = ('year',)  # Default ordering (by year)

# Custom admin for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Display the make name and description in the list view
    search_fields = ('name',)  # Search by make name
    inlines = [CarModelInline]  # Include CarModelInline inside CarMake

# Register the models with the respective admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
