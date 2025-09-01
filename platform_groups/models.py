import uuid

from django.db import models


class PlatformGroup(models.Model):
    class AccountStage(models.TextChoices):
        TRIAL = "trial"
        SINGLE = "single"
        DOUBLE = "double"
        TRIPLE = "triple"
        INSTANT = "instant"

    class AccountType(models.TextChoices):
        STANDARD = "standard"
        AGGRESSIVE = "aggressive"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)  # e.g. competition_001
    description = models.CharField(max_length=255, null=True, blank=True)
    platform_name = models.CharField(max_length=20, default="mt5")
    initial_balance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    account_stage = models.CharField(
        max_length=10,
        choices=AccountStage.choices,
        default=AccountStage.TRIAL,
    )
    account_type = models.CharField(
        max_length=10,
        choices=AccountType.choices,
        default=AccountType.STANDARD,
    )
    profit_target = models.IntegerField(default=0)
    profit_split = models.FloatField(default=0)
    max_drawdown = models.IntegerField(default=0)
    max_daily_drawdown = models.IntegerField(default=0)
    max_trading_days = models.IntegerField(default=0)
    account_leverage = models.IntegerField(default=0)
    prices = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "platform_groups"
