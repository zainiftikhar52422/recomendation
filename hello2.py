from flask import Flask, redirect, url_for, request , render_template
app = Flask(__name__)
# import important libraries 
import pandas as pd    # for handling excel file and making dataFrames
import math
import imdb            # for movies thumbnail

pd_final=pd.read_csv('ml-latest-small/finalized ratings.csv')
def DataInDataFrame(queyMovieName):
    numberOfRows,_=(pd_final.shape)
    query_movie=list(pd_final.iloc[pd_final.loc[pd_final['movie name']==queyMovieName].index[0]])  # will get row of query movie
    print(query_movie)
    query_movie.pop()    #poping movie name from that row
    distanceList=list()
    for i in range(numberOfRows):
        movie=list(pd_final.iloc[pd_final.loc[pd_final['movie name']==pd_final.loc[i,"movie name"]].index[0]])
        movie.pop()     #poping the title 
        d=eucaldainDistance(query_movie,movie)
        distanceList.append((d,i,pd_final.loc[i,"movie name"],pd_final.loc[i,"ratings"],pd_final.loc[i,"arating"]))
    print("ends")
    return distanceList
# function for calculating eucaldian distance between two movies

def eucaldainDistance(x,y):
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return distance  
    


    

@app.route('/<movieName>')  
def main(movieName):
    #ia = imdb.IMDb()           #imdb object for extracting movie image link
    pd_movies=pd.read_csv('ml-latest-small/movies.csv')     #pandas read movies file and store it as data frame
    searchedMovieGenres=(list(pd_movies.iloc[pd_movies.loc[pd_movies['title']==movieName].index[0]]))[2]  #extracting genres
    #searchedMovieId=(list(pd_movies.iloc[pd_movies.loc[pd_movies['title']==movieName].index[0]]))[0]    #extracting searched movieId
    #searchedImdId=(list(pd_links.iloc[pd_links.loc[pd_links['movieId']==searchedMovieId].index[0]]))[1] #extracting imdbId from links file using movieId 
    #seachedMovieImageLink=(ia.get_movie(searchedImdId))['cover url']     #coverUrl of searched movie
    searchedMovieRatings=list(pd_final.iloc[pd_final.loc[pd_final['movie name']==movieName].index[0]])[-3]
    searchedMovieaRating=list(pd_final.iloc[pd_final.loc[pd_final['movie name']==movieName].index[0]])[-2]
    searchedMovieDetail={
        "title":movieName,
        #"thumbnail":seachedMovieImageLink,
        "simpleRating":searchedMovieRatings,
        "arating":searchedMovieaRating,
        "genres":searchedMovieGenres,
    }
    distanceList=DataInDataFrame(movieName)     #function for recomended movies
    #sort in ascending order and pick most 10 related movies
    distanceList = sorted(distanceList)[:5]   
    print(distanceList)
    

    recomendedMovies=list()  
    for movie in distanceList:
        genres=(list(pd_movies.iloc[pd_movies.loc[pd_movies['title']==movie[2]].index[0]]))[2]  #extracting genres
        #movieId=(list(pd_movies.iloc[pd_movies.loc[pd_movies['title']==movie[2]].index[0]]))[0]
        #imdId=(list(pd_links.iloc[pd_links.loc[pd_links['movieId']==movieId].index[0]]))[1] #extracting imdbId from links file using movieId 
        #movieDetail = ia.get_movie(imdId)
        #print("end heress",movieDetail)
        recomendedMovies.append({
            #"thumbnail":movieDetail['cover url'],
            "title": movie[2],
            "rating":movie[3],
            "arating":movie[4],
            "distance":movie[0],
            "genres":genres,
        })
    #print(recomendedMovies)
    return render_template("doc.html",recomendedMovies=recomendedMovies,searchedMovieDetail=searchedMovieDetail)

@app.route('/')
def start():
    return render_template("start.html")
if __name__ == '__main__':
   app.run(debug = True)