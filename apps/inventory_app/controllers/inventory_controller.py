from app.models.inventory_model import get_inventory_data

class InventoryController:
    @staticmethod
    def get_all_inventory():
        return get_inventory_data()
