from ._getuser import *
from core.models import User


class Command(Command):
    help = 'specify username for activate user'

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        user = User.objects.get(username=options['username'])
        try:
            if not user.is_active:
                user.is_active = True
                user.save()
                print(self.style.SUCCESS(f'<{user}> is active now'))
            else:
                raise CommandError(self.style.ERROR(f'this user <{user}> be active already!!!'))
        except Exception as e:
            raise CommandError(e)




