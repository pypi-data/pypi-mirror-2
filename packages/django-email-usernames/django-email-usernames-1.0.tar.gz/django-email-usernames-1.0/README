django-email-usernames
========================

django-email-usernames is an app that takes care of letting your django site
use emails for logging in, like facebook, google and other major sites.

It consists of a email authentication backend, a email login form, a login
view, and also a helper view that together with the popular django-registration
app makes it simple for you to let users create new accounts with email as
username.

Installation
---------------

1. First add it as any other django app, to your installed apps:

    ```python
    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'email_usernames',
    )
    ```

    Obviously you also need to have the django.contrib.auth app in there, in order
    for authentication to be enabled.

2. Add the EmailOrUsernameModelBackend backend to AUTHENTICATION_BACKENDS 
   in your settings:

    ```python
    AUTHENTICATION_BACKENDS = (
        # Our custom auth backend that allows email addresses to be used as
        # usernames.
        'email_usernames.backends.EmailOrUsernameModelBackend', 
        # Default auth backend that handles everything else.
        'django.contrib.auth.backends.ModelBackend', 
    )
    ```

3. This step is important! Because the built-in django username column in
   the auth_user table only allows 30 character long usernames by default, you
   need to modify it to be at least 75 characters. If you don't do this,
   emails that are longer than 30 characters long will be cut off, and this
   app will likely not work!

   You can do this change either manually with SQL, or if you have not run
   syncdb for your site the first time, then django-email-usernames can try to
   do the change for you.

    ### Way #1: Changing the username column manually

    Run the following SQL:
    ```sql
    ALTER TABLE auth_user MODIFY COLUMN username varchar(75) NOT NULL;
    ```
    ### Way #2: Let django-email-usernames do it for you

    When you run python manage.py syncdb the first time, and the
    django.contrib.auth models are created for the first time,
    django-email-usernames will detect this and ask if you want to fix the
    username field in the auth_user table to be 75 chars long instead of 30
    chars. Say yes in the prompt, and it will run the proper SQL for you. For
    this to work, the SQL user needs the ALTER TABLE privileges, otherwise you
    need to do the change manually (see way #1 above).

Example Usage
----------------

    Coming soon!
