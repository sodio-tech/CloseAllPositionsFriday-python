import uuid

from django.db import models

from platform_accounts.models import PlatformAccount


class EquityDataDaily(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    day = models.DateField(
        help_text="Date adjusted to correct timezone prior to saving"
    )
    created_date = models.DateTimeField(
        auto_now_add=True, help_text="Update time in UTC"
    )
    equity = models.FloatField()
    balance = models.FloatField()
    equity_eod_mt5 = models.FloatField(
        null=True, blank=True, help_text="Equity taken after the EOD from MT5"
    )
    platform_account = models.ForeignKey(
        PlatformAccount,
        on_delete=models.CASCADE,
        db_column="platform_account_uuid",
    )
    class Meta:
        db_table = "equity_data_daily"
        unique_together = (("platform_account", "day"),)
        indexes = [
            models.Index(fields=["platform_account"], name="eq_daily_trading_acc_idx"),
        ]

    def __str__(self):
        return f"{self.platform_account}-{self.day}"
