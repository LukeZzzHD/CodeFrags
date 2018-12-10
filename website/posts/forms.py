from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=30)])
    language = SelectField('Programming language', validators=[DataRequired()], choices=[('java', 'Java'), ('javascript', 'Javascript'), ('csharp', 'C#'), ('cpp', 'C++'), ('python', 'Python'), ('c', 'C'), ('markup', 'HTML'), ('ruby', 'Ruby'), ('sql', 'SQL'), ('css', 'CSS'), ('go', 'GO'), ('php', 'PHP'), ('jsx', 'JSX')])
    code = TextAreaField('Your Code', validators=[DataRequired()])
    description = TextAreaField('Post description', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    comment = TextAreaField('Your Comment', validators=[DataRequired(), Length(min=1, max=500)], render_kw={
        "autocomplete" : "off",
        "autocorrect" : "off",
        "autocapitalize" : "off",
        "spellcheck" : "false"
    })

    submit = SubmitField('Comment')
