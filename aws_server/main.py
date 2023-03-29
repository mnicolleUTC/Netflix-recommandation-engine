from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)
URL_FAST_API = 'https://fastapideta-1-a3617093.deta.app/'

# Home route to display movie images
@app.route('/', methods=['GET', 'POST'])
def home():
    response = requests.get(URL_FAST_API)
    fastapi_data = json.loads(response.text)
    movie_titles = fastapi_data['Name']
    # Retrieve user id from api response
    user_id = list(fastapi_data["User_Id"].values())[0]
    # Use omdb API to get movie posters
    posters = []
    movie_titles_available = []
    predicted_score = []
    for title in movie_titles.values():
        url = f'http://www.omdbapi.com/?apikey=7e00c769&t={title}&plot=full'
        response = requests.get(url)
        json_data = response.json()
        # If key "error" exist in json_data dict then path to next movie because not found in omdb api
        if "Error" in json_data.keys():
            continue
        else:
            movie_titles_available.append(title)
            posters.append(json_data['Poster'])
            # Get index in our fastapi_data corresponding to a specific movie
            key = [x for x in fastapi_data['Name'].keys() if fastapi_data['Name'][x] == title][0]
            # Append predicted score
            predicted_score.append(round(fastapi_data['Estimate_Score'][key],2))

    # Render template with movie posters and form to fetch new movies
    return render_template('movies.html', posters=posters,\
                            movies = movie_titles_available,\
                            scores = predicted_score,
                            user_id = user_id)
                             

if __name__ == '__main__':
    app.run(debug=True)
