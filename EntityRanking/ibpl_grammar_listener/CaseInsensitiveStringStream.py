import antlr4


class CaseInsensitiveStringStream(antlr4.InputStream):
    def __init__(self, data=None, number_of_actual_chars_in_array=None):
        if data is not None:
            if isinstance(data, str):
                super().__init__(data)
            elif isinstance(data, list) and number_of_actual_chars_in_array is not None:
                # Convert list of chars to string up to the specified number of chars
                super().__init__("".join(data[:number_of_actual_chars_in_array]))
            else:
                raise ValueError("Invalid initialization parameters")
        else:
            super().__init__()

    def LA(self, i):
        if i == 0:
            return 0
        if i < 0:
            i += 1
            if (self._index + i - 1) < 0:
                return antlr4.Token.EOF
        if (self._index + i - 1) >= self.size:
            return antlr4.Token.EOF
        return ord(self.strdata[self._index + i - 1].lower())
