from templates import *
from gw20e.forms.rendering.interfaces import IControlRenderer
from zope.interface import implements


class SelectAllRenderer:

    implements(IControlRenderer)

    def render(self, renderer, form, renderable, out, **kwargs):

        fmtmap = renderer.createFormatMap(form, renderable, **kwargs)

        fmtmap['value'] = form.data[renderable.bind] or ""

        print >> out, CONTROL_HDR % fmtmap
        print >> out, SELECT_ALL_HDR_TPL % fmtmap

        value = form.data[renderable.bind]

        for opt in renderable.options:

            optfmt = renderer.createFormatMap(form, opt)
            optfmt.update({"id":renderable.id})

            if hasattr(value, "__iter__") and opt.value in value:
                optfmt.update({'checked': 'checked="yes"'})
            elif opt.value == value:
                optfmt.update({'checked': 'checked="yes"'})                
            else:
                optfmt.update({'checked': ""})
                
            print >> out, CHECK_TPL % optfmt

        print >> out, SELECT_ALL_FTR_TPL % fmtmap
        print >> out, CONTROL_FTR

