from django.contrib import admin
from .models import *
from .models import ProjectGalleryImage



@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(PropertySubCategory)
class PropertySubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(BuyerIntent)
class BuyerIntentAdmin(admin.ModelAdmin):
    list_display = ('intent',)
    search_fields = ('intent',)
    list_filter = ('intent',)


@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('stage',)
    search_fields = ('stage',)
    list_filter = ('stage',)

@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
    def icon_preview(self, obj):
        if obj.icon:
            return f'<img src="{obj.icon.url}" width="50" height="50" style="object-fit: contain;" />'
        return "-"
    icon_preview.allow_tags = True
    icon_preview.short_description = "Icon"

# Register Configuration model
@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('c_name',)
    search_fields = ('c_name',)
    
@admin.register(Floor_Plan)
class FloorPlanAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ProjectGalleryImageInline(admin.TabularInline):  
    model = ProjectGalleryImage
    extra = 5
    fields = ['image', 'image_tag']
    readonly_fields = ['image_tag']

@admin.register(City_seher)
class City_SeherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    
@admin.register(Project_Brand)
class Project_BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    inlines = [ProjectGalleryImageInline]  # ✅ Added inline support
    list_display = ('Title', 'City','Price', 'category', 'subcategory',  'stage')
    list_filter = ('category','City', 'subcategory', 'buyer_intent', 'stage', 'is_featured', 'project_type')
    search_fields = ('Title', 'City', 'RERA_No')
    raw_id_fields = ('Project_Location',)
    
    filter_horizontal = ('Amenities',)  # 💡 This gives a dual box select (not checkboxes)

    # To make it checkboxes instead, override formfield
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name in ['Amenities', 'Configuration', 'floor_plans']:
            kwargs['widget'] = admin.widgets.FilteredSelectMultiple(
                verbose_name=db_field.verbose_name,
                is_stacked=False
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
@admin.register(project_enquiry)
class ProjectEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'mobile', 'project')
    list_filter = ('project__Title', 'city')
    search_fields = ('name', 'email', 'mobile','project__Title')

    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')
    search_fields = ('name', 'designation')

@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile')
    search_fields = ('name', 'email', 'mobile')

