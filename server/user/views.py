from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.template import RequestContext

from django.contrib.auth import login, logout

import json

from shared.request import make_response, ErrorResponse
from .models import Subscription, User


def user_dict(user):
    return {}

# These correspond to the filters the user can apply.
valid_keys = {"projects", "text", "box"}


def validate_query(d):
    # Remove unrecognized keys:
    for k in set(d.keys()).difference(valid_keys):
        del d[k]

    if "projects" in d:
        d["projects"] = d["projects"].lower()
        if d["projects"] not in {"all", "null"}:
            del d["projects"]

    # Verify that all the keys are well-formed
    return d


@make_response("subscribed.djhtml", "subscribe_error.djhtml")
def subscribe(request):
    """
    Set up a new subscription. If the supplied
    """
    if request.method is not "POST":
        return ErrorResponse("Request must use POST method.", status=405)

    try:
        query_dict = json.loads(request.POST["query"])
    except KeyError:
        return ErrorResponse("Missing a 'query' field")
    except ValueError:
        return ErrorResponse("Malformed JSON in 'query' field.")

    query_dict = validate_query(query_dict)
    if not query_dict:
        return ErrorResponse("Invalid query", {"query": query_dict})

    user = request.user
    new_user = False

    if not user:
        try:
            email = request.POST["email"]
            user = User.objects.get(email=email)
        except KeyError as kerr:
            return ErrorResponse(
                "Missing required key:" + kerr.args[0],
                {})
        except User.DoesNotExist:
            user = User.objects.create(email=email)
            new_user = True

    try:
        subscription = Subscription()
        subscription.set_validated_query(query_dict)
        user.subscriptions.add(subscription)
    except Exception:
        return ErrorResponse("Invalid subscription")

    messages.success(request, "Subscription added")
    return {"new_user": new_user,
            "email": user.email}


def do_login(request, token, uid):
    try:
        user = User.objects.get(pk=uid)
        if user.token == token:
            login(request, user)
            user.generate_token()
            return user
    except User.DoesNotExist:
        return None


def with_user(view_fn):
    def wrapped_fn(request):
        if request.user:
            return view_fn(request, request.user)
        else:
            try:
                user = do_login(request,
                                request.GET["token"],
                                request.GET["uid"])
                if user:
                    return view_fn(request, user)
            except KeyError:
                messages.error(request,
                               "You must be logged in to view that page.")

            return redirect("/")

    return wrapped_fn


def user_login(request, token, pk):
    try:
        user = User.objects.get(pk=pk)
        if user.token != token:
            messages.error(request, "")
            return render(request, "token_error.djhtml",
                          status=403)
    except User.DoesNotExist:
        user = None

    if not user:
        return redirect("/")

    login(request, user)
    redirect(reverse(manage))


@with_user
def activate_account(request, user):
    user.activate()

    return redirect(reverse("manage-user"))


@with_user
def deactivate_account(request, user):
    user.deactivate()

    return redirect("/")


@with_user
def manage(request, user):
    if not user.is_active:
        user.activate()
        messages.success(request,
                         "Thank you for confirming your account.")

    return render("user/manager.djhtml",
                  {"user": user,
                   "subscriptions": user.subscriptions},
                  context_instance=RequestContext(request))


@with_user
def delete_subscription(request, user, sub_id):
    try:
        subscription = user.subscriptions.get(pk=sub_id)
        subscription.delete()
        messages.success(request, "Subscription deleted")
    except Subscription.DoesNotExist:
        messages.error(request, "Invalid subscription ID")
    return redirect(reverse(manage))


def user_logout(request):
    logout(request)

    return redirect("/")
