from django import forms
from django.template import Template
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from contentmanager import registry
from contentmanager.plugins import BasePlugin, BaseModelPlugin

class BackToTop(BasePlugin):
    def render(self, request):
        return render_to_string("basicblocks/backtotop.html")

class ParagraphForm(forms.Form):
    markup = forms.ChoiceField(
        choices=[(x,x) for x in ("markdown", "restructuredtext", "textile")],
        )
    title  = forms.CharField(required=False)
    text   = forms.CharField(widget=forms.Textarea()) 

class Paragraph(BasePlugin):
    form = ParagraphForm
    help = """
    Choose your markup syntax and type away. More information about
    the options can be found here: <a target="_blank"
    href="http://en.wikipedia.org/wiki/Textile_(markup_language)">Textile</a>,
    <a target="_blank"
    href="http://en.wikipedia.org/wiki/Markdown">Markdown</a> or <a
    target="_blank"
    href="http://en.wikipedia.org/wiki/ReStructuredText">restructuredtext
    (reST)</a>.
    """
    verbose_name = 'Paragraph'

    def render(self, request):
        template_name = 'basicblocks/paragraph_%s.html' % self.params['markup']
        return render_to_string(template_name, self.params)


class LoremForm(forms.Form):
    show = forms.IntegerField(
        help_text=_("How many paragraphs do you want to show?"),
        initial=3,
        min_value=1,
        max_value=5,
        required=True)


class LoremGenerator(BasePlugin):
    form = LoremForm
    verbose_name = "Lorem ipsum"

    def render(self, request):
        show = self.params['show']
        template = "{% load webdesign %}{% lorem "+str(show)+" p %}"
        return Template(template).render({})


class HTMLForm(forms.Form):
    html = forms.CharField(widget=forms.Textarea())


class HTML(BasePlugin):
    form = HTMLForm
    verbose_name = "Html"
    help = _("You can enter raw html here. Be aware that incorrect HTML can make you site misbehave!")

    def render(self, request):
        return self.params['html']

## registry ##
registry.register(Paragraph)
registry.register(BackToTop)
registry.register(LoremGenerator)
registry.register(HTML)
