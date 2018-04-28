from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from cms.models import Pages


def login_view(request):
    if request.user.is_authenticated():
        return ("<p>Hi," + request.user.username +
                " <a href=/logout>logout</a></p>")
    else:
        return ("<p>Not logged in: <a href=/login>login</a></p>")


def main(request):
    resp = login_view(request)
    resp += "<p><a href=/annotated>cms_templates</a></p>"
    resp += "Available pages: "
    pages = Pages.objects.all()
    for page in pages:
        resp += "<br><a href=/" + page.name + ">" + page.name + "</a>"
    return HttpResponse(resp)


@csrf_exempt
def get_page(request, req_name):
    if request.method == "PUT":
        if request.user.is_authenticated():
            Pages(name=req_name, page=request.body).save()
            return HttpResponse("Page submitted.<br><br><a href=/>Home</a>")
        else:
            return HttpResponseNotFound("<h1>Login to add pages. "
                                        "<a href=/login>login</a></h1>")
    else:
        try:
            req_page = login_view(request)
            req_page += Pages.objects.get(name=req_name).page
            if request.method == "GET":
                return HttpResponse(req_page)
            else:
                return HttpResponseNotAllowed("['GET', 'PUT']",
                                              "<h1>405 Not Allowed</h1>")
        except Pages.DoesNotExist:
                return HttpResponseNotFound("<h1>Page does not exist.</h1>")


def ann_main(request):
    Pages_list = {'Pages_list': Pages.objects.all()}
    return render(request, 'home.html', Pages_list)


def ann_get_page(request, req_name):
    if request.method == "GET":
        try:
            content = {'content': Pages.objects.get(name=req_name)}
            return render(request, 'page.html', content)
        except Pages.DoesNotExist:
                return HttpResponseNotFound("<h1>Page does not exist.</h1>")
    else:
        return HttpResponseNotAllowed("['GET']", "<h1>405 Not Allowed</h1>")
