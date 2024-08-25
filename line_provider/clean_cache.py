import os

# Очистите кэш переменных окружения
os.environ.pop('POSTGRES_LINE_PROVIDER_USER', None)
os.environ.pop('POSTGRES_LINE_PROVIDER_PASSWORD', None)
os.environ.pop('POSTGRES_LINE_PROVIDER_DB', None)
os.environ.pop('POSTGRES_LINE_PROVIDER_HOST', None)
os.environ.pop('POSTGRES_LINE_PROVIDER_PORT', None)

print(os.environ)