from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
import sweetify
import requests


def index(request):
    featured_proj = Projects.objects.filter(is_featured=True)
    under_cons_proj = Projects.objects.filter(stage__stage__iexact='Under Construction')
    testi = Testimonial.objects.all()

    # Grouping projects by city
    cities = City_seher.objects.all()
    city_projects = {}

    for city in cities:
        projects = Projects.objects.filter(City=city)
        if projects.exists():
            city_projects[city] = projects

    return render(request, 'Estateapp/index.html', {'featured_proj': featured_proj,'under_cons_proj': under_cons_proj,'city_projects': city_projects, 'testi': testi})

def aboutus(request):
    return render(request, 'Estateapp/aboutus.html')


def projects(request):
    proj = Projects.objects.select_related(
        'category', 'subcategory', 'buyer_intent', 'stage', 'project_type', 'Project_Location'
    ).prefetch_related(
        'Configuration', 'floor_plans', 'Amenities'
    ).all()

    featured_proj = Projects.objects.filter(is_featured=True)
    locations = Location.objects.all()
    brands = Project_Brand.objects.all()
    stages = ProjectStage.objects.all()

    # ✅ Debug prints
    print("Locations:")
    for loc in locations:
        print(f" - ID: {loc.id}, Name: {loc.name}")

    print("Brands:")
    for brand in brands:
        print(f" - ID: {brand.id}, Name: {brand.name}")

    print("Stages:")
    for stage in stages:
        print(f" - ID: {stage.id}, Name: {stage.stage}")

    return render(
        request,
        'Estateapp/all-projects.html',
        {
            'proj': proj,
            'featured_proj': featured_proj,
            'locations': locations,
            'brands': brands,
            'stages': stages,
        }
    )


def filter_projects(request):
    projects = Projects.objects.all()

    brand = request.GET.get('brand')
    location = request.GET.get('location')
    stage = request.GET.get('stage')
    price_range = request.GET.get('price_range')

    print("\n🔍 Initial total projects:", projects.count())

    if brand:
        print(f"📦 Filtering by brand ID: {brand}")
        projects = projects.filter(projectbrand__id=brand)

    if location:
        print(f"📍 Filtering by location ID: {location}")
        projects = projects.filter(Project_Location__id=location)

    if stage:
        print(f"🏗 Filtering by stage ID: {stage}")
        projects = projects.filter(stage__id=stage)

    print(f"🧮 Projects after brand/location/stage filters: {projects.count()}")

    # ✅ Print projects if location and stage are selected
    if location and stage:
        print(f"\n📍 Location ID: {location}, 🏗 Stage ID: {stage}")
        print("Filtered Projects based on Location & Stage:")
        for project in projects:
            print(f" - ID: {project.id}, Name: {project.Title}, Price: {project.Price}")

    if price_range:
        min_price, max_price = map(int, price_range.split('-'))

        import re

        def parse_price(p):
            if not p:
                raise ValueError("Price is empty")

            # Remove ₹, commas, and asterisk
            p = p.upper().replace("₹", "").replace(",", "").replace("*", "").strip()

            # Match float or int followed by unit
            match = re.match(r'([\d.]+)\s*(CR|CRORE|LAKH|LAKHS|LAC|LACS|L)?', p)
            if not match:
                raise ValueError(f"Invalid price format: {p}")

            number, unit = match.groups()
            number = float(number)

            if unit in ["CR", "CRORE"]:
                return number * 1e7
            elif unit in ["LAKH", "LAKHS", "LAC", "LACS"]:
                return number * 1e5
            else:
                return number  # Assume already in raw rupees

        filtered = []
        for project in projects:
            try:
                print(f"Checking project {project.id} - Raw Price: {project.Price}")
                price = parse_price(project.Price)
                print(f"Parsed Price: {price}")
                if min_price <= price <= max_price:
                    print(f"✅ Match: Project {project.id}")
                    filtered.append(project.id)
                else:
                    print(f"❌ Out of range: {price}")
            except Exception as e:
                print(f"⚠ Error parsing price for project {project.id}: {e}")

        projects = projects.filter(id__in=filtered)
        print(f"🔎 Final filtered count after price: {projects.count()}")

    context = {
        'projects': projects,
        'brands': Project_Brand.objects.all(),
        'locations': Location.objects.all(),
        'stages': ProjectStage.objects.all(),
    }

    return render(request, 'Estateapp/result.html', context)



class ProjectDetailView(View):
    def get(self, request, slug):
        projj = get_object_or_404(Projects, project_slug=slug)
        amenities = projj.Amenities.all()
        floor_plans = projj.floor_plans.all()
        configuration = projj.Configuration.all()
        return render(request, 'Estateapp/projectdetail.html', {
            'projj': projj,
            'amenities': amenities,
            'floor_plans': floor_plans,
            'configuration': configuration
        })

    def post(self, request, slug):
        projj = get_object_or_404(Projects, project_slug=slug)
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')

        if name and email and city and mobile:
            project_enquiry.objects.create(
                project=projj,
                name=name,
                email=email,
                city=city,
                mobile=mobile
            )
            sweetify.success(request, 'Enquiry Submitted!', text='We will contact you shortly.', timer=3000)
            # ✅ Redirect to thankyou page with project slug
            return redirect(reverse('thankyou', kwargs={'slug': projj.project_slug}))
        else:
            sweetify.error(request, 'Form Incomplete', text='Please fill all the fields.', timer=3000)
            return redirect(request.path_info)
        
class ThankYouView(View):
    def get(self, request, slug):
        project = get_object_or_404(Projects, project_slug=slug)
        return render(request, 'Estateapp/thankyou.html', {'project': project})

def readytomove(request):
    ready_proj = Projects.objects.filter(stage__stage__iexact='Ready to Move')
    return render(request, 'Estateapp/ready-to-move.html', {'ready_proj': ready_proj})

def underconstruction(request):
    undr_cons = Projects.objects.filter(stage__stage__iexact='Under Construction')
    return render(request, 'Estateapp/under-construction.html',{'undr_cons':undr_cons})

def newlaunch(request):
    new_launch_proj = Projects.objects.filter(stage__stage__iexact='New Launches')
    return render(request, 'Estateapp/new-launch.html', {'new_launch_proj':new_launch_proj})

def location(request):
    cities = City_seher.objects.all()
    featured_proj = Projects.objects.filter(is_featured=True)
    return render(request, 'Estateapp/location.html', {'cities': cities, 'featured_proj': featured_proj})

def location_projects(request, city_slug):
    city = get_object_or_404(City_seher, city_slug=city_slug)
    projects = Projects.objects.filter(City=city)
    ready_proj = Projects.objects.filter(City=city, stage__stage__iexact="Ready to Move")
    newlaunch_proj = Projects.objects.filter(City=city, stage__stage__iexact="New Launches")
    return render(request, 'Estateapp/location_projects.html', {'city': city, 'projects': projects, 'ready_proj':ready_proj, 'newlaunch_proj':newlaunch_proj})


def blogs(request):
    blg = Blogs.objects.all()
    return render(request, 'Estateapp/blogs.html', {'blg': blg})


class BlogdetailView(View):
    def get(self, request, slug):
        blgg = Blogs.objects.get(blogslug=slug)
        return render(request, 'Estateapp/blogdetails.html', {'blgg': blgg})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        message = request.POST.get('message')

        # Save the contact form data
        Contact.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            message=message
        )

        # Sweetify success message
        sweetify.success(request, 'Thank you!', text='Your message has been received.', timer=3000)

        # Redirect back to the same page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'Estateapp/contact.html')

def cities(request):
    return render(request, 'Estateapp/city.html')

def luxury(request):
    lux = Projects.objects.filter(project_type__name__iexact="Luxury")
    return render(request, 'Estateapp/luxury.html', {'lux': lux})


def ultraluxury(request):
    ultra = Projects.objects.filter(project_type__name__iexact="Ultra Luxury")
    return render(request, 'Estateapp/ultraluxury.html', {'ultra': ultra})

def premium(request):
    preem = Projects.objects.filter(project_type__name__iexact="Premium")
    return render(request, 'Estateapp/premium.html', {'preem': preem})
    
def converter(request):
    return render(request, 'Estateapp/converter.html')


def privacypolicy(request):
    return render(request, 'Estateapp/privacy.html')

def citypage(request):
    return render(request, 'Estateapp/cityPage.html')



def convert_units(request):
    result = None

    if request.method == 'POST':
        value = float(request.POST.get('value', 0))
        from_unit = request.POST.get('from_unit')
        to_unit = request.POST.get('to_unit')

        conversions = {
            ('acre', 'bigha'): 1.613,
            ('acre', 'hectare'): 0.404686,
            ('acre', 'sqfeet'): 43560,
            ('acre', 'sqm'): 4046.86,

            ('bigha', 'acre'): 0.6198,
            ('bigha', 'hectare'): 0.25,

            ('cent', 'sqfeet'): 435.6,
            ('cent', 'sqm'): 40.4686,

            ('cm', 'mm'): 10,
            ('cm', 'inches'): 0.3937,

            ('ft', 'cm'): 30.48,
            ('ft', 'inches'): 12,
            ('ft', 'mm'): 304.8,
            ('ft', 'meter'): 0.3048,

            ('hectare', 'acre'): 2.47105,
            ('hectare', 'bigha'): 4.0,
            ('hectare', 'sqfeet'): 107639,

            ('inches', 'cm'): 2.54,
            ('inches', 'mm'): 25.4,

            ('meter', 'cm'): 100,
            ('meter', 'ft'): 3.28084,
            ('meter', 'inches'): 39.37,
            ('meter', 'mm'): 1000,

            ('sqfeet', 'acre'): 2.2957e-5,
            ('sqfeet', 'sqm'): 0.092903,

            # New conversions added 👇
            ('km', 'meter'): 1000,
            ('meter', 'km'): 0.001,
            ('mile', 'km'): 1.60934,
            ('km', 'mile'): 0.621371,
            ('sqmeter', 'sqfeet'): 10.7639,
            ('sqkm', 'acre'): 247.105,
            ('sqmile', 'sqkm'): 2.58999,
            ('guntha', 'sqfeet'): 1089,
            ('kanal', 'sqfeet'): 5445,
            ('marla', 'sqfeet'): 272.25,
            ('yard', 'meter'): 0.9144,
            ('yard', 'feet'): 3,
        }

        key = (from_unit.lower(), to_unit.lower())
        if key in conversions:
            result = value * conversions[key]
        else:
            result = "Conversion not available"

    return render(request, 'conversion.html', {'result': result})

