from pathlib import Path

PROJECT_WAY = Path(__file__).parent.parent.parent


class LstmParams:
    WAY = PROJECT_WAY / 'data/models/lstm_sentiment_analysis.pt'
    OUTPUT_SIZE = 1
    EMBEDDING_DIM = 400
    HIDDEN_DIM = 512
    N_LAYERS = 2


class DataInfo:
    SEQ_LEN = 200
    BATCH_SIZE = 200
    WAY = PROJECT_WAY / 'data/info'
    TRAIN_FILE_WAY = PROJECT_WAY / 'data/amazon/train.ft.txt.bz2'
    TEST_FILE_WAY = PROJECT_WAY / 'data/amazon/test.ft.txt.bz2'
