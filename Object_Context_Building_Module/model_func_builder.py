import tensorflow as tf
from bert import modeling


def input_fn_builder(features, seq_length):
    """
    Creates an `input_fn` closure to be passed
    :param features:
    :param seq_length:
    :return:
    """

    all_unique_ids = []
    all_input_ids = []
    all_input_mask = []
    all_input_type_ids = []

    for feature in features:
        all_unique_ids.append(feature.unique_id)
        all_input_ids.append(feature.input_ids)
        all_input_mask.append(feature.input_mask)
        all_input_type_ids.append(feature.input_type_ids)

    def input_fn(params):
        """
        The input function which processes the Inputs
        :param params:
        :return:
        """

        batch_size = params["batch_size"]
        num_examples = len(features)

        d = tf.data.Dataset.from_tensor_slices({
            "unique_ids":
                tf.constant(all_unique_ids, shape=[num_examples], dtype=tf.int32),
            "input_id":
                tf.constant(
                    all_input_ids, shape=[num_examples, seq_length], dtype=tf.int32
                ),
            "input_mask":
                tf.constant(
                    all_input_mask, shape=[num_examples, seq_length], dtype=tf.int32
                ),
            "input_type_ids":
                tf.constant(
                    all_input_type_ids, shape=[num_examples, seq_length], dtype=tf.int32
                )
        })

        d = d.batch(batch_size=batch_size, drop_remainder=False)

        return d

    return input_fn


def model_fn_builder(bert_config, init_checkpoint, layer_indexes, use_tpus, use_one_hot_embeddings):
    """
    Returns the Model Function for Estimator
    :param bert_config:
    :param init_checkpoint:
    :param layer_indexes:
    :param use_tpus:
    :param use_one_hot_encodings:
    :return:
    """

    def model_fn(features, labels, mode, params):
        """
        The model_fn
        :param features:
        :param labels:
        :param mode:
        :param params:
        :return:
        """

        unique_ids = features["unique_ids"]
        input_ids = features["input_ids"]
        input_mask = features["input_mask"]
        input_type_ids = features["input_type_ids"]

        model = modeling.BertModel(
            config=bert_config,
            is_training=False,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=input_type_ids,
            use_one_hot_embeddings=use_one_hot_embeddings
        )
        if mode != tf.estimator.ModeKeys.PREDICT:
            raise ValueError("Only PREDICT modes are supported: %s" % (mode))

        tvars = tf.compat.v1.trainable_variables()
        scaffold_fn = None

        (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                   init_checkpoint)

        if use_tpus:

            def tpu_scaffold():
                tf.compat.v1.train.init_from_checkpoint(init_checkpoint, assignment_map)
                return tf.compat.v1.train.Scaffold()

            scaffold_fn = tpu_scaffold()
        else:
            tf.compat.v1.train.init_from_checkpoint(init_checkpoint, assignment_map)

        tf.compat.v1.logging.info("******** Trainable Variables **********")
        for var in tvars:
            init_string = ""
            if var.name in initialized_variable_names:
                init_string = ", *INIT_FROM_CKPT*"
            tf.compat.v1.logging.info(" name=%s, shape= %s%s", var.name, var.shape, init_string)

        all_layers = model.get_all_encoder_layers()

        predictions = {
            "unique_id": unique_ids
        }

        for (i, layer_index) in enumerate(layer_indexes):
            predictions["layer_output_%d" % i] = all_layers[layer_index]

        output_spec = tf.compat.v1.estimator.tpu.TPUEstimatorSpec(
            mode=mode, predictions=predictions, scaffold_fn=scaffold_fn
        )
        tf.compat.v1.config.con
        return output_spec

    return model_fn
