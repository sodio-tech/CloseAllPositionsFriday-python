import uuid

from django.db import models


class AdvancedChallengeSettings(models.Model):
   
    class TimeUnit(models.TextChoices):
        DAYS = "days"
        WEEKS = "weeks"
        MONTHS = "months"
        YEARS = "years"

    class BreachType(models.TextChoices):
        ACCOUNT_DELETION = "account_deletion"
        ACCOUNT_SUSPENSION = "account_suspension"
        WARNING = "warning"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Advanced challenge settings
    hundred_profit_split = models.BooleanField(default=False, db_column="100_profit_split")     
    two_percent_lower_target = models.BooleanField(default=False, db_column="2_percent_lower_target")
    two_percent_more_daily_drawdown = models.BooleanField(default=False, db_column="2_percent_more_daily_drawdown")
    two_percent_more_max_drawdown = models.BooleanField(default=False, db_column="2_percent_more_max_drawdown")
    allow_expert_advisors = models.BooleanField(default=False, db_column="allow_expert_advisors")
    breach_type = models.CharField(max_length=191, choices=BreachType.choices, null=True, blank=True, db_column="breach_type")
    close_all_positions_on_friday = models.BooleanField(default=False, db_column="close_all_positions_on_friday")
    delete_account_after_failure = models.IntegerField(null=True, blank=True, db_column="delete_account_after_failure")
    delete_account_after_failure_unit = models.CharField(max_length=50, choices=TimeUnit.choices, null=True, blank=True, db_column="delete_account_after_failure_unit")
    double_leverage = models.BooleanField(default=False, db_column="double_leverage")
    held_over_the_weekend = models.BooleanField(default=False, db_column="held_over_the_weekend")
    inactivity_breach_trigger = models.IntegerField(null=True, blank=True, db_column="inactivity_breach_trigger")
    inactivity_breach_trigger_unit = models.CharField(max_length=50, choices=TimeUnit.choices, null=True, blank=True, db_column="inactivity_breach_trigger_unit")
    max_open_lots = models.IntegerField(default=0, db_column="max_open_lots")
    max_risk_per_symbol = models.IntegerField(default=0, db_column="max_risk_per_symbol")
    max_time_per_evaluation_phase = models.IntegerField(null=True, blank=True, db_column="max_time_per_evaluation_phase")
    max_time_per_evaluation_phase_unit = models.CharField(max_length=50, choices=TimeUnit.choices, null=True, blank=True, db_column="max_time_per_evaluation_phase_unit")
    max_time_per_funded_phase = models.IntegerField(null=True, blank=True, db_column="max_time_per_funded_phase")
    max_time_per_funded_phase_unit = models.CharField(max_length=50, choices=TimeUnit.choices, null=True, blank=True, db_column="max_time_per_funded_phase_unit")
    max_trading_days = models.IntegerField(null=True, blank=True, db_column="max_trading_days")
    min_time_per_phase = models.IntegerField(null=True, blank=True, db_column="min_time_per_phase")
    min_time_per_phase_unit = models.CharField(max_length=50, choices=TimeUnit.choices, null=True, blank=True, db_column="min_time_per_phase_unit")
    no_sl_required = models.BooleanField(default=False, db_column="no_sl_required")
    requires_stop_loss = models.BooleanField(default=False, db_column="requires_stop_loss")
    requires_take_profit = models.BooleanField(default=False, db_column="requires_take_profit")
    time_between_withdrawals = models.IntegerField(null=True, blank=True, db_column="time_between_withdrawals")
    time_between_withdrawals_unit = models.CharField(max_length=50, choices=TimeUnit.choices, null=True, blank=True, db_column="time_between_withdrawals_unit")
    visible_on_leaderboard = models.BooleanField(default=False, db_column="visible_on_leaderboard")
    withdraw_within = models.IntegerField(null=True, blank=True, db_column="withdraw_within")
    withdraw_within_unit = models.CharField(max_length=50, choices=TimeUnit.choices, null=True, blank=True, db_column="withdraw_within_unit")
    
    # Foreign keys
    platform_group = models.ForeignKey(
        'platform_groups.PlatformGroup',
        on_delete=models.CASCADE,
        db_column="platform_group_uuid",
    )

    platform_account_uuid = models.ForeignKey(
        'platform_accounts.PlatformAccount', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        db_column="platform_account_uuid"
        )
    
    # Basic settings
    account_leverage = models.IntegerField(default=0, db_column="account_leverage")
    profit_split = models.IntegerField(default=0, db_column="profit_split")
    profit_target = models.IntegerField(default=0, db_column="profit_target")
    max_drawdown = models.IntegerField(default=0, db_column="max_drawdown")
    max_daily_drawdown = models.IntegerField(default=0, db_column="max_daily_drawdown")
    min_trading_days = models.IntegerField(null=True, blank=True, db_column="min_trading_days")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")

    class Meta:
        db_table = "advanced_challenge_settings"
