from django.apps import AppConfig


class BankAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bank_app"

    def ready(self):
        from exalt_hexarch.containers import Container

        self.container = Container()
        self.container.wire(
            modules=[
                "bank_app.application.adapter.api.views.bank_account",
                "bank_app.application.adapter.api.views.bank_account_overdraft",
            ]
        )
