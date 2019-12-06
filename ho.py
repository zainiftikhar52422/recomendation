import imdb
ia = imdb.IMDb()
movies = ia.get_movie('113497')
print(movies)