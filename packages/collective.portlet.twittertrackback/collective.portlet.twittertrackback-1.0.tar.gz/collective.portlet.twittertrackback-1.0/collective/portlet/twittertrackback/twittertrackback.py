from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.twittertrackback import TwitterTrackbackMessageFactory as _
from plone.memoize.ram import cache

import re
from urllib2 import URLError, urlopen
from simplejson import loads
from time import time

# Match and capture urls
urlsRegexp = re.compile(r"""
    (
    # Protocol
    http://
    # Alphanumeric, dash, slash or dot
    [A-Za-z0-9\-/.]*
    # Don't end with a dot
    [A-Za-z0-9\-/]+
    )
    """, re.VERBOSE)

# Match and capture #tags
hashRegexp = re.compile(r"""
    # Hash at start of string or after space, followed by at least one
    # alphanumeric or dash
    (?:^|(?<=\s))\#([A-Za-z0-9\-]+)
    """, re.VERBOSE)

# Match and capture @names
atRegexp = re.compile(r"""
    # At symbol at start of string or after space, followed by at least one
    # alphanumeric or dash
    (?:^|(?<=\s))@([A-Za-z0-9\-]+)
    """, re.VERBOSE)

# Match and capture email address
emailRegexp = re.compile(r"""
    # Email at start of string or after space
    (?:^|(?<=\s))([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})\b
    """, re.VERBOSE|re.IGNORECASE)

def expand_tweet(str):
    """This method takes a string, parses it for URLs, hashtags and mentions
       and returns a hyperlinked string."""

    str = re.sub(urlsRegexp, '<a href="\g<1>">\g<1></a>', str)
    str = re.sub(hashRegexp, '<a href="http://twitter.com/search?q=%23\g<1>">#\g<1></a>', str)
    str = re.sub(atRegexp, '<a href="http://twitter.com/\g<1>">@\g<1></a>', str)
    str = re.sub(emailRegexp, '<a href="mailto:\g<1>">\g<1></a>', str)
    return str


class ITwitterTrackback(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    name = schema.TextLine(
        title=_(u"Title"),
        description=_(u"The title of the portlet")
        )


    use_actual_url = schema.Bool(title=_(u"Use ACTUAL_URL"),
                                  description=_(u"By default we'll use absolute_url() to work out the url, or if this is checked we will use ACTUAL_URL from the request."),
                                  default=False)

    count = schema.Int(
        title=_(u'Number of items to display'),
        description=_(u'How many items to list.'),
        required=True,
        default=5
        )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ITwitterTrackback)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self, name=u"", use_actual_url=False, count=5):
        self.name = name
        self.use_actual_url = use_actual_url
        self.count = count


    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Twitter Trackback"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('twittertrackback.pt')

    @property
    def title(self):
        return self.data.name or _(u"Tweets")

    @property
    def available(self):
        return len(self.get_tweets()) != 0

    def expand(self, str):
        return expand_tweet(str)

#    @cache(lambda a,b: time() // 180)
    def get_tweets(self):
        if self.data.use_actual_url:
            url = self.request.ACTUAL_URL
        else:
            url = self.context.absolute_url()

        apiurl = "http://otter.topsy.com/trackbacks.json?url=%s&perpage=%d" % (url, self.data.count)

        try:
            json = urlopen(apiurl).read()
            data = loads(json)
            tweets = data['response']['list']
        except URLError:
            return None

        return tweets



class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ITwitterTrackback)

    def create(self, data):
        return Assignment(**data)


# NOTE: If this portlet does not have any configurable parameters, you
# can use the next AddForm implementation instead of the previous.

# class AddForm(base.NullAddForm):
#     """Portlet add form.
#     """
#     def create(self):
#         return Assignment()


# NOTE: If this portlet does not have any configurable parameters, you
# can remove the EditForm class definition and delete the editview
# attribute from the <plone:portlet /> registration in configure.zcml


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ITwitterTrackback)
