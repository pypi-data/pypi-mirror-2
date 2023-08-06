from zope.interface import Interface
#from Products.PloneFormGen.interfaces import IPloneFormGenActionAdapter
from zope import schema
from Products.PFGVerkkomaksut import PFGVerkkomaksutMessageFactory as _

class IPFGVerkkomaksut(Interface):
#class IPFGVerkkomaksut(IPloneFormGenActionAdapter):
    """Interface for Verkkomaksut adapter.
    """

    merchant_id = schema.Int(
        title=_(u"Merchant ID"),
        description=_(u'Please input MERCHANT_ID provided by Verkkomaksut here. The default ID is for demo use which is 13466.'),
        required=True,
        default=13466,
    )

    merchant_authentication_code = schema.TextLine(
        title=_(u"Merchant Authentication Code"),
        description=_(u'Please input Merchant Authentication Code provided by Verkkomaksut here. The default ID is for demo use which is 6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ.'),
        required=True,
        default=u'6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ',
    )

    next_order_number = schema.Int(
        title=_(u"Next Order Number"),
        required=True,
        description=_(u'Please input the next order number here. This number will be automatically increased by one for each transaction and will be sent to Verkkomksut.'),
        default=1,
        )

    price_field = schema.Choice(
        title=_(u"Price Field"),
        required=True,
        description=_(u"Please select the price field which will be used for Verkkomakusut. Remember to add fixed-point field or selection field with required option checked to the form folder first."),
        vocabulary="price_fields",
    )

    cancel_message = schema.TextLine(
        title=_(u"Cancel Message"),
        description=_(u'This message will be shown when one cancels Verkkomaksut payment.'),
        required=False,
    )

    def attachments():
        """
            Attachments from the contents of the form folder.
            They are either images or files.
        """

    def price_fields():
        """
            Price fields driven from contents in the form.
            Fixed point field and selection field with required option checked could be selected.
        """

    def selected_price_field():
        """
            Field selected as the price field.
        """
