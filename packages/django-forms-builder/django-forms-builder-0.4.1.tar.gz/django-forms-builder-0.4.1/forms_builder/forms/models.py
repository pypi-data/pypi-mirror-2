
from datetime import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext, ugettext_lazy as _

from forms_builder.forms.settings import FIELD_MAX_LENGTH, LABEL_MAX_LENGTH, \
    USE_SITES, CHOICES_QUOTE, CHOICES_UNQUOTE


STATUS_DRAFT = 1
STATUS_PUBLISHED = 2
STATUS_CHOICES = (
    (STATUS_DRAFT, "Draft"), 
    (STATUS_PUBLISHED, "Published"),
)

sites_field = None
if USE_SITES:
    import sys
    from django.contrib.sites.models import Site
    kwargs = {}
    if not (len(sys.argv) >= 2 and sys.argv[1] == "syncdb"):
        sites = Site.objects.all()
        if len(sites) == 1:
            kwargs["default"] = (sites[0].id,)
    sites_field = models.ManyToManyField(Site, **kwargs)

FIELD_CHOICES = (
    ("CharField", _("Single line text")),
    ("CharField/django.forms.Textarea", _("Multi line text")),
    ("EmailField", _("Email")),
    ("BooleanField", _("Check box")),
    ("MultipleChoiceField/django.forms.CheckboxSelectMultiple", 
        _("Check boxes")),
    ("ChoiceField", _("Drop down")),
    ("MultipleChoiceField", _("Multi select")),
    ("ChoiceField/django.forms.RadioSelect", _("Radio buttons")),
    ("FileField", _("File upload")),
    ("DateField/django.forms.extras.SelectDateWidget", _("Date")),
    ("DateTimeField", _("Date/time")),
    ("CharField/django.forms.HiddenInput", _("Hidden")),
)

class FormManager(models.Manager):
    """
    Only show published forms for non-staff users.
    """
    def published(self, for_user=None):
        if for_user is not None and for_user.is_staff:
            return self.all()
        return self.filter( 
            Q(publish_date__lte=datetime.now()) | Q(publish_date__isnull=True), 
            Q(expiry_date__gte=datetime.now()) | Q(expiry_date__isnull=True),
            Q(status=STATUS_PUBLISHED))

######################################################################
#                                                                    #
#   Each of the models are implemented as abstract to allow for      #
#   subclassing. Default concrete implementations are then defined   #
#   at the end of this module.                                       #
#                                                                    #
######################################################################

class AbstractForm(models.Model):
    """
    A user-built form.
    """

    sites = sites_field
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(editable=False, max_length=100, unique=True)
    intro = models.TextField(_("Intro"))
    button_text = models.CharField(_("Button text"), max_length=50, 
        default=_("Submit"))
    response = models.TextField(_("Response"))
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, 
        default=STATUS_PUBLISHED)
    publish_date = models.DateTimeField(_("Published from"), 
        help_text=_("With published selected, won't be shown until this time"),
        blank=True, null=True)
    expiry_date = models.DateTimeField(_("Expires on"), 
        help_text=_("With published selected, won't be shown after this time"),
        blank=True, null=True)
    login_required = models.BooleanField(_("Login required"), 
        help_text=_("If checked, only logged in users can view the form"))
    send_email = models.BooleanField(_("Send email"), default=True, help_text=
        _("If checked, the person entering the form will be sent an email"))
    email_from = models.EmailField(_("From address"), blank=True, 
        help_text=_("The address the email will be sent from"))
    email_copies = models.CharField(_("Send copies to"), blank=True, 
        help_text=_("One or more email addresses, separated by commas"), 
        max_length=200)
    email_subject = models.CharField(_("Subject"), max_length=200, blank=True)
    email_message = models.TextField(_("Message"), blank=True)

    objects = FormManager()

    class Meta:
        verbose_name = _("Form")
        verbose_name_plural = _("Forms")
        abstract = True
    
    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Create a unique slug from title - append an index and increment if it 
        already exists.
        """
        if not self.slug:
            self.slug = slugify(self.title)
            i = 0
            while True:
                if i > 0:
                    if i > 1:
                        self.slug = self.slug.rsplit("-", 1)[0]
                    self.slug = "%s-%s" % (self.slug, i)
                if not self.__class__.objects.filter(slug=self.slug):
                    break
                i += 1
        super(AbstractForm, self).save(*args, **kwargs)
        
    @models.permalink
    def get_absolute_url(self):
        return ("form_detail", (), {"slug": self.slug})

    def admin_link_view(self):
        url = self.get_absolute_url()
        return "<a href='%s'>%s</a>" % (url, ugettext("View on site"))
    admin_link_view.allow_tags = True
    admin_link_view.short_description = ""

    def admin_link_export(self):
        url = reverse("admin:form_export", args=(self.id,))
        return "<a href='%s'>%s</a>" % (url, ugettext("Export entries"))
    admin_link_export.allow_tags = True
    admin_link_export.short_description = ""
    
class FieldManager(models.Manager):
    """
    Only show visible fields when displaying actual form..
    """
    def visible(self):
        return self.filter(visible=True)

class AbstractField(models.Model):
    """
    A field for a user-built form.
    """
    
    label = models.CharField(_("Label"), max_length=LABEL_MAX_LENGTH)
    field_type = models.CharField(_("Type"), choices=FIELD_CHOICES, 
        max_length=55)
    required = models.BooleanField(_("Required"), default=True)
    visible = models.BooleanField(_("Visible"), default=True)
    choices = models.CharField(_("Choices"), max_length=1000, blank=True, 
        help_text="Comma separated options where applicable. If an option "
            "itself contains commas, surround the option starting with the %s"
            "character and ending with the %s character." % 
                (CHOICES_QUOTE, CHOICES_UNQUOTE))
    default = models.CharField(_("Default value"), blank=True, 
        max_length=FIELD_MAX_LENGTH)
    help_text = models.CharField(_("Help text"), blank=True, max_length=100)
        
    objects = FieldManager()

    class Meta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")
        abstract = True
    
    def __unicode__(self):
        return self.label

    def get_choices(self):
        """
        Parse a comma separated choice string into a list of choices taking 
        into account quoted choices using the ``CHOICES_QUOTE`` and 
        ``UNCHOICES_QUOTE`` settings.
        """
        choice = ""
        quoted = False
        for char in self.choices:
            if not quoted and char == CHOICES_QUOTE:
                quoted = True
            elif quoted and char == CHOICES_UNQUOTE:
                quoted = False
            elif char == "," and not quoted:
                choice = choice.strip()
                if choice:
                    yield choice, choice
                choice = ""
            else:
                choice += char
        choice = choice.strip()
        if choice:
            yield choice, choice

class AbstractFormEntry(models.Model):
    """
    An entry submitted via a user-built form.
    """

    entry_time = models.DateTimeField(_("Date/time"))
    
    class Meta:
        verbose_name = _("Form entry")
        verbose_name_plural = _("Form entries")
        abstract = True
    
class AbstractFieldEntry(models.Model):
    """
    A single field value for a form entry submitted via a user-built form.
    """
    
    field_id = models.IntegerField()
    value = models.CharField(max_length=FIELD_MAX_LENGTH)

    class Meta:
        verbose_name = _("Form field entry")
        verbose_name_plural = _("Form field entries")
        abstract = True

###################################################
#                                                 #
#   Default concrete implementations are below.   #
#                                                 #
###################################################

class Form(AbstractForm):
    pass

class Field(AbstractField):
    form = models.ForeignKey("Form", related_name="fields")
    class Meta:
        order_with_respect_to = "form"

class FormEntry(AbstractFormEntry):
    form = models.ForeignKey("Form", related_name="entries")

class FieldEntry(AbstractFieldEntry):
    entry = models.ForeignKey("FormEntry", related_name="fields")
