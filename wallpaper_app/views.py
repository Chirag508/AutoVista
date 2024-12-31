from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.http import FileResponse,HttpResponse
from django.core.paginator import Paginator
from .models import Blog, Wallpaper, Category, Sub_category

import requests
import datetime
# Create your views here.
def show_welcome_page(request):
    return render(request,'welcome.html')

def show_home_page(request):
    return render(request,'home.html')

def show_base_page(request):
    return render(request,'base.html')

def show_about_page(request):
    return render(request,'about_us.html')

def show_contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        #date and time
        x = datetime.datetime.now()
        Date = f'{x.day}/{x.month}/{x.year}'
        Time = f'{x.strftime("%I:%M:%S %p")}'
        Day = x.strftime("%A")

        # Send email
        email_subject = f'Contact Us(AutoVista - Premium Automotive Wallpapers)'
        email_message = f'Someone just filled your contact us form check out.....\nHis details are as below...\n\nTime: {Time}\nDay: {Day}\nDate: {Date}\n\nName: {name}\n\nPhone: {phone}\nEmail: {email}\n\nSubject: {subject}\nMessage: {message}\n\n....'
        
        try:
            send_mail(
                email_subject,
                email_message,
                email,  # From email
                ['chiragpanchal143143@gmail.com'],  # Your email address
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except:
            messages.error(request, 'An error occurred. Please try again later.')
        
        return redirect('contact')
    return render(request,'contact_us.html')

def blog_list(request):
    blog_list = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blog_list, 9)  # Show 9 blogs per page
    
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    return render(request, 'blogs.html', {'blogs': blogs})

def blog_detail_page(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    image_url = blog.image.url.replace("http://", "https://")
    return render(request, 'blog_detail.html', {'blog': blog,'image_url': image_url})

def wallpaper_list(request):
    wallpapers = Wallpaper.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        wallpapers = wallpapers.filter(category=category)
    
    # Filter by subcategory
    subcategory_slug = request.GET.get('subcategory')
    if subcategory_slug:
        subcategory = get_object_or_404(Sub_category, slug=subcategory_slug)
        wallpapers = wallpapers.filter(sub_category=subcategory)
    
    # Pagination
    paginator = Paginator(wallpapers, 12)  # Show 12 wallpapers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request,'wallpaper_list.html', context)

def wallpaper_detail(request, id):
    wallpaper = get_object_or_404(Wallpaper, id=id)
    related_wallpapers = Wallpaper.objects.filter(category=wallpaper.category).exclude(id=wallpaper.id)[:6]
    image_url = wallpaper.image.url.replace("http://", "https://")
    context = {
        'wallpaper': wallpaper,
        'related_wallpapers': related_wallpapers,
        'image_url': image_url
    }
    return render(request,'wallpaper_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request,'category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = Sub_category.objects.filter(category=category)
    wallpapers = Wallpaper.objects.filter(category=category)
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'wallpapers': wallpapers,
    }
    return render(request,'category_detail.html', context)

def increment_download(request, id):
    wallpaper = get_object_or_404(Wallpaper, id=id)
    wallpaper.downloads += 1
    wallpaper.save()
    # Fetch the image from Cloudinary URL
    image_url = wallpaper.image.url
    response = requests.get(image_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Generate a custom filename using the wallpaper's title
        custom_filename = f"{wallpaper.title.replace(' ', '_')}.jpg"  # Replace spaces with underscores
        # Prepare the response with the image content
        http_response = HttpResponse(response.content, content_type='image/jpeg')
        http_response['Content-Disposition'] = f'attachment; filename={custom_filename}'
        return http_response
    else:
        # Handle case if image download fails
        return HttpResponse("Error downloading the image", status=500)