from modules.models.lstm import test_lstm
from modules.tools.db_filler import db_creator, csv_to_db, get_comments, get_users, get_movies, get_genres
from modules.tools.kaggle_movies_ds_to_csv import kaggle_movies_db_to_csv, update_info_kaggle_mdb_to_imdb, \
    kaggle_actors_db_to_csv, kaggle_rating_db_to_csv, fix_bugs, union_imdb_kaggle_ds
from modules.models.recommendation_systems import demographic_filtering


if __name__ == '__main__':
    # db_creator()
    # csv_to_db()

    # movies = get_movies()
    # genres = get_genres()
    # comments = get_comments()
    # users = get_users()

    # fix_bugs()
    # union_imdb_kaggle_ds()
    # kaggle_movies_db_to_csv()
    # kaggle_actors_db_to_csv()
    # kaggle_rating_db_to_csv()
    # update_info_kaggle_mdb_to_imdb()

    demographic_filtering()

    # train_lstm()
    # test_lstm()
    print('hello cinema')
