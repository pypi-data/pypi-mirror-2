=========================
The feed subscription API
=========================

TypePad provides a feed subscription API that lets you subscribe to TypePad and web feed content. Once you subscribe your application to a feed, TypePad will discover new items in the feed automatically and push the content to your group or application.

The feed subscription API is only available using authenticated requests. Use your TypePad application's anonymous access token to subscribe to feeds and modify subscriptions. For more on authentication, see :doc:`../tut/auth`.


Feeds and filters
=================

The feed subscription API allows you to create *subscriptions* to feeds. These subscriptions are represented by :class:`ExternalFeedSubscription` instances. Subscriptions can deliver feed content either to a `Group` or to your web application as a web hook.

Each subscription has one or more *feeds* that provide the subscription's content. For instance, when creating a subscription about the Python programming language, you might subscribe to feeds from Planet Python, Stack Overflow questions tagged ``python``, and Repopular's feed of recently mentioned GitHub projects in Python. As TypePad discovers new items in any of these feeds, those items would then be posted in your group or be pushed to your web hook callback URL.

Feeds are identified by the web URLs of their feed documents. These are some feed identifiers:

* ``http://feeds.feedburner.com/AskMetafilter``
* ``http://markpasc.typepad.com/blog/atom.xml``
* ``http://twitter.com/statuses/user_timeline/5553562.rss``

Sometimes you can't find a specific feed for the content you'd like to subscribe to. To pull specific content out of a general feed, each subscription also has zero or more *filter rules*. These filters are search queries with the same syntax as `TypePad full-text asset search queries`_. If a subscription has some filter rules, feed items that match *any* of the filters are delivered. If an item matches none of the filters, TypePad will discard that item. (If you want to require items contain *all* of a set of keywords, specify one filter rule with all of those keywords.)

These are some examples of filters:

* ``nintendo``
* ``python -snake``
* ``"cheese pizza"``
* ``title:awesome``

See `the asset search API endpoint documentation`_ for what syntax is available in filter rules.

.. _the asset search API endpoint documentation: http://www.typepad.com/services/apidocs/endpoints/assets#full-text_search
.. _TypePad full-text asset search queries: http://www.typepad.com/services/apidocs/endpoints/assets#full-text_search


Subscribing a `Group` to feeds
==============================

A good use of the feed subscription API is to automatically collect feed items from third-party web sites into a TypePad `Group`. For instance, if you run a bicycle shop and provide a `Group` powered web site for your fans and customers, you can use the feed subscription API to automatically post all your Twitter tweets to the group where your fans can comment on them and save them as favorites.

To add a subscription to a group, use the `Group.create_external_feed_subscription()` method.

.. function:: typepad.Group.create_external_feed_subscription(feed_idents, filter_rules, post_as_user_id)

   Creates a new feed subscription for the group.

   The subscription is subscribed to the feeds named in ``feed_idents``, a list of feed URLs. The items discovered in these feeds are filtered by ``filter_rules``, a list of search queries, before being posted to the group. Items that match *any* of the filter rules are posted to the group as the `User` identified by ``post_as_user_id``, a TypePad user URL identifier.

   The return value is an object the ``subscription`` attribute of which is the `ExternalFeedSubscription` for the new subscription.

In the bicycle shop example, you would provide the feed for your Twitter stream as a single URL in ``feed_idents``, an empty list for ``filter_rules``, and your own TypePad account's URL identifier for ``post_as_user_id``::

   user = typepad.User.get_by_url_id(MY_USER_ID)
   group = typepad.Group.get_by_url_id(SHOP_GROUP_ID)
   group.create_external_feed_subscription(
       feed_idents=['http://twitter.com/statuses/user_timeline/5553562.rss'],
       filter_rules=[],
       post_as_user_id=user.url_id)

Once your `Group` has some subscriptions, you can also retrieve those subscriptions as the group's `external_feed_subscriptions` list.

.. attribute:: typepad.Group.external_feed_subscriptions

   A list of `ExternalFeedSubscription` instances representing the group's subscriptions.


Subscribing an `Application` to feeds
=====================================

In addition to collecting feed items into groups, TypePad can also push feed content directly to your web application. Once subscribed, TypePad will send HTTP requests to your web app when new feed content is available. (This does mean your web application must be available to TypePad over the public Internet to use this API.) While subscription occurs through the TypePad API, subscriptions are verified and content is pushed using `the PubSubHubbub protocol`_.

Like `Group` instances, `Application` instances provide lists of their existing subscriptions in their `external_feed_subscriptions` endpoints. Once subscribed, your subscription will show up in this list.

.. attribute:: typepad.Application.external_feed_subscriptions

   A list of `ExternalFeedSubscription` instances representing the `Application` instance's subscriptions.

To create a new subscription, use the `Application.create_external_feed_subscription()` method.

.. function:: typepad.Application.create_external_feed_subscription(callback_url, feed_idents, filter_rules, verify_token, secret=None)

   Creates and immediately verifies a new feed subscription for the application.

   The subscription is subscribed to the feeds named in ``feed_idents``, a list of feed URLs. The items discovered in these feeds are filtered by ``filter_rules``, a list of search queries, before being posted to the group. Items that are not filtered out are posted in HTTP ``POST`` requests to ``callback_url``, your application's feed subscription callback URL, according to the PubSubHubbub protocol.

   If ``secret`` (a string) is provided, TypePad will use it to sign the content pushes it sends to your callback URL according to `PubSubHubbub's Authenticated Content Distribution protocol`_.

   This method returns an object with a ``subscription`` attribute containing an `ExternalFeedSubscription` instance representing the new subscription.

.. note::

   TypePad will attempt to verify your callback URL *during* your call to this method. Your web application must be available to respond to TypePad while this call occurs.

Verifying the subscription
--------------------------

During the `create_external_feed_subscription()` call, TypePad will send a *subscription verification request* to your callback URL. For example, you may create a subscription like this::

   app = typepad.Application.get_by_url_id(MY_APP_ID)
   app.create_external_feed_subscription(
       callback_url='http://myapp.example.com/feed-sub',
       feed_idents=['http://twitter.com/statuses/user_timeline/5553562.rss'],
       filter_rules=[],
       verify_token='3FQui9KU6')

As `described in the PubSubHubbub specification`_, TypePad verifies the subscription using a ``GET`` request. A verification request may look like::

   GET /feed-sub?hub.mode=subscribe&hub.challenge=4mg4zMm8J&hub.verify_token=3FQui9KU6 HTTP/1.1
   Host: myapp.example.com
   

Your app would then need to verify the request is correct by checking the ``hub.verify_token`` and any other housekeeping you need to do, then send back the ``hub.challenge`` parameter in a 200 OK response::

   200 OK
   Content-Type: text/plain
   Content-Length: 10
   
   4mg4zMm8J

Receiving new feed content
--------------------------

Once subscribed, TypePad will send *content distribution requests* to your callback URL. These requests are Atom feeds containing the new items. (Even when you subscribe to RSS feeds, the feed items are normalized into Atom entries.)

::

   POST /feed-sub HTTP/1.1
   Host: myapp.example.com
   Content-Type: application/atom+xml
   Content-Length: 1188
   
   <?xml version="1.0" encoding="utf-8"?>
   <feed xmlns="http://www.w3.org/2005/Atom">
       <id>tag:firehoser.superfeedr.com,2010-06-06:feeds.example.com/ExampleFeed</id>
       <updated>2010-07-06T22:27:19Z</updated>
       <title>Example Feed</title>
       <link rel="self" href="http://feeds.example.com/ExampleFeed"/>
       <entry xmlns:geo="http://www.georss.org/georss" xmlns:as="http://activitystrea.ms/spec/1.0/" xmlns:sf="http://superfeedr.com/xmpp-pubsub-ext" xml:lang="en-us">
           <id>tag:feeds.example.com,2010:site.555746</id>
           <published>2010-07-06T23:26:42+00:00</published>
           <title>Example entry</title>
           <summary type="html">This is the summary for the example entry.&lt;br /&gt;</summary>
           <link title="Example entry" type="application/rss+xml" rel="replies" href="http://example.com/555746/Example-entry/rss"/>
           <link title="Example entry" type="text/html" rel="alternate" href="http://example.com/555746/Example-entry"/>
           <category term="example"/>
           <category term="entry"/>
           <category term="feeds"/>
           <category term="xml"/>
           <author>
               <name>Some Author</name>
           </author>
       </entry>
   </feed>

Per the PubSubHubbub protocol, return any 2xx code response to acknowledge receipt of the new content. For more on the format of the verification and content requests, see `the TypePad endpoint documentation`_.

.. _the PubSubHubbub protocol: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html
.. _described in the PubSubHubbub specification: 
.. _PubSubHubbub's Authenticated Content Distribution protocol: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html#authednotify
.. _the TypePad endpoint documentation: http://www.typepad.com/services/apidocs/endpoints/applications/%253Cid%253E/create-external-feed-subscription


Modifying subscriptions
=======================

You can modify an existing subscription in several ways, whether it was newly created or pulled from a list endpoint.

If you have only the ID of an `ExternalFeedSubscription`, load the instance with the `get_by_url_id()` method.

.. automethod:: typepad.api.ExternalFeedSubscription.get_by_url_id

   Returns the subscription identified by ``url_id``.

For any `ExternalFeedSubscription` instance, you can list its feeds using its `feeds` endpoint, as well as change its feeds using the `add_feeds()` and `remove_feeds()` methods.

.. attribute:: typepad.ExternalFeedSubscription.feeds

   A list of the feed URLs (as strings) to which the subscription is subscribed.

.. method:: typepad.ExternalFeedSubscription.add_feeds(feed_idents)

   Adds the specified feed identifiers to the subscription.

   For ``feed_idents``, specify a list of feed URLs to add to the subscription. Feed identifiers that are already part of the subscription are ignored. This method returns no value.

.. method:: typepad.ExternalFeedSubscription.remove_feeds(feed_idents)

   Removes the specified feed identifiers from the subscription.

   For ``feed_idents``, specify a list of feed URLs to remove from the subscription. Feed identifiers that are not part of the subscription are ignored. This method returns no value.

In addition to changing the subscribed feeds, you can also change the filters using the `update_filters()` method.

.. method:: typepad.ExternalFeedSubscription.update_filters(filter_rules)

   Changes the subscription's filters to those specified.

   For ``filter_rules``, specify a list of strings containing search queries by which to filter. The subscription's existing filters will be *replaced* by the filters you specify. To remove all the filters from a subscription, pass an empty list for ``filter_rules``. This method returns no value.

You can also change the way a subscription is delivered. For a `Group` subscription, use the `ExternalFeedSubscription` instance's `update_user()` method; for an `Application` subscription, the `update_notification_settings()` method.

.. method:: typepad.ExternalFeedSubscription.update_user(post_as_user_id)

   Changes a `Group` subscription to deliver feed items to the group as posted by the identified user.

   Specify the new author's TypePad URL identifier as ``post_as_user_id``.

.. method:: typepad.ExternalFeedSubscription.update_notification_settings(callback_url, secret=None, verify_token=None)

   Changes the callback URL or secure secret used to deliver this subscription's new feed items to your web application.

   Specify your application's callback URL for the ``callback_url`` parameter. If you're asking to change the callback URL (that is, ``callback_url`` is different from the subscription's existing callback URL), TypePad will send the new URL a subscription verification request; in that case, you must provide a verification token as the ``verify_token`` parameter.

   If you specify a ``secret``, TypePad will use that secret to deliver future content per PubSubHubbub's Authenticated Content Distribution protocol. If no secret is provided, future content delivery will not be authenticated. To preserve an existing secret, you must provide it as the ``secret`` parameter.

To stop receiving content from a subscription in your `Group` or callback URL, delete the subscription.

.. method:: typepad.ExternalFeedSubscription.delete()

   Deletes a subscription.

   Once a subscription is deleted, items in its feeds will no longer be added to the subscribed `Group` or pushed to the subscribed callback URL.
