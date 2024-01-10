from flask import Flask, render_template, request, url_for
import numpy as np
import cv2

from PIL import Image

app = Flask(__name__)


import tensorflow as tf

model = tf.keras.models.load_model('model\save.h5')
model.summary()




@app.route('/')
def index():
    return render_template('t1.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        photo = request.files['photo']

        # Save the uploaded file to the 'uploads' directory
        photo_path = f'static/{photo.filename}'
        photo.save(photo_path)

        # Generate the correct URL for the uploaded photo
        photo_url = url_for('static', filename=photo.filename)

       
       


        path = photo_path

        img = Image.open(path)



        new_size = (224, 224)
        im = img.resize(new_size)




        img = np.array(im) / 255.

        img.shape

        img = img[np.newaxis, ...]

        armax=np.argmax(model.predict(img))

        val = model.predict(img)
        valpred = val[0].tolist()


        array1=np.sort(model.predict(img))
        sorted = array1[0].tolist()
        sorted.reverse()

        
        rounded_list = [round(value, 2) for value in sorted]
        
        percentage_list = [value * 100 for value in rounded_list]


        pieces = ["Queen","Rook","Bishop","Knight","Pawn"]
        
        setpieces =[]
        for i in sorted:
            setpieces.append(pieces[valpred.index(i)])




        

















        return f'<html><body> \
        <style>body{{\
        background-image: url({ url_for("static", filename="background.jpg") }); background-size: cover; background-position: center; height: 100vh; margin: 0; font-family: \'Arial\', sans-serif; font-size: 26px; color: #FF0000; }} h1 {{ color: #ffc107; text-align: center; margin-top: 50px; }}</style>\
        <center>\
                <h1>Chess Pieces Classification</h1>\
        <img src={photo_url} width=224,height=224>\
        <br><h2>{pieces[armax]}</h2><br>\
        <table border="1" style="font-size: 22px"><tr><th>Piece</th><th>Probabilty(%)</th></tr></tr><tr><td>{setpieces[0]}</td><td>{percentage_list[0]}</td></tr><tr><td>{setpieces[1]}</td><td>{percentage_list[1]}</td></tr><tr><td>{setpieces[2]}</td><td>{percentage_list[2]}</td></tr><tr><td>{setpieces[3]}</td><td>{percentage_list[3]}</td></tr><tr><td>{setpieces[4]}</td><td>{percentage_list[4]}</td></tr></table>\
        </center>\
        </body></html>' 



    return 'No file uploaded.'

if __name__ == '__main__':
    app.run(debug=True)
