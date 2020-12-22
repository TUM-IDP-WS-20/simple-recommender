from flask import Flask, request, jsonify, render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = TextAreaField('Input text:', validators=[validators.required()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    print(form.errors)
    if request.method == 'POST':
        name = request.form['name']
        print(name)

    if form.validate():
        # Save the comment here.
        flash('Received input text: ' + name)
        flash('Recommendations: ' + name)
    else:
        flash('All the form fields are required. ')

    return render_template('index.html', form=form)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
