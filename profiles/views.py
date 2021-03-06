from django.shortcuts import render, redirect
from review.models import ShowReview
from mainpage.models import TVShow
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def reviews(request):
    owner_name = request.user.username
    review_list = ShowReview.objects.filter(username = owner_name)
    checkError = False
    samePassword = False

    if review_list.count() == 0:
        review_list = None

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if old_password == new_password:
                messages.error(request, "Your old and new password cannot be the same!")
                checkError = True
            else:
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('../profiles')
        else:
            checkError = True
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'reviews': review_list,
        'form': form,
        'checkError': checkError,
    }

    return render(request, 'profiles/reviews.html', context)


@login_required
def bookmarks(request):
    user = request.user
    bookmarked = user.profile.bookmark
    bookmark_list = bookmarked.split(", ")
    checkError = False

    show_list = []

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('../profiles/bookmarks')
        else:
            checkError = True
    else:
        form = PasswordChangeForm(request.user)


    if len(bookmarked) == 0:
        show_list = None
        shows = None

        context = {
        'bookmarks': bookmark_list,
        'shows': shows,
        'form': form,
        'checkError': checkError,
        'show_list': show_list,
        }
        
    else:
        for i in bookmark_list:
            show_list.append(TVShow.objects.get(name=i))

        page = request.GET.get('page', 1)

        paginator = Paginator(show_list, 6)
        try:
            shows = paginator.page(page)
        except PageNotAnInteger:
            shows = paginator.page(1)
        except EmptyPage:
            shows = paginator.page(paginator.num_pages)

        context = {
        'bookmarks': bookmark_list,
        'shows': shows,
        'form': form,
        'checkError': checkError,
        'show_list': show_list,
        }

    return render(request, 'profiles/bookmarks.html', context)


