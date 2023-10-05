class InputExample:

    def __init__(self, unique_id, unique_a, unique_b=None):
        self.unique_id = unique_id
        self.unique_a = unique_a
        self.unique_b = unique_b


class InputFeatures:
    """
    Features of the data to be used
    """

    def __init__(self, unique_id, tokens, input_ids, input_mask, input_type_ids):
        self.unique_id = unique_id
        self.tokens = tokens
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.input_type_ids = input_type_ids
