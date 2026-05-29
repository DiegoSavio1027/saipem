import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Create PostgreSQL database if it does not exist'

    def handle(self, *args, **kwargs):
        # Get database configuration from settings
        db_config = settings.DATABASES['default']

        db_name = db_config['NAME']
        db_user = db_config['USER']
        db_password = db_config['PASSWORD']
        db_host = db_config['HOST']
        db_port = db_config['PORT']

        self.stdout.write(self.style.WARNING(f'Attempting to create database: {db_name}...'))

        try:
            # Connect to PostgreSQL default database (postgres)
            conn = psycopg2.connect(
                dbname='postgres',
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Check if database already exists
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            exists = cursor.fetchone()

            if exists:
                self.stdout.write(self.style.SUCCESS(f'✅ Database {db_name} already exists'))
            else:
                # Create database
                cursor.execute(f'CREATE DATABASE "{db_name}"')
                self.stdout.write(self.style.SUCCESS(f'✅ Database {db_name} created successfully'))

            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
            raise
