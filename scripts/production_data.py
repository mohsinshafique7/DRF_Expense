from django.core.management.utils import get_random_secret_key


def genrate_secret_key():
    secret_key = get_random_secret_key()
    print(f'SECRET_KEY:{secret_key}')


if __name__ == 'main':
    print()
    genrate_secret_key()
