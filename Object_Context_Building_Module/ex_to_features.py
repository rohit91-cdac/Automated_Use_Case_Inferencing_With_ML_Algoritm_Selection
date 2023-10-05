from bert import  tokenization
import tensorflow as tf
from bert_input_example import InputFeatures


def convert_examples_to_features(examples, seq_length, tokenizer):
    """
    Loads data file into Input Batches
    :param examples:
    :param seq_length:
    :param tokenizer:
    :return:
    """

    features = []

    def _truncate_seq_pair(tokens_a, tokens_b, max_lenth):
        while True:
            total_length = len(tokens_a) + len(tokens_b)
            if total_length <= max_lenth:
                break
            if len(tokens_a) > len(tokens_b):
                tokens_a.pop()
            else:
                tokens_b.pop()

    for (ex_index, example) in enumerate(examples):
        tokens_a = tokenizer.tokenize(example.text_a)

        tokens_b = None
        if example.text_b:
            tokens_b = tokenizer.tokenize(example.text_b)

        if tokens_b:
            _truncate_seq_pair(tokens_a, tokens_b, seq_length - 3)
        else:
            if len(tokens_a) > seq_length - 2:
                tokens_a = tokens_a[0:(seq_length - 2 )]

        ################################################
        tokens = []
        input_type_ids = []
        tokens.append("[CLS]")
        input_type_ids.append(0)
        for token in tokens_a:
            tokens.append(token)
            input_type_ids.append(0)
        tokens.append("[SEP]")
        input_type_ids.append(0)

        if tokens_b:
            for token in tokens_b:
                tokens.append(token)
                input_type_ids.append(1)
            tokens.append("[SEP]")
            input_type_ids.append(1)

        input_ids = tokenizer.convert_tokens_to_ids(tokens)
        input_mask = [1] * len(input_ids)

        while len(input_ids) < seq_length:
            input_ids.append(0)
            input_mask.append(0)
            input_type_ids.append(0)

        assert len(input_ids) == seq_length
        assert len(input_mask) == seq_length
        assert len(input_type_ids) == seq_length

        if ex_index < 5:
            tf.compat.v1.logging.info("*** Example ***")
            tf.compat.v1.logging.info("unique_id: %s" % (example.unique_id))
            tf.compat.v1.logging.info("tokens: %s" % " ".join(
                [tokenization.printable_text(x) for x in tokens]))
            tf.compat.v1.logging.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            tf.compat.v1.logging.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            tf.compat.v1.logging.info(
                "input_type_ids: %s" % " ".join([str(x) for x in input_type_ids]))

        features.append(
            InputFeatures(
                unique_id=example.unique_id,
                tokens=tokens,
                input_ids=input_ids,
                input_mask=input_mask,
                input_type_ids=input_type_ids))

        return features