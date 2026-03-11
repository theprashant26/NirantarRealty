from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from django.utils.html import format_html
from django.utils.text import slugify



# Main Category Model
class PropertyCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

# Sub Category Model (e.g., Villas, Retail Shops)
class PropertySubCategory(models.Model):
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

# Buyer Intent (e.g., End Users, Investors)
class BuyerIntent(models.Model):
    intent = models.CharField(max_length=100)

    def __str__(self):
        return self.intent

# Project Stage (e.g., New Launches, Under Construction, Ready to Move)
class ProjectStage(models.Model):
    stage = models.CharField(max_length=100)

    def __str__(self):
        return self.stage
    
# Project Type (e.g., Luxury, Ultra Luxury, Premium)
class ProjectType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Configuration(models.Model):
    c_name = models.CharField(max_length=50)  # e.g., "1BHK", "2BHK", "Plot"
    c_pricing = models.CharField(max_length=50, null=True, blank=True)  # e.g., "₹50L", "₹1Cr"
    c_size = models.CharField(max_length=50, null=True, blank=True)  # e.g., "1000 sqft", "2000 sqft"

    def __str__(self):
        return self.c_name


class Floor_Plan(models.Model):
    name = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='floor_plans/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='amenities/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class City_seher(models.Model):
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=500, null=True)
    descp = models.TextField(null=True)
    why_invest = models.TextField(null=True)
    image = models.ImageField(upload_to='city/', null=True)
    image2 = models.ImageField(upload_to='city/', null=True)
    city_slug = AutoSlugField(populate_from='name', unique=True)

    def save(self, *args, **kwargs):
        if not self.city_slug:
            self.city_slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# Location model
class Location(models.Model):
    name = models.CharField(max_length=200, null=True)
    city =  models.ForeignKey(City_seher, on_delete=models.CASCADE,null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    descp = models.TextField(null=True)
    image = models.ImageField(upload_to='location/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Property_Brand(models.Model):
    brand_name = models.CharField(max_length=300, null=True)
    
class Project_Brand(models.Model):
    name = models.CharField(max_length=400, null=True)
    logo = models.ImageField(upload_to='logos/', null=True)
    
    def __str__(self):
        return self.name

# Project Model
class Projects(models.Model):
    Title = models.CharField(max_length=200, null=True)
    Price = models.CharField(max_length=200, null=True)
    Size = models.CharField(max_length=200, null=True)
    Configuration = models.ManyToManyField(Configuration, blank=True)
    RERA_No = models.CharField(max_length=200, null=True)
    
    projectbrand = models.ForeignKey(Project_Brand, on_delete=models.SET_NULL, null=True, related_name='Brands')
    
    Proj_Logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    
    Bann1 = models.ImageField(upload_to='banner/', null=True)
    Bann2 = models.ImageField(upload_to='banner/', null=True)
    Bann3 = models.ImageField(upload_to='banner/', null=True)
    
    Address_line1 = models.CharField(max_length=200, null=True)
    City = models.ForeignKey(City_seher, on_delete=models.SET_NULL, null=True, related_name='projects')
    Zipcode = models.CharField(max_length=6, null=True)
    Brochure = models.FileField(upload_to='brochure/', null=True, blank=True)
    video_link = models.URLField(max_length=500, null=True, blank=True)
    
    About_Content = RichTextField(null=True, blank=True)
    
    # ✅ Changed to TextField with help_text
    Highlights = models.TextField(
        null=True, blank=True,
        help_text="Enter each highlight on a new line (no bullets or HTML needed)."
    )
    
    Featur_Content = RichTextField(null=True, blank=True)
    # Gallery = models.ImageField(upload_to='gallery/', null=True, blank=True)
    Location_Content = models.TextField(
        null=True, blank=True,
        help_text="Enter each Location highlight on a new line (no bullets or HTML needed)."
    )
    floor_plans = models.ManyToManyField(Floor_Plan, blank=True, related_name='projects')
    
    Mobile = models.CharField(max_length=10, null=True, blank=True)
    Whatsapp_no = models.CharField(max_length=10, null=True, blank=True)
    
    Map_Link = models.URLField(max_length=500, null=True, blank=True)
    
    Total_Area = models.CharField(max_length=200, null=True, blank=True)
    Possesion_Time = models.CharField(max_length=200, null=True, blank=True)
    Unit_Variants = models.CharField(max_length=200, null=True, blank=True)
    Amenities = models.ManyToManyField(Amenity, blank=True)
    Abt_builder = models.TextField(null=True)
    is_featured = models.BooleanField(default=False)

    # New relationships
    Project_Location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    project_slug = AutoSlugField(populate_from='Title', unique=True)
    category = models.ForeignKey(PropertyCategory, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(PropertySubCategory, on_delete=models.SET_NULL, null=True)
    buyer_intent = models.ForeignKey(BuyerIntent, on_delete=models.SET_NULL, null=True)
    stage = models.ForeignKey(ProjectStage, on_delete=models.SET_NULL, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, blank=True)
    
    gtm_id = models.CharField(max_length=50,null=True,blank=True,help_text="Add GTM ID like GTM-XXXXXX for this specific project")


    def __str__(self):
        return self.Title
    
    # ✅ Format highlights into styled HTML list
    def get_highlights_as_list(self):
        if not self.Highlights:
            return ""

        lines = self.Highlights.strip().splitlines()
        html_output = '<ul>'
        for line in lines:
            if line.strip():
                html_output += f'''
                <li>
                    <p class="fadeInUp" data-wow-delay=".3s">
                        <i class="fa-solid fa-circle-check"></i> {line.strip()}
                    </p>
                </li>
                '''
        html_output += '</ul>'
        return html_output
    
    def get_location_as_list(self):
        if not self.Location_Content:
            return ""

        lines = self.Location_Content.strip().splitlines()
        html_output = '<ul>'
        for line in lines:
            if line.strip():
                html_output += f'''
                <li>
                    <p class="fadeInUp" data-wow-delay=".3s">
                        <i class="fa-solid fa-circle-check"></i> {line.strip()}
                    </p>
                </li>
                '''
        html_output += '</ul>'
        return html_output
    
    

class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='gallery/')
    
    def __str__(self):
        return f"{self.project.Title} - Image"

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', self.image.url)
        return ""
    image_tag.short_description = 'Preview'
    

class project_enquiry(models.Model):
    project = models.ForeignKey('Projects', on_delete=models.CASCADE, related_name='enquiries')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.name} for {self.project.Title}"


class Testimonial(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(upload_to='testimonial/', null=True, blank=True)
    designation = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Blogs(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    banner = models.ImageField(upload_to='blog/', null=True, blank=True)
    author = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    blogslug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=10, null=True)
    message = models.TextField(null=True, blank=True)
