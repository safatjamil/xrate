import base64


class EncodeDecode:

    def encode(string_):
        return base64.b64encode(string_.encode("ascii")).decode("ascii")
    
    def decode(string_):
        return base64.b64decode(string_.encode("ascii")).decode("ascii")