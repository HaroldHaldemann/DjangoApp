import itertools

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from authentication.models import User
from reviews import models
from reviews.forms import FollowForm, ReviewForm, TicketForm


# =========== FLOW ========== #


@login_required
def flow_page(request: HttpRequest) -> HttpResponse:
    followed_users = [user_follows.followed_user for user_follows in request.user.following.all()] + [request.user]

    tickets = [
        ticket for ticket in models.Ticket.objects.all()
        if ticket.user in followed_users
    ]
    reviews = [
        review for review in models.Review.objects.all()
        if (review.user in followed_users or review.ticket.user in followed_users)
    ]

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


# ========== MY POSTS ========== #


@login_required
def my_posts_page(request: HttpRequest) -> HttpResponse:
    tickets = [ticket for ticket in models.Ticket.objects.all() if ticket.user == request.user]
    reviews = [review for review in models.Review.objects.all() if review.user == request.user]

    for review in reviews:
        review.star_rating = review.headline + " - " + "★" * review.rating + "☆" * (5 - review.rating)

    tickets_and_reviews = sorted(
        itertools.chain(tickets, reviews),
        key=lambda element: element.time_created,
        reverse=True
    )
    context = {'flow_elements': tickets_and_reviews}
    return render(request, 'reviews/my_posts.html', context=context)


# ========== USER FOLLOWS =========== #


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
                message = f"Cet utilisateur '{followed_user_username}' n'existe pas, " \
                    "veuillez choisir un nom d'utilisateur valide."

            else:
                if user.username == followed_user_username:
                    message = "Vous ne pouvez vous suivre, veuillez choisir un nom d'utilisateur valide."

                elif followed_user in [user_follows.followed_user for user_follows in user.following.all()]:
                    message = f"Vous suivez déjà cet utilisateur '{followed_user_username}', " \
                        "veuillez choisir un nom d'utilisateur valide."

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


# ========== REVIEWS ========== #


@login_required
def create_review_page(request: HttpRequest, ticket_id: int = 0, review_id: int = 0) -> HttpResponse:
    review_form: ReviewForm = ReviewForm()
    ticket_form: TicketForm = TicketForm()
    action: str = "Créer votre critique"

    if review_id != 0:
        review = models.Review.objects.get(id=review_id)
        ticket_id = review.ticket.id
        review_form = ReviewForm(instance=review)
        action = "Modifier votre critique"

    if ticket_id != 0:
        ticket = models.Ticket.objects.get(id=ticket_id)
        ticket_form = TicketForm(instance=ticket)
        ticket_form.fields['title'].disable = True
        ticket_form.fields['description'].disable = True

    if request.method == 'POST':
        if review_id == 0:
            review_form = ReviewForm(request.POST)
            review_user = request.user
        else:
            review_form = ReviewForm(instance=review, data=request.POST)
            review_user = review.user

        if ticket_id == 0:
            ticket_form = TicketForm(request.POST)
            ticket_user = request.user
        else:
            ticket_form = TicketForm(instance=ticket, data=request.POST)
            ticket_user = ticket.user

        if all([review_form.is_valid(), ticket_form.is_valid()]):
            if ticket_id == 0:
                if ticket_form.cleaned_data:
                    ticket = ticket_form.save(commit=False)
                    ticket.user = ticket_user
                    ticket.save()

            if review_form.cleaned_data:
                review = review_form.save(commit=False)
                review.ticket = ticket
                review.user = review_user
                review.save()

            return my_posts_page(request)

    context = {'review_form': review_form, 'ticket_form': ticket_form, "action": action}
    return render(request, 'reviews/review.html', context=context)


@login_required
def update_review_page(request: HttpRequest, review_id: int) -> HttpResponse:
    return create_review_page(request, review_id=review_id)


@login_required
def delete_review_page(request: HttpRequest, review_id: int) -> HttpResponse:
    models.Review.objects.get(id=review_id).delete()
    return my_posts_page(request)


# ========== TICKETS ========== #


@login_required
def create_ticket_page(request: HttpRequest, ticket_id: int = 0) -> HttpResponse:
    form: TicketForm = TicketForm()
    action: str = "Créer votre ticket"

    if ticket_id != 0:
        ticket = models.Ticket.objects.get(id=ticket_id)
        form = TicketForm(instance=ticket)
        action = "Modifier votre ticket"

    if request.method == 'POST':
        if ticket_id == 0:
            form = TicketForm(request.POST)
            user: User = request.user
        else:
            form = TicketForm(instance=ticket, data=request.POST)
            user = ticket.user

        if form.is_valid():

            if form.cleaned_data:
                ticket = form.save(commit=False)
                ticket.user = user
                ticket.save()

            return my_posts_page(request)

    context = {'form': form, 'action': action}
    return render(request, 'reviews/ticket.html', context=context)


@login_required
def update_ticket_page(request: HttpRequest, ticket_id: int) -> HttpResponse:
    return create_ticket_page(request, ticket_id)


@login_required
def delete_ticket_page(request: HttpRequest, ticket_id: int) -> HttpResponse:
    models.Ticket.objects.get(id=ticket_id).delete()
    return my_posts_page(request)
