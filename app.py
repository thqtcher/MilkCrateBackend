import mc_recommendations as mc_recommendations
from flask import Flask

app = Flask(__name__)

@app.route('/')
def runApp():
    results = mc_recommendations.give_me_recs()
    df_json = results.to_json()
    return df_json

if __name__ == 'main':
    app.run()