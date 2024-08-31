from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
import datetime

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app) # Initialise CKEditor

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# FlaskForm for creating and editing a blog post
class BlogPostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


with app.app_context():
    db.create_all()

# Get the current date
def get_date():
    today = datetime.date.today()
    formatted_date = today.strftime("%B %d, %y")
    return formatted_date

@app.route('/')
def get_all_posts():
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = 5 # Number of posts per page

    # Query the database for posts with pagination
    paginated_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # # Old code for querying without pagination
    # result = db.session.execute(db.select(BlogPost))
    # posts = result.scalars().all()
    # return render_template("index.html", all_posts=posts)

    # Render the template with paginated posts
    return render_template("index.html",
                           all_posts=paginated_posts.items,
                           pagination=paginated_posts)

# Add a route so that you can click on individual posts.
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)

# add_new_post() to create a new blog post
@app.route('/create-post', methods=["GET", "POST"])
def add_new_post():
    # Get the data
    form = BlogPostForm() # This should be BlogPostForm, not BlogPost
    # validate_on_submit() is a Flask-WTF function line 89 definition
    if form.validate_on_submit():
        # Debugging prints
        print(f"Form Data: {form.title.data}, {form.subtitle.data}")

        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            date=get_date(),  # Automatically assign the current date
            author=form.author.data,
            img_url=form.img_url.data or None,
            body=form.body.data,
        )
        # add to databese
        db.session.add(new_post)
        try:
            db.session.commit()
            flash("Blog added successfully", "success")
            return redirect(url_for("get_all_posts"))
        except Exception as e:
            # Undo the operation if something went wrong
            db.session.rollback()
            flash(f"Error message: {e}","danger")
    else:
        # Print form errors for debugging
        print("Form errors:", form.errors)
    return render_template("make-post.html", form=form)

# edit_post() to change an existing blog post
@app.route('/edit-post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    # Retrieve a BlogPost from the database based on the post_id
    to_edit_post = db.get_or_404(BlogPost, post_id)
    form = BlogPostForm(obj=to_edit_post)  # Prepopulate the form with the existing data

    if form.validate_on_submit():
        to_edit_post.title = form.title.data
        to_edit_post.subtitle = form.subtitle.data
        to_edit_post.author = form.author.data
        to_edit_post.img_url = form.img_url.data or None
        to_edit_post.body = form.body.data

        try:
            # Commit changes to the database
            db.session.commit()
            flash("Post updated successfully", "success")
            return redirect(url_for('get_all_posts'))
        except Exception as e:
            # Undo the operation if something went wrong
            db.session.rollback()
            flash(f"Error occurred: {e}", "danger")

    return render_template("make-post.html", form=form, is_edit=True)

# delete_post() to remove a blog post from the database
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5004)
