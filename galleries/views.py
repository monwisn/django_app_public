from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _

from galleries.models import Gallery, Photo, Status
from galleries.forms import GalleryForm, PhotoForm
from plants_app.config import pagination


@login_required(login_url='/authentication/login')
def add_gallery(request):
    if request.method == "POST":
        form = GalleryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            if Gallery.objects.filter(title=instance.title).exists():
                messages.error(request, 'A gallery with this name already exists, please choose a different name.')
            else:
                instance.save()
                messages.success(request, 'Your gallery has been created successfully.')
        else:
            messages.error(request, f'Something went wrong!\n\n {form.errors}')
        return redirect('galleries:add_gallery')

    else:
        form = GalleryForm()
    return render(request, "galleries/add_gallery.html", {"form": form})


@login_required(login_url='/authentication/login')
def galleries_list(request):
    gallery = Gallery.objects.filter(author=request.user)
    # gallery = Gallery.objects.filter(author=request.user).filter(status=Status.PUBLISHED)
    # gallery = Gallery.objects.filter(status=Status.PUBLISHED).annotate(p_count=Count("photos")).filter(p_count__gt=0)
    pages = pagination(request, gallery, 5)

    return render(request, "galleries/list_galleries.html", {"gallery": pages, 'page_obj': pages})


@login_required(login_url='/authentication/login')
def galleries_list_view(request):
    galleries = Gallery.objects.filter(author=request.user).filter(status=Status.PUBLISHED).annotate(
        p_count=Count("photos")).filter(p_count__gt=0)
    # galleries = Gallery.objects.filter(author=request.user).filter(status=Status.PUBLISHED).annotate(
    #     p_count=Count("photos")).filter(p_count__gt=0)
    pages = pagination(request, galleries, 4)

    return render(request, 'galleries/galleries_list_view.html', {'galleries': pages, 'page_obj': pages})


@login_required(login_url='/authentication/login')
def gallery_details(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)

    return render(request, "galleries/gallery_details.html", {"gallery": gallery})


@login_required(login_url='/authentication/login')
def gallery_edit(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk, author_id=request.user)

    if request.method == 'POST':
        form = GalleryForm(request.POST, instance=gallery)

        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery has been updated.')
            return redirect('galleries:list')
    else:
        form = GalleryForm(instance=gallery)

    return render(request, 'galleries/add_gallery.html', {'form': form, 'gallery': gallery})


@login_required(login_url='/authentication/login')
def gallery_delete(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    if request.method == 'POST':
        gallery.delete()
        messages.success(request, 'Gallery has been deleted.')
        return redirect('galleries:list')

    return render(request, 'galleries/gallery_delete.html', {'gallery': gallery})


@staff_member_required
def galleries_list_admin(request):
    galleries = Gallery.objects.all()
    pages = pagination(request, galleries, 15)

    context = {'galleries_list_admin': galleries,
               'page_obj': pages}
    return render(request, 'galleries/galleries_list_admin.html', context)


@login_required(login_url='/authentication/login')
def add_photos(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)
    PhotosFormSet = modelformset_factory(Photo, form=PhotoForm, extra=1)
    formset = PhotosFormSet(queryset=gallery.photos.none())
    form = PhotoForm()
    if request.method == "POST":
        formset = PhotosFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for f in formset.cleaned_data:
                if f:
                    Photo.objects.create(gallery=gallery, **f)
        messages.success(request, "Your photos have been successfully added to the gallery!")
        return HttpResponseRedirect(reverse("galleries:details", args=[gallery_id]))

    return render(request, "galleries/add_photos.html", {"formset": formset, "gallery": gallery, 'form': form})


@login_required(login_url='/authentication/login')
def photos_view(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)
    # photos = Photo.objects.filter(gallery__author=request.user)

    return render(request, "galleries/photos_view.html", {"gallery": gallery})


@login_required(login_url='/authentication/login')
def photo_edit(request, pk):
    photo = Photo()
    photo_form = PhotoForm(instance=photo)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES or None)

        if form.is_valid():
            for f in photo_form:
                f = form.save(commit=False)
                f.save()
                print(form.cleaned_data)
            # form.save()
            messages.success(request, 'Photo details have been updated!')
            return redirect('galleries:list')

    return render(request, 'galleries/add_photos.html', {'form': form})


@login_required(login_url='/authentication/login')
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        photo.delete()
        messages.success(request, f'Photo has been successfully deleted from "{photo.gallery.title}" gallery.')
        return redirect('galleries:list')

    return render(request, 'galleries/photo_delete.html', {'photo': photo})
