from flask import Flask, request, jsonify, render_template, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
import RecommendationScript

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
        recs = RecommendationScript.make_suggestions(name)
        # Save the comment here.
        for i in range(len(recs)):
            flash('File: ' + recs[i][30] + ', Similarity:' + "{:.16f}".format(recs[i][31]) + ', Topic Probabilities: '+','.join(["{:.16f}".format(i) for i in recs[i][:30]]))
    else:
        flash('After putting input text and clicking "Suggest" button, you will see recommendations here.')

    return render_template('index.html', form=form)


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
