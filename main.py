from modules.tools.db_filler import db_creator, movies_csv_to_db, get_movies, get_genres
from modules.models.lstm import train_lstm, test_lstm


if __name__ == '__main__':
    # db_creator()
    # movies_csv_to_db()
    # movies = get_movies()
    # genres = get_genres()

    # train_lstm()
    test_lstm()
    print('hello cinema')
