import warnings
import pandas as pd
warnings.filterwarnings("ignore")


def create_db():

    # df_titles = pd.read_csv('data/title.akas.tsv', sep='\t', on_bad_lines='skip')
    # df_people = pd.read_csv('data/name.basics.tsv', sep='\t', on_bad_lines='skip')
    # df_principals = pd.read_csv('data/title.principals.tsv', sep='\t', on_bad_lines='skip')
    df_rating = pd.read_csv('data/title.ratings.tsv', sep='\t', on_bad_lines='skip')
    df_title_basics = pd.read_csv('data/title.basics.tsv', sep='\t', on_bad_lines='skip')
    # df_title_crew = pd.read_csv('data/title.crew.tsv', sep='\t', on_bad_lines='skip')

    filtered_movie = df_title_basics[(df_title_basics['startYear'] != '\\N') & (df_title_basics['startYear'] >= '1985') & ((df_title_basics['titleType'] == 'tvSeries') | (df_title_basics['titleType'] == 'movie'))]

    data_movies = []
    columns_movies = ['id', 'tconst', 'name', 'year', 'isAdult', 'minutes', 'genres', 'type', 'rating', 'linkImg',
                      'description']
    data_principals = []
    columns_principals = ['id', 'tconst', 'nconst', 'category']
    data_people = []
    columns_people = ['id', 'nconst', 'name', 'birthYear', 'deathYear', 'profession', 'linkImg']
    index_principals = 0
    index_people = 0

    k = 0
    for i, row in filtered_movie.iterrows():
        rating = ''
        votes = 0

        data_rating = df_rating[df_rating['tconst'] == row['tconst']]
        if len(data_rating) != 0:
            rating = data_rating['averageRating'].item()
            votes = data_rating['numVotes'].item()

        if rating == '' or rating < 7.0 or votes < 20000:
            continue

        item_movie = [k, row['tconst'], row['primaryTitle'], row['startYear'], row['isAdult'], row['runtimeMinutes'],
                row['genres'], row['titleType'], rating, '', '']
        data_movies.append(item_movie)

        # principals = df_principals[df_principals['tconst'] == row['tconst']]
        # for j, principal in principals.iterrows():
        #     item_principal = [index_principals, principal['tconst'], principal['nconst'], principal['category']]
        #     data_principals.append(item_principal)
        #
        #     people = df_people[df_people['nconst'] == principal['nconst']]

            # actor = list(filter(lambda item: item[1] == people['nconst'].item(), data_people))

            # actor = [item for item in data_people if item[1] == people['nconst'].item()]
            # if len(actor) == 0:

            # item_people = [index_people, people['nconst'].item(), people['primaryName'].item(), people['birthYear'].item(),
            #                people['deathYear'].item(), people['primaryProfession'].item(), '']
            # data_people.append(item_people)
            #
            # index_principals += 1
            # index_people += 1

        print(f"{k}, {i}/{len(filtered_movie)}, {row['tconst']}, {row['primaryTitle']}")
        k += 1

        # if k > 5:
        #     break

    df_movie = pd.DataFrame(data_movies, [i for i in range(len(data_movies))], columns_movies)
    df_movie.to_csv('data/movies.csv', sep='\t')
    # df_principals = pd.DataFrame(data_principals, [i for i in range(len(data_principals))], columns_principals)
    # df_principals.to_csv('data/principals.csv', sep='\t')
    # df_people = pd.DataFrame(data_people, [i for i in range(len(data_people))], columns_people)
    # df_people.to_csv('data/people.csv', sep='\t')
