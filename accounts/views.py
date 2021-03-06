from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from .forms import UserLoginForm, UserSignUpForm, StaffField
from .forms import UserSignUpFormAddon, UserAdditionalFields
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from review.models import Review
from checkout.models import Order, OrderLineItem
from django.contrib.auth.models import User

# Create your views here.


def login(request):
    """A view that manages the login form."""
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request.POST['username_or_email'],
                                     password=request.POST['password'])

            if user:
                auth.login(request, user)
                username = request.user.username
                messages.success(request, "Welcome %s!" % username)

                if request.GET and request.GET['next'] != '':
                    nextItem = request.GET['next']
                    return HttpResponseRedirect(nextItem)
                else:
                    return redirect(reverse('profile'))
            else:
                user_form.add_error(
                    None, "Your username or password are incorrect")
    else:
        user_form = UserLoginForm()

    args = {'user_form': user_form,
            'nextItem': request.GET.get('nextItem', '')}
    return render(request, 'login.html', args)


def logout(request):
    """A view that logs the user out and redirects back to the index page."""
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('index'))


@login_required
def profile(request):
    """A view that displays the profile page of a logged in user,
    reviews that the user has made are passed to the profile page also."""
    user = request.user
    reviews = Review.objects.filter(user_id=user.id)
    orders = Order.objects.filter(user_id=user.id).order_by('-date')
    items = OrderLineItem.objects.all()
    args = {"reviews": reviews, "orders": orders, "items": items}
    return render(request, 'profile.html', args)


def register(request):
    """A view that manages the registration form."""
    if request.method == 'POST':
        user_form = UserSignUpForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            user = auth.authenticate(request.POST.get('email'),
                                     password=request.POST.get('password1'))
            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('profile'))

            else:
                messages.error(request, "Unable to log you in at this time!")
    else:
        user_form = UserSignUpForm()

    args = {'user_form': user_form}
    return render(request, 'sign-up.html', args)


@login_required
def edit_user(request):
    """A view that allows a user to add and edit
    additional information for their profile."""
    this_user = request.user

    if request.method == 'POST':
        user_form = UserSignUpFormAddon(request.POST, instance=request.user)
        profile_form = UserAdditionalFields(
            request.POST, request.FILES, instance=request.user.usercreate)

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request, "Your profile has successfully been updated!")
            return redirect(reverse('profile'))
        else:
            messages.error(
                request, "Unable to update. Please rectify the problems below")
    else:
        user_form = UserSignUpFormAddon(instance=request.user)
        profile_form = UserAdditionalFields(instance=request.user.usercreate)
        staff_form = StaffField()
    args = {
        'user_form': user_form,
        'profile_form': profile_form,
        'staff_form': staff_form,
        'this_user': this_user
    }
    return render(request, 'edit_user.html', args)


def delete_user(request):
    user = request.user
    try:
        user.delete()
        messages.success(request, "Account successfully deleted.")
    except Exception as e:
        messages.success(request, "Account not deleted")
        return redirect(reverse('index', {'err': e.message}))
    return redirect(reverse('index'))


def all_orders(request):
    """A view that displays the profile page of a logged in user,
    reviews that the user has made are passed to the profile page also."""
    user = request.user
    orders = Order.objects.filter(user_id=user.id).order_by('-date')
    items = OrderLineItem.objects.all()
    args = {"orders": orders, "items": items}
    return render(request, 'all_orders.html', args)


@login_required
def all_users(request):
    """A view that displays all of the users for a staff / admin to,
    review the users basic info and change if they are staff or not."""
    all_users = User.objects.all()
    return render(request, 'all_users.html', {"all_users": all_users})


@login_required
def admin_delete_user(request, pk):
    """A view that allows an admin to delete a user."""
    admin = request.user
    this_user = get_object_or_404(User, id=pk)

    try:
        this_user.delete()
        messages.success(request, "Account successfully deleted.")
        if admin.id == this_user.id:
            return redirect(reverse('index'))
    except Exception as e:
        messages.success(request, "Account not deleted")
        return redirect(reverse('all_users', {'err': e.message}))
    return redirect(reverse('all_users'))


@login_required
def admin_edit_user(request, pk):
    """A view that allows an admin to edit a user."""
    this_user = get_object_or_404(User, id=pk)

    if request.method == 'POST':
        user_form = UserSignUpFormAddon(request.POST, instance=this_user)
        profile_form = UserAdditionalFields(
            request.POST, request.FILES, instance=this_user.usercreate)
        staff_form = StaffField(request.POST, instance=this_user.usercreate)

        if profile_form.is_valid() and user_form.is_valid() and staff_form.is_valid():
            user_form.save()
            profile_form.save()
            staff_form.save()

            messages.success(
                request, "Your profile has successfully been updated!")
            return redirect(reverse('all_users'))

        else:
            messages.error(
                request, "Unable to update. Please rectify the problems below")
    else:
        user_form = UserSignUpFormAddon(instance=this_user)
        profile_form = UserAdditionalFields(instance=this_user.usercreate)
        staff_form = StaffField(instance=this_user.usercreate)

    args = {
        'user_form': user_form,
        'profile_form': profile_form,
        'staff_form': staff_form,
        'this_user': this_user
    }
    return render(request, 'edit_user.html', args)
