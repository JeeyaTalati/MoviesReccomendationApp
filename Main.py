from crypt import methods
from flask import Flask, jsonify
from Storage import all_movies, liked_movies, not_liked_movies, did_not_watch
from demographic_filtering import output
from content_based_filtering import get_recommendations 

app = Flask(__name__)

@app.route("/")
def home():
    return "Movie Recommendation App"

@app.route("/get-movies")
def get_movies():
    movie_data = {
        "title": all_movies[0][7],
        "release_date": all_movies[0][13],
        "duration": all_movies[0][15],
        "rating": all_movies[0][20],
        "overview": all_movies[0][8]
    }
    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/liked-movies", methods= ["POST"])
def liked_movies():
    movie = all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status": "success"
    })
    
    
@app.route("/not-liked-movies",methods=["POST"])
def not_liked_movies():
    movie=all_movies[0]
    not_liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status":"success"
    })
    
@app.route("/did-not-watch", methods=["POST"])
def did_not_watch():
    movie=all_movies[0]
    did_not_watch.append(movie)
    all_movies.pop(0)
    return jsonify({
        "status":"success"
    })


@app.route("/popular-movies")
def popular_movies():
    movie_data = []
    for movie in output:
        d = {
        "title": movie[0],
        "release_date": movie[1] or "N/A",
        "duration": movie[2],
        "rating": movie[3],
        "overview": movie[4] 
        }
        movie_data.append(d)

    return jsonify({
        "data": movie_data,
        "status": "success"
    })


@app.route("/recommended-movies")
def recommended_movies():
    all_recommended = []
    for movie in liked_movies:
        output = get_recommendations(movie)
        for data in output: 
            all_recommended.append(data)

    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended, _ in itertools.groupby(all_recommended) )
    movie_data = []
    for movie in all_recommended:
        d = {
        "title": movie[0],
        "release_date": movie[1] or "N/A",
        "duration": movie[2],
        "rating": movie[3],
        "overview": movie[4] 
        }
        movie_data.append(d)

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

if __name__ == "__main__":
    app.run(debug = True)