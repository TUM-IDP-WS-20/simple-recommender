import os
import random

from dominate.tags import i
from flask import Flask, request, jsonify, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask_bootstrap import Bootstrap

# App config.
import RecommendationScript

DEBUG = True
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Request, Engine, Item  # need to be set after SQLAlchemy for model detection


class ReusableForm(Form):
    name = TextAreaField('Input text:', validators=[validators.required()],
                         default='We examine how subjective performance evaluations are influenced by the level and controllability of an accompanying measure of a separate performance dimension. In our experiment, supervisors evaluate the office administration perfor- mance of a hypothetical subordinate. We find that supervisors’ subjective evaluations are directionally influenced by an accompanying objective measure of sales perfor- mance, even after excluding participants who perceive informativeness across measures. Consistent with concerns for fairness and motivation, we also find an asymmetric uncontrollability effect—supervisors’ evaluations are higher when an uncontrollable factor decreases the subordinate’s sales (i.e., they compensate for bad luck), but are not lower when the uncontrollable factor increases the subordinate’s sales (i.e., they do not punish for good luck). This evidence suggests that supervisors use discretion provided to evaluate performance on one task to adjust for perceived deficiencies in the evaluation of performance on other tasks. Our study integrates theories of cognitive bias and motivation, highlighting the need to consider the potentially interactive effects of different performance measures in multi-task settings I. INTRODUCTION Organizational incentive systems often allow managerial discretion in the evaluation of employee performance (Murphy and Oyer 2003). Subjective performance evaluation allows managers to use noncontractible information to assess actions and efforts that objective measures (such as those produced by the accounting system) are not able to capture, creating a more complete depiction of employee performance (Bol 2008).1 Subjectivity can therefore be useful in reducing risk to employees and improving the incentive alignment of the firm’s performance measurement system (Baker et al. 1994; Bushman et al. 1996; Hayes and Schaefer 2000).2 Many performance measurement systems include both objective measures and subjective evaluations (Prendergast 1999; Gibbs et al. 2004). While designed to capture separate dimensions of employee performance, these different measurement types can influence each other. For example, theories from psychology and organizational behavior suggest that subjective judgments can be unduly influenced by an individual’s knowledge of other, unrelated information (Nisbett et al. 1981; Bond et al. 2007). Such an influence could limit the complementary role of subjective evaluation in improving the overall informativeness of the measures used to evaluate performance. We examine how supervisors’ subjective performance evaluations are affected by the level and controllability of an objective measure of a separate aspect of performance. We analyze a two-dimensional employment setting in which an employee’s performance on one dimension (i.e., task) is measured objectively, while performance on the other dimension is evaluated subjectively by the supervisor. In many such settings, the objective performance measure is known by the supervisor before s/he subjectively evaluates the employee’s performance on the other dimension (Huber et al. 1987; Bommer et al. 1995). Our first research question examines whether the level of the objective measure has a directional impact on the supervisor’s subjective evaluation. Specifically, we examine whether, consistent with cognitive distortion, supervisors bias their subjective evaluations of performance on one dimension to be consistent with an objective measure of performance on a separate and unrelated dimension.3 Our second research question considers how such a spillover effect differs when the controllability of the objective performance measure is relatively low. Uncontrollability introduces noise and error into the performance measurement system (Feltham and Xie 1994), and has been shown to affect attribution judgments (Tan and Lipe 1997). Employees are likely to perceive uncontrollable performance measures to be unfair when the uncontrollability reduces measured performance. Perceptions of unfairness in compensation lead to reduced job satisfaction and motivation (Cohen-Charash and Spector 2001; Colquitt et al. 2001). We examine whether this expectation is reflected in supervisors’ use of their discretion, even when that discretion is provided for the evaluation of a separate task. Specifically, we examine whether supervisors use the discretion in their subjective evaluations to adjust for (or offset) the effects of an uncontrollable objective measure. Consistent with concerns for fairness and employee motivation, we predict that supervisors will make such an adjustment when the uncontrollable factor reduces measured performance (i.e., the employee suffers from bad luck) but not when it increases measured performance (i.e., the employee benefits from good luck). In our experiment, experienced supervisors employed by a large state university participate as evaluators in a hypothetical case setting. Participants assume the role of a regional director with supervisory authority over district managers who have both sales- and office administration-related duties. Objective individual sales information is given, after which participants are charged with subjectively evaluating the office administration performance of one district manager based on personal notes and staff interview responses, which are held constant in all conditions. The experiment employs a 2 3 2 þ 1 between-subjects design. In four treatment conditions, we manipulate the level of the manager’s individual sales at two levels by varying the objective sales score (high and low), and we manipulate the controllability of the individual sales measure at two levels by varying whether significant but uncontrollable events impacted the manager’s sales during the period. A fifth (control) condition includes only the information about the manager’s office administration performance. We find that supervisors’ subjective evaluations of the manager’s office administration performance are significantly higher (lower) when the objective level of the manager’s individual sales measure is relatively high (low). By excluding those participants who perceived the individual sales measure to be informative about the manager’s office administration performance in our primary analysis, we provide evidence of cognitive distortion of performance information as a result of exposure to the objective measure. We also find that the effect of the objective measure depends on its controllability. Specifically, participants use their subjective evaluations to adjust for the impact of uncontrollable events on the sales measure. Consistent with theory, this effect is asymmetric—participants’ evaluations are higher (relative to the high controllability condition) when the uncontrollable factor leads to an unfavorable outcome, but are no lower when the uncontrollable factor leads to a favorable outcome. Thus, we find that participants use their discretion to compensate for bad luck, but not to punish for good luck. This study contributes to the accounting and management literatures on performance evaluation. Prior research on bias in performance evaluation has found that supervisors’ subjective evaluations of current performance may be directionally influenced by prior performance information (Murphy et al. 1985; Huber et al. 1987; Kravitz and Balzer 1992) or information from different sources (Blakely 1993; Murphy and Cleveland 1995; Bono and Colbert 2005). Our study contributes to this line of research by showing that cognitive distortion can cause spillover from the objective evaluation of one dimension of performance to the subjective evaluation of performance on a separate and unrelated dimension. Prior research has also found evidence that controllability concerns can affect evaluators’ judgments in single-dimension performance-evaluation settings. For example, Tan and Lipe (1997) find that controllability moderates outcome effects in evaluators’ judgments (also see Brown and Solomon 1987). Our study reveals a very different controllability effect. Specifically, our results suggest that supervisors can use discretion that is provided for the evaluation of performance on a particular dimension to ‘‘correct’’ perceived deficiencies in other areas of the evaluation system. While the use of ‘‘borrowed’’ discretion can yield motivational benefits for employees, the intended benefits of that discretion (i.e., accurate reflection of performance on a specific dimension) can be reduced. Overall, our evidence indicates that the known level of an objective performance measure compromises the effectiveness of subjective performance evaluation for completing the picture of employee performance. Thus, our results have implications for the weight, timing, and nature of subjectivity in compensation contracting, suggesting that consideration of different measurement types in isolation can lead to incomplete conclusions about the optimal design of performance measurement systems. An asymmetric pattern of compensation payouts, in which managers are sheltered from downside risk but are allowed the advantages of upside risk, has been demonstrated in accounting')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)

    print(form.errors)

    if request.method == 'POST' and request.form['action'] == 'recommendation':
        name = request.form['name']
        print(name)

        if form.validate():
            recs = RecommendationScript.make_suggestions(name)
            # print('dssfdsf')
            # print(recs[0])

            # Save the comment here.

            flash(Markup(RecommendationScript.df_topic_keywords.to_html(classes='')), 'table')

            html_content = '<form action="" method="post">' \
                           'Give general rating for this model: <input type="number" value="3" min="1" max="5" step="1" name="engine_rating_0" />' \
                           '(1=very bad, 5=very good)' \
                           '<input type = "submit" value = "Rate" style="background: orange; color: white; width: 100px; height: 40px" />' \
                           '<ul>'
            for i in range(len(recs)):
                html_content += '<li><div style="width: 100%"><strong>File: </strong>' + RecommendationScript.get_file_name(
                    str(recs[i][0])) + \
                             '<br /><input type="number" min="1" max="5" step="1" value="3" name="rate_'+str(i)+'">(give 1 to 5. 1=very bad, 5=very good)' + \
                             '<br /><strong>Title: </strong>' + str(recs[i][54]) + \
                             '<br /><strong>Journal: </strong>' + str(recs[i][55]) + \
                             '<br /><strong>Year: </strong>' + str(recs[i][52])[:4] + \
                             '<br /><strong>Authors: </strong>' + str(recs[i][53]) + \
                             '<br /><strong>Doi: </strong>' + str(recs[i][56]) + \
                             '<br /><strong>Link: </strong>' + str(recs[i][57]) + \
                             '<br /><input type="hidden" name="name" value="'+name+'">' + \
                             '<input type="hidden" name="action" value="rating">' + \
                             '</div></li>'
            html_content += '</ul></form>'
            flash(Markup(html_content))
        else:
            flash('After putting input text and clicking "Suggest" button, you will see recommendations here.')

    if request.method == 'POST' and request.form['action'] == 'rating':
        print('test anmemasd a')
        name = request.form['name']
        recs = RecommendationScript.make_suggestions(name)
        ratings=[request.form['rate_0'],request.form['rate_1'],request.form['rate_2'],request.form['rate_3'],request.form['rate_4']]
        engine_ratings=[request.form['engine_rating_0']]

        # FUCK
        #for i in range(5):
        #    idnex = 'rate_'+str(i)
            #print(idnex)
            #ratings.append(request.form[''+idnex])

        add_rating(name, recs, ratings, engine_ratings)
        flash(Markup('<div style="font-size: 18px; color: green"> Thank you for rating!! You can take suggestion for different text! </div>'), 'rating')

    return render_template('index.html', form=form)


def add_rating(input_content, recs, ratings, engine_ratings):
    req = Request(input_content=input_content, user_name='test_user')
    db.session.add(req)

    engine = Engine(model_type='LDA', model_version='model_8_content_3_topic_50', rating=engine_ratings[0])
    engine.request = req
    db.session.add(engine)

    for sequence, rec in enumerate(recs):
        file_path = RecommendationScript.get_file_name(str(rec[0]))
        rating = ratings[sequence]

        item = Item(file_path=file_path, sequence=sequence, rating=rating)

        item.engine = engine
        db.session.add(item)

    db.session.commit()


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
