from django.shortcuts import render
from visualizer.infographics import InfographicGenerator

def index(request):
    """
    handle homepage routing
    """
    return render(request, 'index.html',)

def create(request):
    """
    handle create landing page routing
    """
    # generator = InfographicGenerator()
    #
    #
    #     # generator.generate_infographic(data)
    return render(request, 'create.html', {})

def create_prompt(request):
    """
    handle create from prompt page routing
    """
    if request.POST:
        prompt = request.POST['prompt']
        print('====')
        print(prompt)
        print('====')

    return render(request, 'create_prompt.html', )

def create_upload(request):
    """
    handle create from upload page routing
    """
    if request.POST:
        file = request.FILES.get('file', None)

        if file:
            file_contents = file.read()
            print('====')
            print(file_contents)
            print('====')

        else:
            print("empty file")

    return render(request, 'create_upload.html', )
