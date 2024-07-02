from flask import Flask, render_template, request, url_for, redirect, send_file
import matplotlib.pyplot as plt
import extract_data as ed
import numpy as np
import base64
import io

#? Server Details
app = Flask(__name__)

# Start server: python -m flask --app .\app.py run --debug

@app.route("/", methods=['GET', 'POST'])
def home():
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
        result = ed.get_data()
        names = [row[1] for row in result]
        
        #*  Return to view
        return render_template('index.html', names=names)
        

@app.route("/roomies/<int:user_id>/<int:roomies_quant>/match_result")
def graph_result(user_id : int, roomies_quant : int):
    try:
        #*  Get Relationship Data
        data = ed.get_realtionship(user_id, roomies_quant)
        graph_data = ed.format_to_graph(user_id, data)
        
        #* Extraer nombres y Scores
        inverted_roomies_name = np.array([row[1] for row in graph_data[1:]])
        roomies_name = inverted_roomies_name [::-1]
        
        inverted_tolerance_score  = np.array([row[-1] for row in graph_data[1:]])
        tolerance_score = inverted_tolerance_score [::-1]
        # print(graph_data, roomies_name, tolerance_score, sep="\n")
        
        # Create the plot in memory
        fig, ax = plt.subplots()  # Create figure and axes
        ax.barh(roomies_name, tolerance_score, color='skyblue')
        plt.xlim(0,1210)
        ax.set_xlabel('Puntaje Obtenido (x de 1210)')
        ax.set_ylabel('Nombres')

        # Convert plot to PNG image data
        img_data = io.BytesIO()
        fig.savefig(img_data, format='png')
        img_data.seek(0)  # Rewind the buffer

        # Encode image data in base64
        encoded_image = base64.b64encode(img_data.read()).decode('utf-8')
        
        for row in graph_data:
            row.insert(2, row.pop())
        
        # Prepare the view HTML
        return render_template('result.html', image_data=encoded_image, data=graph_data)
    except Exception as err:
        return err
    
    
if __name__ == '__main__':
    app.run(debug=True)