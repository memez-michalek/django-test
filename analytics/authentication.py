from rest_framework.authentication import TokenAuthentication

class BearerAuthentication(TokenAuthentication):
    keyword = 'bearer'

    def get_model(self):
        if self.model is not None:
            return self.model
        from analytics.models import Token
        return Token