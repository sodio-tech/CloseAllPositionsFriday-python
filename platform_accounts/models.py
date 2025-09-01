import uuid

from django.db import models

from platform_groups.models import PlatformGroup


class PlatformAccount(models.Model):
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

    user_uuid = models.UUIDField()

    purchase_uuid = models.UUIDField()

    platform_group = models.ForeignKey(
        PlatformGroup,
        on_delete=models.CASCADE,
        db_column="platform_group_uuid",
    )

    platform_login_id = models.CharField(max_length=255, default="0")
    platform_name = models.CharField(max_length=255, default="mt5")
    remote_group_name = models.CharField(max_length=50, default="0")
    current_phase = models.IntegerField(default=0)

    main_password = models.CharField(max_length=255, default="password")
    investor_password = models.CharField(max_length=255, default="password")

    initial_balance = models.DecimalField(max_digits=8, decimal_places=2)
    profit_target = models.IntegerField(default=0)
    profit_split = models.FloatField(default=0)
    max_drawdown = models.IntegerField(default=0)
    max_daily_drawdown = models.IntegerField(default=0)

    account_stage = models.CharField(
        max_length=10,
        choices=AccountStage.choices,
        null=True,
        blank=True,
    )
    account_type = models.CharField(
        max_length=10,
        choices=AccountType.choices,
        null=True,
        blank=True,
    )
    account_leverage = models.IntegerField(default=0)

    status = models.PositiveSmallIntegerField(
        default=1, db_index=True
    )  # 0: inactive, 1: active

    funded_at = models.DateTimeField(null=True, blank=True, db_index=True)
    # is_contract_sign = models.BooleanField(default=False)
    is_trades_check = models.BooleanField(default=False)
    # contract_sign_id = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "platform_accounts"

        indexes = [
            models.Index(fields=["platform_name"]),
        ]
