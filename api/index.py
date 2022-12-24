import music.mc_recommendations as mc_recommendations
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADER'] = 'Content-Type'
#revert
@app.route('/form')
@cross_origin()
def show_form():
    
    return render_template('form.html')

    


@app.route('/process', methods=['POST', 'GET'])
@cross_origin()
def process_input():
    #print("here")
    #print(request.form)
    input_value = request.form['input']
    
    parts = input_value.split('/')
    playlist_id = parts[-1]
    parts = playlist_id.split('?')
    playlist_id = parts[0]

    

    results = mc_recommendations.give_me_recs(input_value)
    df_json = results.to_json()
    #print(len(df_json))
    return df_json




if __name__ == 'main':
    app.run()
