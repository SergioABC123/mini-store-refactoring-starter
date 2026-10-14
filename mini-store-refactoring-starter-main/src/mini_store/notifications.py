"""Customer notification behavior."""


class NotificationService:
    def __init__(self, email_sender, sms_sender, push_sender):
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.push_sender = push_sender

    def _get_preferred_channel(self, customer) -> str:
        channel = customer.preferred_channel
        if channel not in ("email", "sms", "push"):
            raise ValueError("Unsupported notification channel")
        return channel

    def send_order_confirmation(self, customer, order_id: str) -> None:
        channel = self._get_preferred_channel(customer)
        if channel == "email":
            subject = f"Order {order_id} confirmed"
            message = f"Hello {customer.name}, your order {order_id} was confirmed."
            self.email_sender.send(customer.email, subject, message)
        elif channel == "sms":
            message = f"Order {order_id} confirmed for {customer.name}."
            self.sms_sender.send(customer.phone, message)
        elif channel == "push":
            title = "Order confirmed"
            message = f"Order {order_id} is confirmed."
            self.push_sender.send(customer.device_id, title, message)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        channel = self._get_preferred_channel(customer)
        if channel == "email":
            subject = f"Order {order_id} shipped"
            message = (
                f"Hello {customer.name}, your order {order_id} shipped. "
                f"Tracking: {tracking_code}.\n"
                f"Tracking: {tracking_code}."
            )
            self.email_sender.send(customer.email, subject, message)
        elif channel == "sms":
            message = f"Order {order_id} shipped. Tracking: {tracking_code}."
            self.sms_sender.send(customer.phone, message)
        elif channel == "push":
            title = "Order shipped"
            message = f"Track order {order_id}: {tracking_code}."
            self.push_sender.send(customer.device_id, title, message)
