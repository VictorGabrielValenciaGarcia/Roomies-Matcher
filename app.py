from flask import Flask, render_template, request, url_for, redirect, send_file
import matplotlib.pyplot as plt
import extract_roomies_data as erd
import extract_accidents_data as ead
import numpy as np
import base64
import io

#? Server Details
app = Flask(__name__)

# Start server: python -m flask --app .\app.py run --debug

# ?* Default Routes
@app.route("/")
def home():
    return render_template('index.html')

# ?* Roomies Routes
@app.route("/roomies", methods=['GET', 'POST'])
def roomies():
    if request.method == 'POST':
        
        #*  Get Data Form
        user_base = request.form['user_base']
        roomies = request.form['roomies']

        #*  Redirect to Graph View
        if user_base and roomies:
            # print(f'''
            #     Result:
            #         user => '{user_base}'
            #         cnt roomies => '{roomies}'
            # ''')
            return redirect(url_for('graph_result', user_id=int(user_base), roomies_quant=int(roomies)))        
    else:
        #*  Get users name
        result = erd.get_data()
        names = [row[1] for row in result]
        
        #*  Return to view
        return render_template('roomies/form.html', names=names)
        

@app.route("/roomies/<int:user_id>/<int:roomies_quant>/match_result")
def graph_result(user_id : int, roomies_quant : int):
    try:
        #*  Get Relationship Data
        data = erd.get_realtionship(user_id, roomies_quant)
        graph_data = erd.format_to_graph(user_id, data)
        
        #* Extraer nombres y Scores
        inverted_roomies_name = np.array([row[1] for row in graph_data[1:]])
        roomies_name = inverted_roomies_name [::-1]
        
        inverted_tolerance_score  = np.array([row[-1] for row in graph_data[1:]])
        tolerance_score = inverted_tolerance_score [::-1]
        # print(graph_data, roomies_name, tolerance_score, sep="\n")
        
        #* Creamos las bases de la Grafica
        fig, ax = plt.subplots()  # Create figure and axes
        ax.barh(roomies_name, tolerance_score, color='skyblue')
        plt.xlim(0,1210)
        ax.set_xlabel('Puntaje Obtenido (x de 1210)')
        ax.set_ylabel('Nombres')

        #  Convertimos la Grafica en un formato PNG
        img_data = io.BytesIO()
        fig.savefig(img_data, format='png')
        img_data.seek(0) 

        # Encode image en base64
        encoded_image = base64.b64encode(img_data.read()).decode('utf-8')
        
        for row in graph_data:
            row.insert(2, row.pop())
        
        # Regresamos a la vista
        return render_template('roomies/result.html', image_data=encoded_image, data=graph_data)
    except Exception as err:
        return err
    
# ?* Accidents Routes
@app.route("/accidents", methods=['GET', 'POST'])
def accidents():
        
    if request.method == 'POST':
        #*  Get Data Form
        region = request.form['region']
        periodo = request.form['periodo']
        
        #*  Redirect to Graph View
        if region and periodo:
            return redirect(url_for('graph_accidents', region_name=region, period_name=periodo))    
        
    else:
        
        data_form = ead.get_form_data()
    
        regions = data_form[0]
        periods = data_form[2]
        
        return render_template('accidents/graph.html', regions = regions, periods = periods)
    
@app.route("/accidents/<region_name>/<period_name>/result")
def graph_accidents(region_name, period_name):
    try:
        accidents_data = ead.get_graph_data(region_name, period_name)
        
        trimesters = list(accidents_data.keys())
        accidents_values = list(accidents_data.values())
        
        #* Creamos las bases de la Grafica
        fig, ax = plt.subplots()  # Create figure and axes
        ax.bar(trimesters, accidents_values, color='skyblue')
        plt.grid(True)
        ax.set_xlabel('Trimestre')
        ax.set_ylabel("Número de Accidentes")
        
        #  Convertimos la Grafica en un formato PNG
        img_data = io.BytesIO()
        fig.savefig(img_data, format='png')
        img_data.seek(0) 

        # Encode image en base64
        encoded_image = base64.b64encode(img_data.read()).decode('utf-8')
        
        # Return the template with the image data
        return render_template('accidents/result.html', image_data=encoded_image, region_name=region_name, period_name=period_name, trimesters=trimesters, accidents_values=accidents_values)
    except Exception as err:
        return err

# ?* Extras
if __name__ == '__main__':
    app.run(debug=True)