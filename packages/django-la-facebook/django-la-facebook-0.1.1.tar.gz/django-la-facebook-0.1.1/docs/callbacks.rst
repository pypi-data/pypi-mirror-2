Callbacks
=========

In the context of la_facebook, callbacks are a subclass of
la_facebook.callbacks.base.BaseFacebookCallback.

The callback is called after the user authenticates with Facebook, either for
the first time, or when returning after authentication expiration. The callback
determines what happens next, whether that be a user being created, or the
browser being redirected.

la_facebook ships with two callbacks. BaseFacebookCallback defines the key
steps that any response to a facebook auth should include, but is largely an
abstract class.  DefaultFacebookCallback is a working callback that addresses
the most common use case for basic user auth. Most projects will
probably be fine to just use this default implementation.

What the default implementation does
------------------------------------

When a new user comes to your site, and clicks on a link that calls the
la_facebook.views.facebook_login view, they are redirected to facebook
where they are authenticated and approve your app. They are then redirected
to your site and the default callback is executed. This callback fist checks
whether there is already an authenticated Django user in the session. If not
the Facebook id of the user is examined and it is determined whether they have
previously authenticated to the site by looking for database model that stores
an association between a Django user and a Facebook user.

If there exists a prior association, the expiration of that users Facebook
authentication token is updated, the Django session expiration is set to match,
and the user is logged and redirected.

If no prior association is present, a django user and its association object
are created. The default Django username consists of the facebook user's name
sluggified and concatenated with their facebook id. Any profile object, as
defined in Django's settings, is updated with any matching fields in the users
Facebook data.

Callback Reference
------------------

A callback is a view like object is called with instances of a Django request,
OAuthAccess, and OAuth20Token.


.. py:class:: BaseFacebookCallback

    Provides a largely abstract class defining an auth interaction with
    Facebook.

.. py:method:: __call__(request, access, token)

    is called by the view and handles the basic check of whether the user
    is authenticated and dispatches to the other methods as nessasary and then
    returns the response to the view and thus to the browser (usually a redirect)

.. py:method:: fetch_user_data(request, access, token)

    Not implemented.

.. py:method:: lookup_user(request, access, token)

    Not implemented.

.. py:method:: redirect_url(request, access, token)

    Checks in order: the request GET params, the session, settings for
    a url to redirect to.

.. py:method:: handle_no_user(request, access, token, user_data)

    Not implemented.

.. py:method:: handle_unauthenticated_user(request, access, token, user_data)

    Not implemented.

.. py:method:: identifier_from_data(data)

    Concatenates a sluggified facebook name and user id

.. py:module:: la_facebook.callbacks.default


.. py:class:: DefaultFacebookCallback

    Provides the default implementation.

.. py:method:: fetch_user_data(self, request, access, token):

    Uses the authorized token and makes an API call to Facebook to retrieve the
    user graph data.

.. py:method:: lookup_user(self, request, access, user_data):

    Based on the Facebook user ID in the :param user_data:, will attempt to
    lookup a an associated Django user.  If one is not found, returns None.

.. py:method:: persist(self, user, token, user_data):

    Creates or updates the user association object, and if available updates
    the Django user's email from the Facebook user's data.

.. py:method:: handle_no_user(self, request, access, token, user_data):

    The default implementation simply returns :py:meth:`.create_user`.

.. py:method:: login_user(self, request, user):

    The default implementation assumes Django's model backend, and will log the
    user in via that backend's login method.

.. py:method:: handle_unauthenticated_user(self, request, user, access, token, user_data):

    Given a valid user, the user is first logged in, and then their Facebook
    data is created or updated through persist.  Finally the session's
    expiration is set to match the expiration of the Facebook auth token.

.. py:method:: update_profile_from_graph(self, request, access, token, profile):

    Given a profile object, will try to update any fields whose names match the
    Facebook usergraph object.

.. py:method:: create_profile(self, request, access, token, user):

    if ``AUTH_PROFILE_MODULE`` is set, will attempt to create and then update
    a profile object for the given user.

.. py:method:: create_user(self, request, access, token, user_data):

    If the user does not already exist, creates a user, a profile if available,
    and logs the user in.

