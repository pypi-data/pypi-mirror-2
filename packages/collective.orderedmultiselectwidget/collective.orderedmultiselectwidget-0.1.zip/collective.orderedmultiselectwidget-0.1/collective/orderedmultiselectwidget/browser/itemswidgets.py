from Acquisition import aq_base
from zope.app.form.browser.itemswidgets import OrderedMultiSelectWidget

class SecureOrderedMultiSelectWidget(OrderedMultiSelectWidget):
    """ This class fixes an acquisition bug in
        zope.app.form.browser.itemswidgets.py line 556.

        itemswidgets.py has since been moved to zope.formlib, which is zope.ap, 
        zope2 and Acquisition agnostic, so I don't see how this fix (which uses
        'aq_base') can be contributed there since Acquisition (and aq_base)
        isn't a dependency of zope.formlib.

        Description of the bug:
        -----------------------
        The 'get' method on the 'speakers' List fields is called, which tries
        to see if there is a 'speakers' attribute on the add or edit view.
        In the case of (for example) slc.seminarportal, we have a folder named 
        'speakers' which is then sometimes erroneously returned 
        (because of Acquisition) which then causes chaos.
    """

    def selected(self):
        """Return a list of tuples (text, value) that are selected."""
        # Get form values
        values = self._getFormValue()
        # Not all content objects must necessarily support the attributes
        # XXX: Line below contains the bugfix. (aq_base)
        if hasattr(aq_base(self.context.context), self.context.__name__):
            # merge in values from content 
            for value in self.context.get(self.context.context):
                if value not in values:
                    values.append(value)

        terms = [self.vocabulary.getTerm(value)
                 for value in values]
        return [{'text': self.textForValue(term), 'value': term.token}
                for term in terms]

