from typing import Any, Dict, Optional
import requests
import json

class WhatsApp:

    """
    A class for sending WhatsApp messages using the Meta Business API.

    Attributes:
        url (str): The API endpoint URL.
        meta_token (str): The Meta Business API token.
        wapaId (str): The WhatsApp Business API ID.
        phone_number_prefix (str): The phone number prefix to use when sending messages.
    """

    def __init__(self, url, meta_token, wapaId, phone_number_prefix = "+91"):
        self.url = url
        self.token = meta_token
        self.wapaId = wapaId
        self.phone_number_prefix = phone_number_prefix

    def _create_headers(self) -> Dict[str, str]:
        """
        Creates the authorization headers for the API request.

        Returns:
            Dict[str, str]: The headers for the API request.
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _create_data(
        self,
        to: str,
        template_name: str,
        template_params: Dict[str, Any],
        language_code: str,
        data_type: str,
        recipient_type: str = "individual"
    ) -> Dict[str, Any]:
        """
        Creates the data for the API request.

        Args:
            to (str): The recipient phone number.
            template_name (str): The template name.
            template_params (Dict[str, Any]): The template parameters.
            language_code (str): The language code.
            data_type (str): The data type (e.g. "template" or "text").
            recipient_type (str): The recipient type.

        Returns:
            Dict[str, Any]: The data for the API request.
        """
        components = template_params if template_params else []

        if not all(isinstance(comp, dict) for comp in components):
            raise ValueError(
                "Each component in 'template_params' must be a JSON object."
            )

        return {
            "messaging_product": "whatsapp",
            "wabaId": self.wapaId,
            "recipient_type": recipient_type,
            "to": (self.phone_number_prefix + to) if not to.startswith("+") else to,
            "type": data_type,
            data_type: {
                "name": template_name,
                "language": {"code": language_code},
                "components": components,
            },
        }

    def _send_request(self, data: Dict[str, Any]) -> requests.Response:
        """
        Sends the API request.

        Args:
            data (Dict[str, Any]): The data for the API request.

        Returns:
            requests.Response: The response from the API.
        """
        headers = self._create_headers()
        response = requests.post(self.url, headers=headers, data=json.dumps(data))
        return response

    def send_message(
        self,
        recipient_phone: str,
        template_name: str,
        data_type: str = "template",
        components: Dict[str, Any] = None,
        language_code: str = "en",
        success_message: str = "Message sent successfully.",
        failed_message: str = "Failed to send message.",
    ) -> Dict[str, Optional[str]]:
        """
        Sends a WhatsApp message using the Meta Business API.

        Args:
            recipient_phone (str): The recipient phone number.
            template_name (str): The template name.
            data_type (str): The data type (e.g. "template" or "text").
            components (Dict[str, Any]): The template parameters.
            language_code (str): The language code.
            success_message (str): The message to return when the message is sent successfully.
            failed_message (str): The message to return when the message fails to be sent.

        Returns:
            Dict[str, Optional[str]]: A dictionary containing the status and message of the API request.
        """
        recipient_phone = str(recipient_phone).lstrip('0')
        data = self._create_data(
            recipient_phone,
            template_name,
            components,
            language_code,
            data_type,
        )
        try:
            response = self._send_request(data)
            response_data = response.json()
            if response.status_code == 200:
                if "messages" in response_data and response_data["messages"]:
                    first_message = response_data["messages"][0]
                    request_id = first_message.get("id")
                    message_status = (
                        "sent"
                        if first_message.get("message_status") == "accepted"
                        else "failed"
                    )
                    return {
                        "status": True,
                        "message": success_message,
                        "request_id": request_id,
                        "message_status": message_status,
                    }
                else:
                    return {
                        "status": True,
                        "message": "Message sent, but no message details found.",
                    }
            else:
                error_message = response_data.get("error", {}).get(
                    "message", failed_message
                )
                print(f"Failed to send message: {error_message}")
                return {"status": False, "message": error_message}

        except (requests.RequestException, ValueError) as e:
            print(f"Error sending message: {str(e)}")
            return {"status": False, "message": str(e)}
