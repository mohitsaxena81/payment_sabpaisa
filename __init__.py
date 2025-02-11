# Part of Odoo. See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models
import subprocess,sys
from odoo.addons.payment import setup_provider, reset_payment_provider

REQUIRED_LIBRARIES = ['pycryptodomex']

def install_libraries():
    for library in REQUIRED_LIBRARIES:
        try:
            __import__(library)
        except ImportError:
            print(f"Installing missing library: {library}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

install_libraries()


def post_init_hook(env):
    setup_provider(env, 'sabpaisa')


def uninstall_hook(env):
    reset_payment_provider(env, 'sabpaisa')
