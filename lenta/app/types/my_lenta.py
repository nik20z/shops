

class MyLenta:

    def __init__(self, user_id: int, data_info: dict):
        self.data_info = data_info
        self.replace_keys = {
            "emailAddress": 'email_address',
            "emailConfirmed": 'email_confirmed',
            "hasLoyalty": 'has_loyalty',
            "isLoyaltyMember": 'is_loyalty_member',
            "isNewLoyaltyMember": 'is_new_loyalty_member',
            "loyaltyLevel": 'loyalty_level',
            "isUserPro": 'is_user_pro',
            "isBonusGameChoice": 'is_bonus_game_choice',
            "pushTokenChangeNeeded": 'push_token_change_needed'
        }

        self.user_id: int = user_id
        self.access_token: str
        self.refresh_token: str

        self.email_address: str = data_info['emailAddress']
        self.email_confirmed: bool = data_info['emailConfirmed']
        self.bonus_points: float = data_info['bonus']['points']
        self.bonus_expiration_date: str = data_info['bonus']['expirationDate']
        self.bonus_points_to_expire: float = data_info['bonus']['bonus']
        self.stamps_points: int = data_info['stamps']['points']
        self.stamps_daily_limit: int = data_info['stamps']['dailyLimit']
        self.stamps_total_limit: int = data_info['stamps']['dailyLimit']
        self.has_loyalty: bool = data_info['hasLoyalty']
        self.is_loyalty_member: bool = data_info['isLoyaltyMember']
        self.is_new_loyalty_member: bool = data_info['isNewLoyaltyMember']
        self.loyalty_level: int = data_info['loyaltyLevel']
        self.is_user_pro: bool = data_info['isUserPro']
        self.is_bonus_game_choice: bool = data_info['isBonusGameChoice']
        self.push_token_change_needed: bool = data_info['pushTokenChangeNeeded']
