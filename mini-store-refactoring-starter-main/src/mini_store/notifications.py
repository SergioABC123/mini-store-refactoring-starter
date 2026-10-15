"""Customer notification behavior."""

from typing import Protocol


class NotificationChannel(Protocol):
    """Protocol defining the interface for customer notification channels."""

    def send_order_confirmation(self, customer, order_id: str) -> None:
        ...

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        ...


class EmailChannel:
    """Channel for sending notifications via email."""

    def __init__(self, email_sender):
        self.email_sender = email_sender

    def send_order_confirmation(self, customer, order_id: str) -> None:
        subject = f"Order {order_id} confirmed"
        message = f"Hello {customer.name}, your order {order_id} was confirmed."
        self.email_sender.send(customer.email, subject, message)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        subject = f"Order {order_id} shipped"
        message = (
            f"Hello {customer.name}, your order {order_id} shipped. "
            f"Tracking: {tracking_code}.\n"
            f"Tracking: {tracking_code}."
        )
        self.email_sender.send(customer.email, subject, message)


class SmsChannel:
    """Channel for sending notifications via SMS."""

    def __init__(self, sms_sender):
        self.sms_sender = sms_sender

    def send_order_confirmation(self, customer, order_id: str) -> None:
        message = f"Order {order_id} confirmed for {customer.name}."
        self.sms_sender.send(customer.phone, message)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        message = f"Order {order_id} shipped. Tracking: {tracking_code}."
        self.sms_sender.send(customer.phone, message)


class PushChannel:
    """Channel for sending push notifications to mobile devices."""

    def __init__(self, push_sender):
        self.push_sender = push_sender

    def send_order_confirmation(self, customer, order_id: str) -> None:
        title = "Order confirmed"
        message = f"Order {order_id} is confirmed."
        self.push_sender.send(customer.device_id, title, message)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        title = "Order shipped"
        message = f"Track order {order_id}: {tracking_code}."
        self.push_sender.send(customer.device_id, title, message)


class NotificationService:
    """Coordinates customer notifications across channels."""

    def __init__(
        self,
        email_sender,
        sms_sender,
        push_sender,
        channels: dict[str, NotificationChannel] | None = None,
    ):
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.push_sender = push_sender
        self._channels: dict[str, NotificationChannel] = channels or {
            "email": EmailChannel(email_sender),
            "sms": SmsChannel(sms_sender),
            "push": PushChannel(push_sender),
        }

    def _get_preferred_channel(self, customer) -> str:
        channel = customer.preferred_channel
        if channel not in self._channels:
            raise ValueError("Unsupported notification channel")
        return channel

    def _get_channel(self, customer) -> NotificationChannel:
        channel_name = self._get_preferred_channel(customer)
        return self._channels[channel_name]

    def send_order_confirmation(self, customer, order_id: str) -> None:
        channel = self._get_channel(customer)
        channel.send_order_confirmation(customer, order_id)

    def send_shipping_update(self, customer, order_id: str, tracking_code: str) -> None:
        channel = self._get_channel(customer)
        channel.send_shipping_update(customer, order_id, tracking_code)
