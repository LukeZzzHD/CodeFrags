from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=30)])
    language = SelectField('Programming language', validators=[DataRequired()], choices=[('java', 'Java'), ('javascript', 'Javascript'), ('csharp', 'C#'), ('cpp', 'C++'), ('python', 'Python'), ('c', 'C'), ('markup', 'HTML'), ('ruby', 'Ruby'), ('sql', 'SQL'), ('css', 'CSS'), ('go', 'GO'), ('php', 'PHP'), ('jsx', 'JSX')])
    code = TextAreaField('Your Code', validators=[DataRequired()])
    description = TextAreaField('Post description', validators=[DataRequired()])
    submit = SubmitField('Post')
