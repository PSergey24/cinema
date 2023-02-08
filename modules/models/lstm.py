import bz2
from collections import Counter
import re
import nltk
import ssl
import pickle
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')
# nltk.download()


class SentimentNet(nn.Module):
    def __init__(self, vocab_size, output_size, embedding_dim, hidden_dim, n_layers, drop_prob=0.5):
        super(SentimentNet, self).__init__()
        self.output_size = output_size
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, dropout=drop_prob, batch_first=True)
        self.dropout = nn.Dropout(0.2)
        self.fc = nn.Linear(hidden_dim, output_size)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x, hidden):
        batch_size = x.size(0)
        x = x.long()
        embeds = self.embedding(x)
        lstm_out, hidden = self.lstm(embeds, hidden)
        lstm_out = lstm_out.contiguous().view(-1, self.hidden_dim)

        out = self.dropout(lstm_out)
        out = self.fc(out)
        out = self.sigmoid(out)

        out = out.view(batch_size, -1)
        out = out[:, -1]
        return out, hidden

    def init_hidden(self, batch_size):
        device = torch.device("cpu")

        weight = next(self.parameters()).data
        hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device),
                  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device))
        return hidden


def made_prediction(comment):
    word2idx, test_sentences, test_labels = read_file()
    model = get_model(word2idx)

    seq_len = 200
    comment = clean_data(comment)
    comment = test_sentences_to_idx(comment, word2idx)
    comment = pad_input(comment, seq_len)

    prediction = predict_text(model, comment)
    return prediction


def get_model(word2idx):
    vocab_size = len(word2idx) + 1
    output_size = 1
    embedding_dim = 400
    hidden_dim = 512
    n_layers = 2

    model = SentimentNet(vocab_size, output_size, embedding_dim, hidden_dim, n_layers)
    model.load_state_dict(torch.load('data/models/lstm_sentiment_analysis.pt'))
    return model


def predict_text(model, text):
    device = torch.device("cpu")
    word_seq = np.array(text)
    pad = torch.from_numpy(word_seq)
    inputs = pad.to(device)
    batch_size = 1
    h = model.init_hidden(batch_size)
    h = tuple([each.data for each in h])
    output, h = model(inputs, h)
    return (output.item())


def test_lstm():
    comments = ['this is not very good movie', 'amazing, i want to watch next part',
                'great work, never seen same', 'i love leonardo dicaprio', 'normal movie, nothing special',
                'Ryan Gosling is a very talented actor. he often starred in melodramas. Girls love him',
                "I can't say that this is an outstanding picture. Many people will go to see this movie in theaters",
                'my brother will probably watch this movie', "this movie is shit, it shouldn't be shown to kids.",
                "movie is very violent", "There are many scenes of violence and murder in the film",
                "There are many scenes of violence and murder in the film. this is bad"]

    comments = clean_data(comments)
    word2idx, test_sentences, test_labels = read_file()
    comments_idx = test_sentences_to_idx(comments, word2idx)

    seq_len = 200
    test_sentences = pad_input(test_sentences, seq_len)
    comments_idx = pad_input(comments_idx, seq_len)

    # check_accuracy(test_sentences, test_labels, word2idx)
    check_comments(comments, comments_idx, word2idx)
    print(1)


def check_comments(comments, test_sentences, word2idx):
    model = get_model(word2idx)

    for i, item in enumerate(test_sentences):
        pred = predict_text(model, [item])
        print(f'{comments[i]}: {pred}')
    print(1)


def check_accuracy(test_sentences, test_labels, word2idx):
    num_correct = 0
    batch_size = 200
    test_losses = []

    model = get_model(word2idx)
    h = model.init_hidden(batch_size)
    model.eval()

    criterion = nn.BCELoss()

    test_labels = np.array(test_labels)
    test_data = TensorDataset(torch.from_numpy(test_sentences), torch.from_numpy(test_labels))
    test_loader = DataLoader(test_data, shuffle=True, batch_size=batch_size)

    device = torch.device("cpu")
    for inputs, labels in test_loader:
        h = tuple([each.data for each in h])
        inputs, labels = inputs.to(device), labels.to(device)
        output, h = model(inputs, h)
        test_loss = criterion(output.squeeze(), labels.float())
        test_losses.append(test_loss.item())
        pred = torch.round(output.squeeze())  # rounds the output to 0/1
        correct_tensor = pred.eq(labels.float().view_as(pred))
        correct = np.squeeze(correct_tensor.cpu().numpy())
        num_correct += np.sum(correct)

    print("Test loss: {:.3f}".format(np.mean(test_losses)))
    test_acc = num_correct / len(test_loader.dataset)
    print("Test accuracy: {:.3f}%".format(test_acc * 100))


def train_lstm():
    num_train = 80000
    num_test = 20000

    train_file, test_file = get_files(num_train, num_test)
    train_sentences, test_sentences = get_sentences(train_file, test_file)
    train_labels, test_labels = get_labels(train_file, test_file)
    train_sentences = clean_data(train_sentences)
    test_sentences = clean_data(test_sentences)

    del train_file, test_file
    print('data was cleaned')

    words = count_words(train_sentences, num_train)
    word2idx, idx2word = create_dictionary(words)
    print('dictionary was created')

    train_sentences = train_sentences_to_idx(train_sentences, word2idx)
    test_sentences = test_sentences_to_idx(test_sentences, word2idx)
    print('sentences to indexes')

    seq_len = 200
    train_sentences = pad_input(train_sentences, seq_len)
    test_sentences = pad_input(test_sentences, seq_len)
    print('added inputs')

    save_to_file(word2idx, test_sentences, test_labels)
    print('saved data')

    train_model(train_sentences, test_sentences, train_labels, test_labels, word2idx)


def get_files(num_train, num_test):
    train_file = bz2.BZ2File('data/amazon/train.ft.txt.bz2')
    test_file = bz2.BZ2File('data/amazon/test.ft.txt.bz2')

    train_file = train_file.readlines()
    test_file = test_file.readlines()

    print("Number of training reivews: " + str(len(train_file)))
    print("Number of test reviews: " + str(len(test_file)))

    train_file = [x.decode('utf-8') for x in train_file[:num_train]]
    test_file = [x.decode('utf-8') for x in test_file[:num_test]]
    return train_file, test_file


def get_sentences(train_file, test_file):
    train_sentences = [x.split(' ', 1)[1][:-1].lower() for x in train_file]
    test_sentences = [x.split(' ', 1)[1][:-1].lower() for x in test_file]
    return train_sentences, test_sentences


def get_labels(train_file, test_file):
    train_labels = [0 if x.split(' ')[0] == '__label__1' else 1 for x in train_file]
    test_labels = [0 if x.split(' ')[0] == '__label__1' else 1 for x in test_file]
    return train_labels, test_labels


def clean_data(input_sentences):
    # Some simple cleaning of data
    for i in range(len(input_sentences)):
        input_sentences[i] = re.sub('\d', '0', input_sentences[i])

    # Modify URLs to <url>
    for i in range(len(input_sentences)):
        if 'www.' in input_sentences[i] or 'http:' in input_sentences[i] or 'https:' in input_sentences[i] or '.com' in \
                input_sentences[i]:
            input_sentences[i] = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", "<url>", input_sentences[i])
    return input_sentences


def count_words(train_sentences, num_train):
    words = Counter()
    for i, sentence in enumerate(train_sentences):
        train_sentences[i] = []
        for word in nltk.word_tokenize(sentence):
            words.update([word.lower()])
            train_sentences[i].append(word)
        if i % 20000 == 0:
            print(str((i * 100) / num_train) + "% done")
    print("100% done")

    words = {k: v for k, v in words.items() if v > 1}
    words = sorted(words, key=words.get, reverse=True)
    words = ['_PAD', '_UNK'] + words
    return words


def create_dictionary(words):
    word2idx = {o: i for i, o in enumerate(words)}
    idx2word = {i: o for i, o in enumerate(words)}
    return word2idx, idx2word


def train_sentences_to_idx(train_sentences, word2idx):
    for i, sentence in enumerate(train_sentences):
        train_sentences[i] = [word2idx[word] if word in word2idx else word2idx['_UNK'] for word in sentence]
    return train_sentences


def test_sentences_to_idx(test_sentences, word2idx):
    idx_sentences = []
    for i, sentence in enumerate(test_sentences):
        idx_sentences.append([word2idx[word.lower()] if word.lower() in word2idx else word2idx['_UNK'] for word in
                             nltk.word_tokenize(sentence)])
    return idx_sentences


def pad_input(sentences, seq_len):
    features = np.zeros((len(sentences), seq_len), dtype=int)
    for ii, review in enumerate(sentences):
        if len(review) != 0:
            features[ii, -len(review):] = np.array(review)[:seq_len]
    return features


def save_to_file(word2idx, test_sentences, test_labels):
    data = [word2idx, test_sentences, test_labels]
    file = open('info', 'wb')
    pickle.dump(data, file)
    file.close()


def read_file():
    file = open('data/info', 'rb')
    data = pickle.load(file)
    file.close()
    return data[0], data[1], data[2]


def train_model(train_sentences, test_sentences, train_labels, test_labels, word2idx):
    train_labels = np.array(train_labels)
    test_labels = np.array(test_labels)

    split_frac = 0.5
    split_id = int(split_frac * len(test_sentences))
    val_sentences, test_sentences = test_sentences[:split_id], test_sentences[split_id:]
    val_labels, test_labels = test_labels[:split_id], test_labels[split_id:]

    train_data = TensorDataset(torch.from_numpy(train_sentences), torch.from_numpy(train_labels))
    val_data = TensorDataset(torch.from_numpy(val_sentences), torch.from_numpy(val_labels))
    test_data = TensorDataset(torch.from_numpy(test_sentences), torch.from_numpy(test_labels))

    batch_size = 200

    train_loader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
    val_loader = DataLoader(val_data, shuffle=True, batch_size=batch_size)
    test_loader = DataLoader(test_data, shuffle=True, batch_size=batch_size)

    is_cuda = torch.cuda.is_available()

    if is_cuda:
        device = torch.device("cuda")
        print("GPU is available")
    else:
        device = torch.device("cpu")
        print("GPU not available, CPU used")

    dataiter = iter(train_loader)
    sample_x, sample_y = next(dataiter)

    print(sample_x.shape, sample_y.shape)

    vocab_size = len(word2idx) + 1
    output_size = 1
    embedding_dim = 400
    hidden_dim = 512
    n_layers = 2

    model = SentimentNet(vocab_size, output_size, embedding_dim, hidden_dim, n_layers)
    model.to(device)
    print(model)

    lr = 0.005
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    epochs = 2
    counter = 0
    print_every = 2
    clip = 5
    valid_loss_min = np.Inf

    model.train()
    for i in range(epochs):
        h = model.init_hidden(batch_size)

        for inputs, labels in train_loader:
            counter += 1
            h = tuple([e.data for e in h])
            inputs, labels = inputs.to(device), labels.to(device)
            model.zero_grad()
            output, h = model(inputs, h)
            loss = criterion(output.squeeze(), labels.float())
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), clip)
            optimizer.step()

            if counter % print_every == 0:
                val_h = model.init_hidden(batch_size)
                val_losses = []
                model.eval()
                for inp, lab in val_loader:
                    val_h = tuple([each.data for each in val_h])
                    inp, lab = inp.to(device), lab.to(device)
                    out, val_h = model(inp, val_h)
                    val_loss = criterion(out.squeeze(), lab.float())
                    val_losses.append(val_loss.item())

                model.train()
                print("Epoch: {}/{}...".format(i + 1, epochs),
                      "Step: {}...".format(counter),
                      "Loss: {:.6f}...".format(loss.item()),
                      "Val Loss: {:.6f}".format(np.mean(val_losses)))
                if np.mean(val_losses) <= valid_loss_min:
                    torch.save(model.state_dict(), 'data/models/state_dict.pt')
                    print('Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(valid_loss_min,
                                                                                                    np.mean(
                                                                                                        val_losses)))
                    valid_loss_min = np.mean(val_losses)


