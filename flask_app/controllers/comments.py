from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.comment import Comment
from flask_app.models.user import User



@app.route('/user/dashboard')
def user_dashboard():

    if 'user_id' not in session:
        return redirect('/')

    user = User.get_id(
        {
        'id': session['user_id'],
        }
    )
    

    comment = Comment.get_all_comments()
    return render_template('dashboard.html', user=user,comment=comment)

@app.route('/new_comment')
def new_comment():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('add_comment.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    

    Comment.save(
        {
        'user_id': session['user_id'],
        'description': request.form['description'],
        } 
    )
    if 'user_id' not in session:
        return redirect('/')
    if not Comment.validate_comment(request.form):
        return redirect('/new_comment')
    return redirect('/user/dashboard')

# @app.route('/comment/<int:id>')
# def view_comment(id):
    
#     if 'user_id' not in session:
#         return redirect('/')

#     comment = Comment.get_id( { 'id': id } )
#     return render_template('dashboard.html',comment=comment)

@app.route('/user/edit_comment/<int:id>')
def edit_comment(id):
    if 'user_id' not in session:
        return redirect('/')
    
    user = User.get_id(
        {
        'id': session['user_id'],
        }
    )
    comment = Comment.get_id( { 'id' : id } )
    return render_template('edit_comment.html',comment=comment, user=user)

@app.route('/user/update_comment/<int:id>', methods=['POST'])
def update_comment(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Comment.validate_comment(request.form):
        return redirect('/user/edit_comment/<int:id>')

    comment_data = {
        'id': id,
        'description': request.form['description'],
    }
    Comment.update_comment(comment_data)
    return redirect('/user/dashboard')

@app.route('/delete_comment/<int:id>')
def delete_comment(id):
    if 'user_id' not in session:
        return redirect('/')

    Comment.delete_comment({'id':id})
    return redirect('/user/dashboard')