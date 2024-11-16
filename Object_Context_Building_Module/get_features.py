from globals import LAYERS, BERT_CONFIG, VOCAB_FILE, NUM_TPU_CORES, MAX_SEQ_LENGTH, INIT_CHECKPOINT, BATCH_SIZE
from bert import modeling, tokenization
import tensorflow as tf
from read_sequence import  read_sequence
from ex_to_features import convert_examples_to_features
from model_func_builder import model_fn_builder, input_fn_builder
import collections
import numpy as np


def get_features(input_text, dim=768):
    layer_indexes = LAYERS

    bert_config = modeling.BertConfig.from_json_file(BERT_CONFIG)

    tokenizer = tokenization.FullTokenizer(
        vocab_file=VOCAB_FILE, do_lower_case=True
    )

    is_per_host = tf.compat.v1.estimator.tpu.InputPipelineConfig.PER_HOST_V2
    tpu_cluster_resolver = tf.distribute.cluster_resolver.TPUClusterResolver(TPU_ADDRESS)
    run_config = tf.contrib.tpu.RunConfig(
        cluster=tpu_cluster_resolver,
        tpu_config=tf.contrib.tpu.TPUConfig(
            num_shards=NUM_TPU_CORES,
            per_host_input_for_training=is_per_host))

    examples = read_sequence(input_text)

    features =  convert_examples_to_features(
        examples=examples, seq_length=MAX_SEQ_LENGTH, tokenizer=tokenizer
    )

    unique_id_to_feature = {}
    for feature in features:
        unique_id_to_feature[feature.unique_id] = feature


    model_fn = model_fn_builder(
        bert_config=bert_config,
        init_checkpoint=INIT_CHECKPOINT,
        layer_indexes=layer_indexes,
        use_tpus=True,
        use_one_hot_embeddings=True
    )

    # If TPU is not available, this will fall back to normal Estimator on CPU or CPU
    estimator = tf.compat.v1.estimator.tpu.TPUEstimator(
        use_tpu=True,
        model_fn=model_fn,
        config=run_config,
        predict_batch_size=BATCH_SIZE,
        train_batch_size=BATCH_SIZE
    )

    input_fn = input_fn_builder(
        features=features, seq_length=MAX_SEQ_LENGTH
    )

    # GET Features
    for result in estimator.predict(input_fn, yield_single_examples=True):
        unique_id = int(result["unique_id"])
        feature = unique_id_to_feature[unique_id]
        output = collections.OrderedDict()
        for (i, token) in enumerate(feature.tokens):
            layers = []
            for (j, layer_index) in enumerate(layer_indexes):
                layer_output = result["layer_output_%d" % j]
                layer_output_flat = np.array([x for x in layer_output[i:(i + 1)].flat])
                layers.append(layer_output_flat)
            output[token] = sum(layers)[:dim]

        return output


if __name__ == "__main__":
    get_embedding = get_features(input_text="I wish to fight a war")
    print(get_embedding)
