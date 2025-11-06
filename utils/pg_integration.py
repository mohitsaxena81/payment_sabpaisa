import datetime
from odoo.addons.payment_sabpaisa.utils.auth_sabpaisa import AESCipher


class PgService:

    def __init__(self, client_code=None, trans_user_name=None, trans_user_password=None, auth_key=None, auth_iv=None,
                 call_back_url=None, pg_url=None,client_txn_id=None,amount=None,payer_name=None,
                 payer_email=None,payer_mobile=None,payer_address=None
                 ):
        self.client_code = client_code
        self.trans_user_name = trans_user_name
        self.trans_user_password = trans_user_password
        self.auth_key = auth_key
        self.auth_iv = auth_iv
        self.call_back_url = call_back_url
        self.pg_url = pg_url
        self.client_txn_id = client_txn_id
        self.amount=amount
        self.payer_name=payer_name
        self.payer_email = payer_email
        self.payer_mobile = payer_mobile
        self.payer_address = payer_address


    def create_pg_url(self, url_data):
        print("url data: ", url_data)
        clientTxnId = self.client_txn_id
        payerName = self.payer_name
        payerMobile = self.payer_mobile
        payerEmail = "anand.rathore@sabpaisa.in"
        payerAddress = "New Delhi"
        amount = self.amount
        callbackUrl = self.call_back_url

        spURL = "payerName=" + payerName + "&payerEmail=" + payerEmail + "&payerMobile=" + payerMobile + "&clientTxnId=" + clientTxnId + "&amount=" + amount + "&clientCode=" + self.clientCode + "&transUserName=" + self.transUserName + "&transUserPassword=" + self.transUserPassword + "&callbackUrl=" + callbackUrl + "&amountType=" + "INR"

        # spURL = (
        #         "?clientName="
        #         + self.clientCode
        #         + "&usern="
        #         + self.transUserName
        #         + "&pass="
        #         + self.transUserPassword
        #         + "&amt="
        #         + "1.00"
        #         + "&txnId="
        #         + clientTxnId
        #         + "&firstName="
        #         + payerFirstName
        #         + "&lstName="
        #         + payerLastName
        #         + "&contactNo="
        #         + payerContact
        #         + "&Email="
        #         + payerEmail
        #         + "&Add="
        #         + payerAddress
        #         + "&callbackUrl="
        #         + callbackUrl
        # )

        spURL = AESCipher(self.authKey, self.authIV).encrypt(spURL)
        spURL = spURL.decode("utf-8")
        spURL = spURL.replace("+", "%2B")
        spURL = "&query=" + spURL + "&clientCode=" + self.clientCode
        spURL = self.spDomain + spURL
        return spURL

    def enc_data(self):

        client_txn_id = self.client_txn_id
        payer_name = self.payer_name
        payer_mobile = self.payer_mobile
        payer_email = self.payer_email
        payer_address = self.payer_address
        amount = str(self.amount)
        callback_url = self.call_back_url



        end_data = "payerName=" + payer_name + "&payerEmail=" + payer_email + "&payerMobile=" + payer_mobile + \
                   "&clientTxnId=" + client_txn_id + "&amount=" + amount + "&clientCode=" + self.client_code + \
                   "&transUserName=" + self.trans_user_name + "&transUserPassword=" + self.trans_user_password + \
                   "&callbackUrl=" + callback_url + "&amountType=" + "INR" + "&channelId=W"

        end_data = AESCipher(self.auth_key, self.auth_iv).encrypt(end_data)
        #end_data = end_data.decode("utf-8")
        return end_data

    def dec_data(self, enc_response):
        dec_data = AESCipher(self.auth_key, self.auth_iv).decrypt(enc_response)

        print("dec response: ", dec_data)
        return dec_data.split("&")
