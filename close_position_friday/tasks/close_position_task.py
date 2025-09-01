import logfire


from datetime import datetime, timezone, timedelta
from equity_data_daily.models import EquityDataDaily
from django.utils.timezone import now
from django.db import transaction
from libs.client import Client
from platform_accounts.models import PlatformAccount
from advanced_challenge_settings.models import AdvancedChallengeSettings
from platform_groups.models import PlatformGroup

class InsertUserData:
    def __init__(self, platform_account, trade_group, equity, balance, prev_day_equity):
        self.platform_account = platform_account
        self.trade_group = trade_group
        self.equity = equity
        self.balance = balance
        self.prev_day_equity = prev_day_equity
client = Client()


def close_position_task():
    """Close position task that runs at friday"""
    try:
        logfire.info(f"Close position task started at {now()}")
        process_close_position(client)
    except Exception as e:
        logfire.error(f"Error in close_position_task", exc_info=True, extra={"error": str(e)})
        return f"Close position failed at {now()}"

    logfire.info(f"Close position completed at {now()}")  

def process_close_position(client: Client):
    logfire.info(f"Processing close position at {now()}")
    total_logins = get_login_list()
    print(total_logins)
    if not total_logins:
        logfire.error("No logins found", extra={"error": "No logins found"})
        return False
    account_numbers = total_logins
    print(account_numbers)

    execute_close_position(account_numbers)

def get_login_list():
    """
    Query advanced_challenge_settings filtered by close_all_positions_on_friday=True,
    get platform_group_uuid, then fetch platform_login_id from platform_accounts with status=1
    """
    try:
        # Step 1: Filter advanced_challenge_settings by close_all_positions_on_friday=True
        challenge_settings = AdvancedChallengeSettings.objects.filter(
            close_all_positions_on_friday=True
        ).select_related('platform_group')
        
        # Step 2: Extract platform_group_uuid values
        platform_group_uuids = [setting.platform_group.uuid for setting in challenge_settings]
        
        if not platform_group_uuids:
            logfire.warning("No platform groups found with close_all_positions_on_friday=True")
            return []
        
        # Step 3: Query platform_accounts using platform_group_uuid with status=1
        platform_accounts = PlatformAccount.objects.filter(
            platform_group__uuid__in=platform_group_uuids,
            status=1
        ).values_list('platform_login_id', flat=True)
        
        # Step 4: Convert to list of integers (platform_login_id values)
        login_ids = [int(login_id) for login_id in platform_accounts if login_id.isdigit()]
        
        logfire.info(f"Found {len(login_ids)} platform accounts for Friday position closure", extra={
            "platform_groups_count": len(platform_group_uuids),
            "login_ids_count": len(login_ids)
        })
        
        return login_ids
        
    except Exception as e:
        logfire.error(f"Error getting login list: {e}", exc_info=True)
        return []

def execute_close_position(trade_acc_data: list):       
        close_position = client.close_multiple_positions(trade_acc_data)
        print(close_position)
        if not close_position:
            logfire.error("Failed to close positions", extra={"error": "Failed to close positions"})
            return False
        logfire.info("Positions closed successfully", extra={"login_ids": trade_acc_data})
        return True


