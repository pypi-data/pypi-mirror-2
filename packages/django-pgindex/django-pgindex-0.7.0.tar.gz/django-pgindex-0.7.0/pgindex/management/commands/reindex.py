import pgindex
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from optparse import make_option
from pgindex.models import Index


class Command(BaseCommand):
    help = _('Reindex for django-pgindex')

    option_list = BaseCommand.option_list + (
        make_option('--apps',
            action='store',
            dest='apps',
            default='',
            help=_('specify apps to reindex for.'),
            ),
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help=_('reindex all apps.'),
            )
        )
    def handle(self, *args, **options):
        registry = pgindex.helpers._registry
        if options['all']:
            Index._default_manager.all().delete()
        elif options['apps']:
            apps = [ app.strip() for app in options['apps'].split(',') ]
            Index._default_manager.filter(obj_app_label__in=apps).delete()
        else:
            raise CommandError(_('No apps to reindex.'))
        for model, idx_cls in registry.iteritems():
            app_label = model._meta.app_label
            if options['all'] or app_label in apps:
                print _('Reindexing %s') % app_label,
                for obj in model._default_manager.all():
                    idx = idx_cls(obj)
                    idx.update()
                print '\tOK'

