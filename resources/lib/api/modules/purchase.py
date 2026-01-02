from .base import BaseModule

class PurchaseModule(BaseModule):
    def available(self) -> list:
        """
        Get all media purchased
        """

        res = self.sender.req(endpoint="/user/purchased/medias")
        return res["data"]

    def use_ticket(self, item_id: int):
        """
        Rent media using a ticket
        """

        self.sender.req(endpoint="/user/tickets/activate", body={"id": item_id})
