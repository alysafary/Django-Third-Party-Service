from rest_framework.exceptions import APIException


class APINotFoundError(APIException):
    status_code = 400

    def __init__(self, detail="API not found"):
        self.default_code = "api_not_found"
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class APIKeyNotFoundError(APIException):
    status_code = 400

    def __init__(self, detail="APIKey is required"):
        self.default_code = "api_key_required"
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class IPAddressNotFoundError(APIException):
    status_code = 400

    def __init__(self, detail="IP address not found in request"):
        self.default_code = "ip_address_not_found"
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class ThirdPartyInvalidUsernameException(APIException):
    status_code = 400

    def __init__(self, detail="Please enter a valid Username"):
        self.default_code = "third_party_invalid_uuid"
        super().__init__(detail, self.default_code)
        self.default_detail = detail
