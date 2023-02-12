from modules.models.lstm import test_lstm
from modules.tools.db_filler import db_creator, movies_csv_to_db, get_comments, get_users


if __name__ == '__main__':
    # db_creator()
    # movies_csv_to_db()
    # movies = get_movies()
    # genres = get_genres()
    # comments = get_comments()
    users = get_users()

    # train_lstm()
    # test_lstm()
    print('hello cinema')
