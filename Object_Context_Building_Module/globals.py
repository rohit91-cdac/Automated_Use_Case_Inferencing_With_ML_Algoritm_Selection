
import os

LAYERS = [-1, -2, -3, -4]
NUM_TPU_CORES = 8
MAX_SEQ_LENGTH = 128
BERT_MODEL = 'uncased_L-12_H-768_A-12'
BERT_PRETRAINED_DIR = os.path.join(os.getcwd(), BERT_MODEL)
BERT_CONFIG = BERT_PRETRAINED_DIR + '/bert_config.json'
CHKPT_DIR = BERT_PRETRAINED_DIR + '/bert_model.ckpt'
VOCAB_FILE = BERT_PRETRAINED_DIR + '/vocab.txt'
INIT_CHECKPOINT = BERT_PRETRAINED_DIR + '/bert_model.ckpt'
BATCH_SIZE = 128
TPU_ADDRESS = 'grpc://' + os.environ['COLAB_TPU_ADDR']
