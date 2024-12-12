from django.shortcuts import render
from django.contrib import messages
from django.db import IntegrityError

from visualizer.infographics import InfographicGenerator
from visualizer.models import Prompts
from visualizer import utils

def index(request):
    """
    handle homepage routing
    """
    return render(request, 'index.html',)

def create(request):
    """
    handle create landing page routing
    """
    recent_prompts = Prompts.objects.order_by("-timestamp")[:5]

    return render(request, 'create.html', {"recent_prompts": recent_prompts})

def create_prompt(request):
    """
    handle create from prompt page routing
    """
    if request.POST:
        prompt = request.POST['prompt']

        # save prompt on submission
        try:
            prompts = Prompts(prompt=prompt)
            prompts.save()
        except IntegrityError as e:
            print(e)

        generator = InfographicGenerator()
        vid_path = generator.generate_infographic(prompt)
        utils.cleanup_dir("media")

        if vid_path is None:
            # if some error occurs, notify the user something went wrong
            messages.error(request, 'Something went wrong, Re-submit the prompt. (You can just refresh to re-submit)')
            return render(request, 'create_prompt.html')

        return render(request, 'result.html', {'vid_path': vid_path})

    return render(request, 'create_prompt.html', )

def create_upload(request):
    """
    handle create from upload page routing
    """
    if request.POST:
        file = request.FILES.get('file', None)

        if file:
            file_contents = file.read()

            generator = InfographicGenerator()
            vid_path = generator.generate_infographic(file_contents)

            if vid_path is None:
                # if some error occurs, notify the user something went wrong
                messages.error(request, 'Something went wrong, Re-submit the file. (You can just refresh to re-submit')
                return render(request, 'create_upload.html')

            print(vid_path)

            return render(request, 'result.html', {'vid_path': vid_path})
        else:
            print("empty file")

    return render(request, 'create_upload.html', )
