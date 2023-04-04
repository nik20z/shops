

class Store:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "id": 'store_id',
            "name": 'name_',
            "address": 'address',
            "cityKey": 'city_key',
            "cityName": 'city_name',
            "type": 'type_',
            "lat": 'lat',
            "long": 'long',
            "opensAt": 'opens_at',
            "closesAt": 'closes_at',
            "isDefaultStore": 'is_default_store',
            "isEcomAvailable": 'is_ecom_available',
            "isPickupAvailable": 'is_pickup_available',
            "isDeliveryAvailable": 'is_delivery_available',
            "isLentaScanAvailable": 'is_lenta_scan_available',
            "is24hStore": 'is_24h_store',
            "hasPetShop": 'has_pet_shop',
            "division": 'division',
            "isFavorite": 'is_favorite',
            "minOrderSumm": 'min_order_summ',
            "maxOrderSumm": 'max_order_summ',
            "minDeliveryOrderSumm": 'min_delivery_order_summ',
            "maxDeliveryOrderSumm": 'max_delivery_order_summ',
            "maxWeight": 'max_weight',
            "maxDeliveryWeight": 'max_delivery_weight',
            "maxQuantityPerItem": 'max_quantity_per_item',
            "maxDeliveryQuantityPerItem": 'max_delivery_quantity_per_item',
            "orderLimitOverall": 'order_limit_overall',
            "deliveryOrderLimitOverall": 'delivery_order_limit_overall'
        }

        self.store_id: int = data_info['id']
        self.name_: str = data_info['name']
        self.address: str = data_info['address']
        self.city_key: str = data_info['cityKey']
        self.city_name: str = data_info['cityName']
        self.type_: str = data_info['type']
        self.lat: float = data_info['lat']
        self.long: float = data_info['long']
        self.opens_at: int = data_info['opensAt']
        self.closes_at: int = data_info['closesAt']
        self.is_default_store: bool = data_info['isDefaultStore']
        self.is_ecom_available: bool = data_info['isEcomAvailable']
        self.is_pickup_available: bool = data_info['isPickupAvailable']
        self.is_delivery_available: bool = data_info['isDeliveryAvailable']
        self.is_lenta_scan_available: bool = data_info['isLentaScanAvailable']
        self.is_24h_store: bool = data_info['is24hStore']
        self.has_pet_shop: bool = data_info['hasPetShop']
        self.division: str = data_info['division']
        self.is_favorite: bool = data_info['isFavorite']
        self.min_order_summ: int = data_info['minOrderSumm']
        self.max_order_summ: int = data_info['maxOrderSumm']
        self.min_delivery_order_summ: int = data_info['minDeliveryOrderSumm']
        self.max_delivery_order_summ: int = data_info['maxDeliveryOrderSumm']
        self.max_weight: int = data_info['maxWeight']
        self.max_delivery_weight: int = data_info['maxDeliveryWeight']
        self.max_quantity_per_item: int = data_info['maxQuantityPerItem']
        self.max_delivery_quantity_per_item: int = data_info['maxDeliveryQuantityPerItem']
        self.order_limit_overall: int = data_info['orderLimitOverall']
        self.delivery_order_limit_overall: int = data_info['deliveryOrderLimitOverall']
