# Copyright (c) 2010 ifPeople, Kapil Thangavelu, and Contributors
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
$Id: interfaces.py 3426 2010-04-07 22:02:23Z dglick $
"""

from zope import schema

from getpaid.core import interfaces

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('getpaid.nullpayment')

class INullPaymentOptions( interfaces.IPaymentProcessorOptions ):
    """
    Null Payment Options
    """

    allow_authorization = schema.Choice(
        title=_(u"Allow Authorizations"),
        default=u"allow_authorization",
        values = (u"allow_authorization",
                  u"no_authorization")
        )

    allow_capture = schema.Choice(
        title=_(u"Allow Captures"),
        default=u"allow_capture",
        values = (u"allow_capture",
                  u"no_capture" )
        )

    allow_refunds = schema.Choice(
        title=_(u"Allow Refunds"),
        default=u"allow_refund",
        values = (u"allow_refund",
                  u"no_refund" )
        )



