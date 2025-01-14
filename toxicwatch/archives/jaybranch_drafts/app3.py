from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField(validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print(form.errors)
    if request.method == 'POST':
        name=request.form['name']
        print(name)
 
        if form.validate():
            # Save the comment here.
            flash('Your phrase was: ' + name)
            flash("... and that's pretty neat!")
        else:
            flash('All the form fields are required. ')
 
    return render_template('index2.html', form=form)
 
if __name__ == "__main__":
    app.run()