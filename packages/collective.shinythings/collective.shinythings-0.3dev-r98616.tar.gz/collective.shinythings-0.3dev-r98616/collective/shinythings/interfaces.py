from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.shinythings')

class IShinythingsConfiguration(Interface):
  """This interface defines the configlet for Shinythings."""

  roundcorners_on = schema.ASCIILine(title=_(u"label_roundcorners_on", default=u'Round corners on'),
                              description=_(u"help_roundcorners_on",
                                            default=u'The divs or classes to put round corners on.'),
                              required=True,
                              default="")

  roundcorners_top_on = schema.ASCIILine(title=_(u"label_roundcorners_top_on", default=u'Round top corners on'),
                              description=_(u"help_roundcorners_top_on",
                                            default=u'The divs or classes to put round corners only on top on.'),
                              required=True,
                              default="")
                              
  roundcorners_bottom_on = schema.ASCIILine(title=_(u"label_roundcorners_bottom_on", default=u'Round bottom corners on'),
                              description=_(u"help_roundcorners_bottom_on",
                                            default=u'The divs or classes to put round corners only on bottom on.'),
                              required=True,
                              default="")
                              
  shadow_on = schema.ASCIILine(title=_(u"label_shadow_on", default=u'Shadow effect on'),
                              description=_(u"help_shadow_on",
                                            default=u'The divs or classes to put shadow effect on.'),
                              required=False,
                              default="")

  fonteffect_on = schema.ASCIILine(title=_(u"label_fonteffect_on", default=u'Fonteffect on'),
                              description=_(u"help_fonteffect_on",
                                            default=u'The divs or classes to put fonteffect on.'),
                              required=False,
                              default="")


  fadein = schema.ASCIILine(title=_(u"label_fadein", default=u'Fade in effect on'),
                              description=_(u"help_fadein",
                                            default=u'The divs or classes to put fade in.'),
                              required=False,
                              default="")
