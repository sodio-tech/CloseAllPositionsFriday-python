import uuid

from django.db import models

from platform_accounts.models import PlatformAccount


class PeriodicTradingExport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    deal_id = models.BigIntegerField()
    position_id = models.BigIntegerField()
    deal_type = models.CharField(max_length=20)
    profit = models.FloatField()
    deal_time = models.DateTimeField()
    deal_entry = models.CharField(max_length=20)
    deal_price = models.FloatField()
    deal_symbol = models.CharField(max_length=30)
    deal_stoploss = models.FloatField(null=True, blank=True)
    deal_volume = models.FloatField(null=True, blank=True)
    deal_commission = models.FloatField(null=True, blank=True)
    deal_swap = models.FloatField(default=0)
    dupe_detected = models.BooleanField(default=False)

    platform_account = models.ForeignKey(
        PlatformAccount,
        on_delete=models.CASCADE,
        db_column="platform_account_uuid",
    )
    class Meta:
        db_table = "periodic_trading_export"
        unique_together = (("deal_id", "platform_account"),)
        indexes = [
            models.Index(fields=["deal_type"], name="pte_deal_type_idx"),
            models.Index(fields=["deal_entry"], name="pte_deal_entry_idx"),
            models.Index(fields=["platform_account"], name="pte_trading_acc_idx"),
        ]

    def __str__(self):
        return f"{self.deal_id}-{self.platform_account}"
