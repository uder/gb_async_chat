class MessageMapper(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._register()
