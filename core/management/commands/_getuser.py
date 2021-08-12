from abc import ABC
from argparse import ArgumentParser
from django.core.management import BaseCommand, CommandError
from core.models import User


class Command(BaseCommand, ABC):
    def add_arguments(self, parser):
        parser.add_argument('username', metavar='USERNAME')

    def handle(self, *args, **options):
        pass

