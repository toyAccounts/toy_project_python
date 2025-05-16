from django.shortcuts import redirect, render

from django.http import HttpRequest, HttpResponse, JsonResponse

from sub_app_1.models import Users
from sub_app_1.forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def index(request:HttpRequest):
    user = Users.objects.filter(username="admin").first()
    # user = Users.objects.get(username="admin")

    print(f"user: {user}")
    email = user.email if user else "Anonymous user"

    # if(request.user.is_authenticated is False):
    #     email = "Anonymous user"

    return render(request, "base.html", {"welcom_msg" : f"Hello {email}"})


# def index(request:HttpRequest):
#     return HttpResponse("Hello, django")

def redirect_index(request:HttpRequest):
    # path의 name
    return redirect("index")


# postman 사용시 csrf 해제
# @csrf_exempt 
def get_user(request:HttpRequest, user_id:int):
    # pathvariable
    print(user_id)
    
    if (request.method == "GET"):
        #querystring
        name = request.GET.get("name")
        print(name)

    return JsonResponse(data=dict(user_id=user_id,
                             name=name),
                        json_dumps_params={"ensure_ascii": False})


def register(request:HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        msg = "올바르지 않은 데이터 입니다."
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            msg = "회원가입완료"
        return render(request, "register.html", {"form": form, "msg": msg})
    else:
        form = RegisterForm()
        return render(request, "register.html", {"form": form})





def login_view(request:HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        msg = "가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        print(form.is_valid)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                msg = "로그인 성공"
                login(request, user)
        return render(request, "login.html", {"form": form, "msg": msg})
    else:
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})


def logout_view(request:HttpRequest):
    logout(request)
    return redirect("index")



@login_required
def list_view(request:HttpRequest):
    page = int(request.GET.get("p", 1)) # query string
    users = Users.objects.all().order_by("-id") # -: 내림차순, +: 오름차순 (생략)
    paginator = Paginator(users, 10) # 페이지당 보여지는 개수
    users = paginator.get_page(page)

    return render(request, "boards.html", {"users": users})