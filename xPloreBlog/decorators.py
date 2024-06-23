# Here we are creating a decorator to check whether the user is authenticated or not. We'll use this decorator where we believe logged-in users shouldn't be able to access it. As I mentioned, we create a function inside a function that we call a decorator, and to access a Django request, we again create another specific function that we call a "_wrapped_view". Here, we check if a user is authenticated; if it is, we return a redirect function. Otherwise, we redirect the original function the user is trying to access. Not to make it too complicated, let's leave it as it is; it will do the hard work we want. For more detailed information about decorators, you may navigate to Django's official documentation about decorators.

from django.shortcuts import redirect


def user_not_authenticated(function=None, redirect_url='/'):
    """
    Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if necessary by default.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator
