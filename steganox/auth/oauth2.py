"""
OAuth2 / SAML enterprise authentication — Phase 2 roadmap.
Placeholder for future implementation.
"""


class OAuth2Provider:
    """
    Future: OAuth2 integration with Okta, Azure AD, Google.
    See ROADMAP.md Phase 2 for implementation details.
    """

    def __init__(self, client_id: str, client_secret: str, server_metadata_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.server_metadata_url = server_metadata_url

    def get_authorization_url(self) -> str:
        raise NotImplementedError("OAuth2 integration coming in v2.0")

    def exchange_code_for_token(self, code: str) -> dict:
        raise NotImplementedError("OAuth2 integration coming in v2.0")
