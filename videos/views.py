from django.http import HttpResponse
from django.shortcuts import render
from .forms import  VideoUploadForm
# Create your views here.
from django.shortcuts import render
from .models import Video

from django.shortcuts import render
from django.conf import settings
from .models import Video  # Assuming your Video model is in the same app

def homepage(request):
    # Fetch the latest video based on the 'upload_date' field
    latest_video = Video.objects.order_by('-upload_date').first()

    context = {
        'latest_video': latest_video,
    }

    return render(request, 'videos/homepage.html', context)


def video_list(request):
    videos = Video.objects.all()
    return render(request, 'videos/video_list.html', {'videos': videos})

# Add more views as needed


from django.shortcuts import render, get_object_or_404, redirect
from .models import Video, CommentRating
from .forms import CommentRatingForm

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    form = CommentRatingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment_rating = form.save(commit=False)
        comment_rating.video = video
        comment_rating.user = request.user
        comment_rating.save()
        return redirect('video_detail', pk=pk)

    context = {
        'video': video,
        'form': form,
    }
    return render(request, 'videos/video_detail.html', context)

from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VideoUploadForm

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the user from the request
            user = request.user
            # Check if the user exists in the database
            if user.is_authenticated:
                # Save the video object
                video = form.save(commit=False)
                video.uploaded_by = user
                video.save()
                return redirect('video_detail', pk=video.pk)
            else:
                # User is not authenticated
                return HttpResponse("You are not authorized to upload videos.")
        else:
            return HttpResponse("Invalid form data.")
    else:
        form = VideoUploadForm()
    return render(request, 'videos/video_upload.html', {'form': form})

def upload_video_success(request):
    return render(request, 'upload_video_success.html')


from django.shortcuts import render, get_object_or_404, redirect
from .forms import VideoUploadForm
from .models import Video

def modify_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VideoUploadForm(instance=video)
    return render(request, 'videos/modify_video.html', {'form': form, 'video': video})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Video

def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.delete()
    return redirect('dashboard')