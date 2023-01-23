
from unicodedata import name
from django.shortcuts import render,redirect

# Create your views here.
from myapp.forms import BookForm,BookModelForm,RegistrationForm,LoginForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout

from django.views.generic import View,ListView,DetailView,CreateView,UpdateView
from myapp.models import books,Books
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Signin required")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(signin_required,name="dispatch")
class BookCreateView(CreateView):
    model=Books
    form_class=BookModelForm
    template_name: str="addbook.html"
    success_url=reverse_lazy("book-list")
    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,"Book has been Created")
        return super().form_valid(form)


    # def get(self,request,*args, **kwargs):
    #     # form=BookForm()
    #     form=BookModelForm()
    #     return render(request,"addbook.html",{"form":form})

    # def post(self,request,*args, **kwargs):
    #     # form=BookForm(request.POST)
    #     form=BookModelForm(request.POST)
    #     if form.is_valid():
    #         form.instance.author=request.user   #
    #         form.save()
    #         messages.success(request,"Book has Created Successfully")

            # last_bookid=books[-1].get("id")
            # id=last_bookid+1
            # form.cleaned_data["id"]=id
            # books.append(form.cleaned_data)
            # print(books)
            # bname=form.cleaned_data.get("name")
            # bauthor=form.cleaned_data.get("author")                        #normal Form
            # bprice=form.cleaned_data.get("price")
            # Books.objects.create(name=bname,author=bauthor,price=bprice)
            
            # return render(request,"addbook.html")

        #     return redirect("book-list")
        # else:
        #     messages.error(request,"Failed to Create")
        #     return render(request,"addbook.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class BookListView(ListView):
    model=Books
    context_object_name="books"
    template_name="book-list.html"
    def get_queryset(self):
        return Books.objects.filter(author=self.request.user)

    # def get(self,request,*args,**kwargs):

    #     # all_books=books

    #     ls=Books.objects.filter(author=request.user)
    #     return render(request,"book-list.html",{"books":ls})

@method_decorator(signin_required,name="dispatch")
class BookDetailView(DetailView):
    model=Books
    context_object_name: str="book"
    template_name: str="book-detail.html"
    pk_url_kwarg: str="id"

    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")

        # book=[book for book in books if book.get("id")==id].pop()

        # dt=Books.objects.filter(id=id)[0]
        # return render(request,"book-detail.html",{"book":dt})

@method_decorator(signin_required,name="dispatch")
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        # book=[book for book in books if book.get("id")==id].pop()
        de=Books.objects.filter(id=id).delete()
        # books.remove(book)
        return redirect("book-list")

@method_decorator(signin_required,name="dispatch")
class BookEditView(UpdateView):
    model=Books
    form_class=BookModelForm
    template_name: str="book-update.html"
    pk_url_kwarg: str="id"
    success_url=reverse_lazy("book-list")
    def form_valid(self, form):
        messages.success(self.request,"Book Changed")
        return super().form_valid(form)
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     book=Books.objects.get(id=id)
    #     form=BookModelForm(instance=book)
    #     return render(request,"book-update.html",{"form":form})

        # book=[book for book in books if book.get("id")==id].pop()
        # book=Books.objects.filter(id=id).values()[0]
        # form=BookForm(initial=book)
        
    # def post(self,request,*args,**kwargs):
    #     # form=BookForm(request.POST)
    #     form=BookModelForm(request.POST)
    #     # if form.is_valid():
    #     id=kwargs.get("id")
    #     book=Books.objects.get(id=id)
    #     form=BookModelForm(request.POST,instance=book)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"Book has Been Updated Successfully")
    #         return redirect("book-list")
    #     else:
    #         messages.error(request,"Failed To Update")
    #         return render(request,"book-update.html",{"form":form})

            # data=form.cleaned_data
            # book=[book for book in books if book.get("id")==id].pop()
            # book.update(data)                                                    #normal Form
            # Books.objects.filter(id=id).update(**form.cleaned_data)
        


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"registration.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            User.objects.create_user(**form.cleaned_data)
            # messages.success(request,"Registration Successful")
            return redirect("signin")
        else:
            messages.error(request,"Failed to Register")
            return render(request,"registration.html",{"form":form})


class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                return redirect("book-list")
            else:
                messages.error(request,"invalid credentials")
                return render(request,"login.html",{"form":form})

@signin_required
def signout(request,*args,**kwargs):
    logout(request)
    return redirect("signin")


