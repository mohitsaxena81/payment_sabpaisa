# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from urllib.parse import urljoin
from odoo.http import request
from odoo.addons.payment_sabpaisa.utils.pg_integration import PgService
from werkzeug.utils import redirect


class PaymentDemoController(http.Controller):
    _simulation_url = '/payment/sabpaisa/simulate_payment'
    _webhook_url = '/payment/sabpaisa/webhook'

    @http.route(_simulation_url, type='json', auth='user')
    def demo_simulate_payment(self, **data):
        """ Simulate the response of a payment request.

        :param dict data: The simulated notification data.
        :return: None
        """

        current_user =request.env.user
        user_name = current_user.name
        user_email = current_user.email
        user_phone = current_user.partner_id.phone or ''
        partner = current_user.partner_id

        street = partner.street or ''
        street2 = partner.street2 or ''
        city = partner.city or ''
        state = partner.state_id.name if partner.state_id else ''
        zip_code = partner.zip or ''
        country = partner.country_id.name if partner.country_id else ''


        full_address = f"{street}, {street2}, {city}, {state}, {zip_code}, {country}".strip(', ')



        base_url = request.httprequest.host_url

        full_url = urljoin(base_url,'/payment/sabpaisa/webhook')


        request.env['payment.transaction'].sudo()._handle_notification_data('sabpaisa', data)

        transaction = request.env['payment.transaction'].sudo().search([('reference', '=', data['reference'])], limit=1)


        provider = transaction.provider_id

        auth_key = provider.auth_key
        auth_iv = provider.auth_iv
        client_code = provider.client_code
        trans_user_name = provider.client_username
        trans_user_password = provider.client_password
        call_back_url = full_url
        pg_url = provider.pg_url
        pg_service = PgService(client_txn_id=data['reference'],client_code=client_code, auth_key=auth_key, auth_iv=auth_iv,
                               trans_user_name=trans_user_name,
                               trans_user_password=trans_user_password, call_back_url=call_back_url, pg_url=pg_url,
                               amount=transaction.amount,payer_name=user_name.split(' ')[0],payer_email=user_email,
                               payer_mobile = user_phone,payer_address=full_address)
        enc_data = pg_service.enc_data()


        return {
            'type': 'ir.actions.act_url',
            'url': pg_url,
            'target': 'new',
            'enc_data':enc_data,
            'client_code':client_code
        }

    @http.route(_webhook_url, type='http', auth='none',methods=['POST'],csrf=False)
    def webhook_payment(self, **data):
        request.env = request.env(user=request.env.ref('base.public_user').id)
        provider = request.env['payment.provider'].sudo().search([('code', '=', 'sabpaisa')], limit=1)
        auth_key = provider.auth_key
        auth_iv = provider.auth_iv
        client_code = provider.client_code
        trans_user_name = provider.client_username
        trans_user_password = provider.client_password
        pg_service = PgService( client_code=client_code, auth_key=auth_key,
                               auth_iv=auth_iv,
                               trans_user_name=trans_user_name,
                               trans_user_password=trans_user_password,
                              )
        dec_data = pg_service.dec_data(data['encResponse'].replace(" ", "+"))


        dict_data={k.split('=')[0]:k.split("=")[1] for k in dec_data}


        transaction = request.env['payment.transaction'].sudo().search([('reference', '=', dict_data['clientTxnId'])], limit=1)


        if dict_data.get('status')=='SUCCESS':
            dict_to_update = {'reference': dict_data['clientTxnId'], 'payment_details': '', 'simulated_state': 'done'}
            request.env['payment.transaction'].sudo()._handle_notification_data('sabpaisa', dict_to_update)
            transaction.write({
                'amount': dict_data.get('amount', 0),
                'paid_amount':dict_data.get('paidAmount',0),
                'sabpaisa_txn_id':dict_data.get('sabpaisaTxnId',None),
                'bank_txn_id':dict_data.get('bankTxnId',None)
            })

        elif dict_data.get('status')in ['FAILED','ABORTED']:
            dict_to_update = {'reference': dict_data['clientTxnId'], 'payment_details': '', 'simulated_state': 'cancel'}
            request.env['payment.transaction'].sudo()._handle_notification_data('sabpaisa', dict_to_update)


        if transaction:
            return request.redirect(f'/payment/sabpaisa/transaction/{transaction.id}')


    @http.route('/payment/sabpaisa/transaction/<int:transaction_id>', type='http', auth='none',csrf=False)
    def transaction_page(self, transaction_id, **kwargs):
        transaction = request.env['payment.transaction'].sudo().browse(transaction_id)
        if not transaction.exists():
            return request.render('payment_sabpaisa.transaction_not_found', {})

        # return request.render('payment_sabpaisa.transaction_details', {
        #     'transaction': transaction,
        # })

        return redirect('/payment/status')



