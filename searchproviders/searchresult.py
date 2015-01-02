
class SearchResult:
    """The result of a search provder"""

    def __init__(self, data, data_type=None, confidence=0.0, tostring=None):
        self.data = data
        self.data_type = data_type
        self.confidence = confidence
        self.tostring = None

    @property
    def ans(self):
        """Just to make it a little friendlier"""
        return str(self)

    @ans.setter
    def ans(self, value):
        """Just to make it a little friendlier"""
        data = value
        return

    def __str__(self):
        """If tostring is defined, use it, else just pass the data"""
        if self.tostring != None:
            return self.tostring()
        return str(self.data)
