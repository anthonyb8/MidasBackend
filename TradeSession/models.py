from django.db import models

# Temporary in-memory store
SESSION_DATA = {
    'positions': {},
    'orders': {},
    'account': {},
    'risk_model': {},
    'market_data': {}
}