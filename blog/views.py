from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render, Http404
from django.utils import timezone
# Create your views here.
from .models import Post
from .forms import TestForm, PostModelForm


def formset_view(request):
    if request.user.is_authenticated():
        PostModelFormset = modelformset_factory(Post, form=PostModelForm)
        formset = PostModelFormset(request.POST or None,
                queryset=Post.objects.filter(user=request.user))
        if formset.is_valid():
            #formset.save(commit=False)
            for form in formset:
                print(form.cleaned_data)
                obj = form.save(commit=False)
                if form.cleaned_data:
                    #obj.title = "This title %s" %(obj.id)
                    if not form.cleaned_data.get("publish"):
                        obj.publish = timezone.now()
                    obj.save()
            # return redirect("/")
                #print(form.cleaned_data)
        context = {
            "formset": formset
        }
        return render(request, "formset_view.html", context)
    else:
        raise Http404


# def formset_view(request):
#     TestFormset = formset_factory(TestForm, extra=2)
#     formset = TestFormset(request.POST or None)
#     if formset.is_valid():
#         for form in formset:
#             print(form.cleaned_data)
#     context = {
#         "formset": formset
#     }
#     return render(request, "formset_view.html", context)





def home(request):
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        print(obj.title)
        obj.title = "Some random title"
        obj.publish = timezone.now()
        obj.save()
    if form.has_error:
        # print(form.errors.as_json())
        # print(form.errors.as_text())
        data = form.errors.iteritems()
        for key,value in data:
            #print(dir(value))
            error_str = "{field}: {error}".format(
                    field=key,
                    error=value.as_text()
                    )
            print(error_str)
        #print(form.non_field_errors())
    # initial_dict = {
    #     #"some_text": "Text",
    #     "boolean": True,
    #     # "integer": "123"
    # }
    # form = TestForm(request.POST or None, initial=initial_dict)
    # if form.is_valid():
    #     print(form.cleaned_data)
    #     print(form.cleaned_data.get("some_text"))
    #     print(form.cleaned_data.get("email"))
    #     print(form.cleaned_data.get("email2"))

    # if request.method == "POST":
    #     form = TestForm(data=request.POST)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    #         print(form.cleaned_data.get("some_text"))
    #     #print(request.POST)
    #     #print(request.POST.get("username")) #None
    #     #print(request.POST["username2"]) #Raise error
    # elif request.method == "GET":
    #     form = TestForm(user=request.user)
    #     print(request.GET)

    return render(request, "forms.html", {"form": form})




