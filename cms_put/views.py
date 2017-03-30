from django.shortcuts import render
from cms_put.models import Pages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def show(request):
    content = Pages.objects.all()
    response = "Contenido de la base de datos:<br>"
    for entry in content:
        response = response + entry.name + " => " + entry.page + "<br>"
    return HttpResponse(response)


@csrf_exempt
def entry(request, identifier):
    if request.method == "POST":
        content = Pages(name=request.POST['nombre'],
                        page=request.POST['pagina'])
        content.save()
    elif request.method == "PUT":
        # Form of data in the body: name='<nombre>'&page='<pagina>'
        body = request.body.decode('utf-8')
        [parsed_name, parsed_page] = body.split("&")
        content = Pages(id=identifier, name=parsed_name, page=parsed_page)
        content.save()
    try:
        entry = Pages.objects.get(id=identifier)
        response = "La pagina solicitada es:" + "<br>" + entry.name + \
                   " => " + entry.page
    except Pages.DoesNotExist:
        response = "No existe en la base de datos. Creala:<br><br>"
        response += "<form action='' method = 'POST'>" + \
                    "Nombre:<br> <input type='text' name='nombre'><br>" + \
                    "Pagina:<br> <input type='text' name='pagina'><br><br>" + \
                    "<input type='submit' value='Enviar'>"
    return HttpResponse(response)


def error(request):
    response = "La pagina solicitada no se encuentra disponible"
    return HttpResponse(response)
