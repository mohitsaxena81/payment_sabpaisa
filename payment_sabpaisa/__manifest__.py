# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: Sabpaisa',
    'version': '2.0',
    'category': 'Invoicing',
    'sequence': 350,
    'summary': "A payment provider that covers India",
    'author':'sabpaisa',
    'website':'https://sabpaisa.in/payment-gateway/',
    'version': '18.0.0.1',
    'description': " ",  # Non-empty string to avoid loading the README file.
    'depends': ['payment', 'website'],
    'data': [
        'views/payment_demo_templates.xml',
        'views/payment_provider_views.xml',
        'views/payment_token_views.xml',
        'views/payment_transaction_views.xml',
        'views/transaction_custom_templates.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',  # Depends on `payment_method_demo`.
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_sabpaisa/static/src/js/**/*',
        ],
    },
    'license': 'LGPL-3',
    'external_dependencies': {
        'python': ['requests','pycryptodomex'],  # Add the required libraries here
    },
}



