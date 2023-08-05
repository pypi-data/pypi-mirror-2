import threading


class MessageHandler(object):

    def __init__(self):
        pass

    def get_type(self):
        return 'message'

    def handle(self, message):
        pass


class Message(object):

    def __init__(self):
        """
        >>> x = Message()
        >>> x.message is None
        True
        >>> x.event is not None
        True
        """
        self.event = threading.Event()
        self.message = None

    def __getattr__(self, name):
        """
        >>> x = Message()
        >>> x.set()
        >>> x.message
        """
        try:
            return getattr(self.event, name)
        except NameError:
            return super(self.__class__, self).__getattr__(name)

    def get_message(self):
        """
        >>> x = Message()
        >>> x.get_message()
        >>> x.set_message('hello, world')
        >>> x.isSet()
        True
        >>> x.get_message()
        'hello, world'
        >>> x.isSet()
        False
        """
        self.event.clear()
        return self.message

    def set_message(self, message):
        """
        >>> x = Message()
        >>> x.set_message('hello, world')
        >>> x.isSet()
        True
        """
        self.message = message
        self.event.set()
