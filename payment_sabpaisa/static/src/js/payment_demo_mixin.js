/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { rpc, RPCError } from "@web/core/network/rpc";

export default {

    /**
     * Send a URL-encoded request as a form submission and render the response.
     *
     * @private
     * @param {string} pg_url - The target URL.
     * @param {object} data_obj - The data object to be sent as URL-encoded.
     * @return {Promise<void>}
     */
    async sendFormRequest(pg_url, data_obj) {
        try {
            // Open a new tab
            const newTab = window.open("", "_blank");

            // Create a form element dynamically
            const form = document.createElement("form");
            form.method = "POST";
            form.action = pg_url;

            // Add form fields for each data key-value pair
            for (const [key, value] of Object.entries(data_obj)) {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = key;
                input.value = value;
                form.appendChild(input);
            }

            // Append the form to the new tab's document and submit it
            newTab.document.body.appendChild(form);
            form.submit();

            // Optionally, you can close the tab after submission if needed
            // newTab.close();  // Uncomment to close the tab after form submission

        } catch (error) {
            console.error("Error while sending the form request:", error);
        }
    },

    /**
     * Process a simulated payment and redirect the user.
     *
     * @private
     * @param {object} processingValues - The processing values of the transaction.
     * @return {Promise<void>}
     */
    async processDemoPayment(processingValues) {
        try {
            console.log("calling this function")

            const customerInput = document.getElementById("customer_input").value;
            console.log('got customer input')
            const simulatedPaymentState = document.querySelector("input[name='simulated_payment_state']").value;
            console.log('git simulated state')

            const response = await rpc("/payment/sabpaisa/simulate_payment", {
                reference: processingValues.reference,
                payment_details: customerInput,
                simulated_state: simulatedPaymentState,
            });

            console.log("RPC Response:", response);

            // Call the function to send the form request
            await this.sendFormRequest(response.url, {
                encData: response.enc_data,
                clientCode: response.client_code,
            });

            window.location = '/payment/status';


        } catch (error) {
            if (error instanceof RPCError) {
                this._displayErrorDialog(
                    _t("Payment processing failed"),
                    error.data.message
                );
            } else {
                console.error("Unexpected error:", error);
            }
        }
    },
};
