"""Descriptors for XBlocks/Xmodules, that provide editing of atrributes"""


import logging

from xblock.fields import Scope, String

from xmodule.mako_module import MakoModuleDescriptor, MakoTemplateBlockBase

log = logging.getLogger(__name__)


class EditingFields:
    """Contains specific template information (the raw data body)"""
    data = String(scope=Scope.content, default='')


class EditingMixin(EditingFields, MakoTemplateBlockBase):
    """
    Module that provides a raw editing view of its data and children.  It does not
    perform any validation on its definition---just passes it along to the browser.

    This class is intended to be used as a mixin.
    """
    resources_dir = None

    mako_template = "widgets/raw-edit.html"

    @property
    def non_editable_metadata_fields(self):
        """
        `data` should not be editable in the Studio settings editor.
        """
        non_editable_fields = super().non_editable_metadata_fields
        non_editable_fields.append(self.fields['data'])
        return non_editable_fields

    # cdodge: a little refactoring here, since we're basically doing the same thing
    # here as with our parent class, let's call into it to get the basic fields
    # set and then add our additional fields. Trying to keep it DRY.
    def get_context(self):
        _context = MakoTemplateBlockBase.get_context(self)
        # Add our specific template information (the raw data body)
        _context.update({'data': self.data})
        return _context


class TabsEditingMixin(EditingFields, MakoTemplateBlockBase):
    """
    Common code between TabsEditingDescriptor and XBlocks converted from XModules.
    """

    mako_template = "widgets/tabs-aggregator.html"
    js_module_name = "TabsEditingDescriptor"
    tabs = []

    def get_context(self):
        _context = MakoTemplateBlockBase.get_context(self)
        _context.update({
            'tabs': self.tabs,
            'html_id': self.location.html_id(),  # element_id
            'data': self.data,
        })
        return _context


class TabsEditingDescriptor(TabsEditingMixin, MakoModuleDescriptor):  # lint-amnesty, pylint: disable=abstract-method
    """
    Module that provides a raw editing view of its data and children.  It does not
    perform any validation on its definition---just passes it along to the browser.

    This class is intended to be used as a mixin.

    Engine (module_edit.js) wants for metadata editor
    template to be always loaded, so don't forget to include
    settings tab in your module descriptor.
    """
    pass  # lint-amnesty, pylint: disable=unnecessary-pass
