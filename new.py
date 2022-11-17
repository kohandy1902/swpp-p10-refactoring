from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseNotFound,
    JsonResponse,
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Article, Comment
import json


def dict_to_response(dict: dict, status_code: int) -> HttpResponse:
    return HttpResponse(
        json.dumps(dict),
        content_type="application/json",
        status=status_code,
    )


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        req_data = json.loads(request.body.decode())
        username = req_data["username"]
        password = req_data["password"]
        User.objects.create_user(username=username, password=password)
        return HttpResponse(status=201)
    else:
        return HttpResponseNotAllowed(["POST"])


def signin(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        req_data = json.loads(request.body.decode())
        username = req_data["username"]
        password = req_data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponseNotAllowed(["POST"])


def signout(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse(status=204)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponseNotAllowed(["GET"])


def article_list(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        article_all_list = [
            {
                "title": article.title,
                "content": article.content,
                "author": article.author_id,
            }
            for article in Article.objects.all()
        ]
        return JsonResponse(article_all_list, safe=False)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        else:
            try:
                req_data = json.loads(request.body.decode())
                title = req_data["title"]
                content = req_data["content"]
            except (KeyError, json.JSONDecodeError) as e:
                return HttpResponseBadRequest()
            article = Article(title=title, content=content, author=request.user)
            article.save()
            response_article = {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "author": article.author.id,
            }
            return dict_to_response(response_article, 201)

    else:
        return HttpResponseNotAllowed(["GET", "POST"])


def article(request: HttpRequest, article_id: int = 0) -> HttpResponse:
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        try:
            article = Article.objects.get(id=article_id)
        except:
            return HttpResponseNotFound()
        return JsonResponse(
            {
                "title": article.title,
                "content": article.content,
                "author": article.author.id,
            }
        )
    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        try:
            body = request.body.decode()
            title = json.loads(body)["title"]
            content = json.loads(body)["content"]
        except:
            return HttpResponseBadRequest()

        try:
            article = Article.objects.get(id=article_id)
        except:
            return HttpResponseNotFound()

        if article.author.id != request.user.id:
            return HttpResponseForbidden()

        article.title = title
        article.content = content
        article.save()
        response_article = {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author": article.author.id,
        }
        return dict_to_response(response_article, 200)

    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        try:
            article = Article.objects.get(id=article_id)
        except:
            return HttpResponseNotFound()

        if article.author.id != request.user.id:
            return HttpResponseForbidden()

        article.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])


def article_comment(request: HttpRequest, article_id: int = 0) -> HttpResponse:
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        try:
            article = Article.objects.get(id=article_id)
        except:
            return HttpResponseNotFound()

        comment_list = [
            {
                "article": comment.article_id,
                "content": comment.content,
                "author": comment.author_id,
            }
            for comment in article.article_set.all()
        ]
        return JsonResponse(comment_list, safe=False)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        try:
            article = Article.objects.get(id=article_id)
        except:
            return HttpResponseNotFound()

        try:
            req_data = json.loads(request.body.decode())
            content = req_data["content"]
        except (KeyError, json.JSONDecodeError) as e:
            return HttpResponseBadRequest()

        comment = Comment(article=article, content=content, author=request.user)
        comment.save()
        response_comment = {
            "id": comment.id,
            "article": comment.article.id,
            "content": comment.content,
            "author": comment.author.id,
        }
        return dict_to_response(response_comment, 201)

    else:
        return HttpResponseNotAllowed(["GET", "POST"])


def comment(request: HttpRequest, comment_id: int = 0) -> HttpResponse:
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return HttpResponseNotFound()

        return JsonResponse(
            {
                "article": comment.article.id,
                "content": comment.content,
                "author": comment.author.id,
            }
        )
    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        try:
            req_data = json.loads(request.body.decode())
            content = req_data["content"]
        except (KeyError, json.JSONDecodeError) as e:
            return HttpResponseBadRequest()

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return HttpResponseNotFound()

        if comment.author.id != request.user.id:
            return HttpResponseForbidden()

        comment.content = content
        comment.save()
        response_comment = {
            "id": comment.id,
            "article": comment.article.id,
            "content": comment.content,
            "author": comment.author.id,
        }
        return dict_to_response(response_comment, 200)

    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return HttpResponse(status=401)

        try:
            comment = Comment.objects.get(id=comment_id)
        except:
            return HttpResponseNotFound()

        if comment.author.id != request.user.id:
            return HttpResponseForbidden()

        comment.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])


@ensure_csrf_cookie
def token(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return HttpResponse(status=204)
    else:
        return HttpResponseNotAllowed(["GET"])
