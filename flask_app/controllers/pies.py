from flask_app import app
from flask import render_template,redirect,request,session, flash 
from flask_app.models import pie
import os
from flask_app import app
from flask_app.models.user import User
from datetime import datetime

from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from .env import ADMINEMAIL
from .env import PASSWORD


@app.route('/add_pie', methods=['POST'])
def add_pie():
    #if 'user_id' in session:
        #if not request.files['image']:
            #flash('Please include an image!', 'postImage')
            #return redirect(request.referrer)
   
        #image = request.files['image']
        #if not allowed_file(image.filename):
            #flash('Image should be in png, jpg, jpeg format!', 'postImage')
            #return redirect(request.referrer)
        
        #if image and allowed_file(image.filename):
            #filename1 = secure_filename(image.filename)
            #time = datetime.now().strftime("%d%m%Y%S%f")
            #time += filename1
            #filename1 = time
            #image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

    if pie.Pie.validate_pie(request.form):
        data = {
            'name': request.form['name'],
            'filling': request.form['filling'],
            'crust': request.form['crust'],
            'baker_id': session['user_id'], 
            #'image': filename1
        }
        print(data)
        pie.Pie.save(data)
        return redirect('/dashboard')
    return redirect('/dashboard')

@app.route('/pies')
def show_pies():
    return render_template('pie_derby.html', pies = pie.Pie.get_all())

@app.route('/show/<int:id>')
def pie_card(id):
    return render_template('pie_card.html', pie = pie.Pie.get_one({'id':id}))

@app.route('/like/<int:pie_id>', methods=['POST'])
def like(pie_id):
    data = {
        'id': pie_id,
        'consumer_id': session['user_id']
    }
    pie.Pie.like(data)
    return redirect(f'/show/{pie_id}')
    
@app.route('/dislike/<int:pie_id>', methods=['POST'])
def dislike(pie_id):
    data = {
        'id': pie_id
    }
    pie.Pie.dislike(data)
    return redirect(f'/show/{pie_id}')

@app.route('/edit/<int:id>')
def edit(id):
    return render_template('edit.html', this_pie = pie.Pie.get_one({'id': id}))

@app.route('/edit_pie/<int:id>', methods=['POST'])
def edit_pie(id):
    data = {
        'id' : id,
        'name': request.form['name'],
        'filling': request.form['filling'],
        'crust': request.form['crust']
    }
    pie.Pie.edit(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    pie.Pie.delete({'id': id})
    return redirect('/dashboard')
