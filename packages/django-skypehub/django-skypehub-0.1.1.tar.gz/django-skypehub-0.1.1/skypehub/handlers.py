from skypehub.models import Message

def message_logging_receiver(handler, message, status):
    Message.objects.create(
        body=message.Body,
        sender=message.Sender.Handle,
        chat_name=message.Chat.Name,
    )

class OnMessageHandler(object):
    """
    Skype OnMessage event handler
    """
    default_statuses = ('RECEIVED',)
    default_receivers = ()

    def __init__(self, skype=None):
        self.receivers = list(self.default_receivers)
        self.skype = skype

    def connect(self, receiver, statuses=None):
        if statuses is None:
            statuses = list(self.default_statuses)
        if not receiver in self.receivers:
            self.receivers.append((statuses, receiver))

    def dispatch(self, message, status):
        for statuses, receiver in self.receivers:
            if status in statuses:
                receiver(self, message, status)

on_message = OnMessageHandler()
on_message.connect(message_logging_receiver)
