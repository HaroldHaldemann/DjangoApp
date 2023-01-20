import itertools

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from authentication.models import User
from reviews import models
from reviews.forms import FollowForm


@login_required
def flow_page(request: HttpRequest) -> HttpResponse:
    followed_users = [user_follows.followed_user for user_follows in request.user.following.all()] + [request.user]

    tickets = [ticket for ticket in models.Ticket.objects.all() if ticket.user in followed_users]
    reviews = [review for review in models.Review.objects.all() if (review.user in followed_users or review.ticket.user in followed_users)]

    for ticket in tickets:
        if ticket in [review.ticket for review in reviews]:
            ticket.is_ticket_reviewed = True
        else:
            ticket.is_ticket_reviewed = False

    for review in reviews:
        review.star_rating = review.headline + " - " + "★" * review.rating + "☆" * (5 - review.rating)

    tickets_and_reviews = sorted(
        itertools.chain(tickets, reviews),
        key=lambda element: element.time_created,
        reverse=True
    )
    context = {'flow_elements': tickets_and_reviews}
    return render(request, 'reviews/flow.html', context=context)


@login_required
def user_follows_page(request: HttpRequest) -> HttpResponse:
    form: FollowForm = FollowForm()
    message: str = ""

    if request.method == 'POST':
        form = FollowForm(request.POST)

        if form.is_valid():
            user: User = request.user
            followed_user_username: str = form.cleaned_data['username']

            try:
                followed_user = User.objects.get(username=followed_user_username)

            except User.DoesNotExist:
                message = f"Cet utilisateur '{followed_user_username}' n'existe pas, veuillez choisir un nom d'utilisateur valide."

            else:
                if user.username == followed_user_username:
                    message = "Vous ne pouvez vous suivre, veuillez choisir un nom d'utilisateur valide."
                
                elif followed_user in [user_follows.followed_user for user_follows in user.following.all()]:
                    message = f"Vous suivez déjà cet utilisateur '{followed_user_username}', veuillez choisir un nom d'utilisateur valide."
                
                else:
                    models.UserFollows(user=user, followed_user=followed_user).save()
                    message = f"L'utilisateur '{followed_user_username}' a été ajouté dans votre liste d'abonnements."

    followed_by_connected_user = sorted([
        user_follows
        for user_follows in request.user.following.all()
    ], key=lambda element: element.user.username)
    following_connected_user = sorted([
        user_follows
        for user_follows in request.user.followed_by.all()
    ], key=lambda element: element.followed_user.username)
    context = {
        'followed_by_connected_user': followed_by_connected_user,
        'following_connected_user': following_connected_user,
        'message': message,
        'form': form
    }
    return render(request, 'reviews/user_follows.html', context=context)

@login_required
def delete_user_follows_page(request: HttpRequest, user_follows_id: int) -> HttpResponse:
    models.UserFollows.objects.filter(id=user_follows_id).delete()
    return user_follows_page(request)

@login_required
def create_review_page(request: HttpRequest, ticket_id: int=0) -> HttpResponse:
    pass

@login_required
def create_ticket_page(request: HttpRequest) -> HttpResponse:
    pass