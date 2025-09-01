import uuid

from django.db import models

from platform_accounts.models import PlatformAccount

class AccountStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(max_length=20, null=True)
    current_equity = models.FloatField(null=True)
    yesterday_equity = models.FloatField(null=True)
    performance_percent = models.FloatField(null=True)
    current_overall_drawdown = models.FloatField(null=True)
    current_daily_drawdown = models.FloatField(null=True)
    average_win = models.FloatField(null=True)
    average_loss = models.FloatField(null=True)
    hit_ratio = models.FloatField(null=True)
    best_trade = models.FloatField(null=True)
    worst_trade = models.FloatField(null=True)
    max_consecutive_wins = models.IntegerField(null=True)
    max_consecutive_losses = models.IntegerField(null=True)
    trades_without_stoploss = models.IntegerField(null=True)
    most_traded_asset = models.CharField(max_length=30, null=True)
    win_coefficient = models.FloatField(null=True)
    avg_win_loss_coefficient = models.FloatField(null=True)
    best_worst_coefficient = models.FloatField(null=True)
    maximum_daily_drawdown = models.FloatField(null=True)
    maximum_overall_drawdown = models.FloatField(null=True)
    consistency_score = models.FloatField(null=True)
    lowest_watermark = models.FloatField(null=True)
    highest_watermark = models.FloatField(null=True)
    current_balance = models.FloatField(null=True)
    current_profit = models.FloatField(null=True)

    platform_account = models.ForeignKey(
        PlatformAccount,
        on_delete=models.CASCADE,
        db_column="platform_account_uuid",
    )
    class Meta:
        db_table = "account_stats"

    def __str__(self):
        return str(self.platform_account)
