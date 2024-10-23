from flask import Blueprint, request, render_template, flash
from app import db
from models import Member
from werkzeug.utils import secure_filename
from datetime import datetime
import os

members_bp = Blueprint('members_bp', __name__)

@members_bp.route('/members', methods=['GET', 'POST'])
def members_page():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        joindate = datetime.now().date()

        # Handle the image file upload
        file = request.files['profilepicture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_pics', filename))
            img_path = os.path.join('images/profile_pics', filename).replace("\\", "/")
        else:
            img_path = None

        # Insert new member
        new_member = Member(firstname=firstname, lastname=lastname, email=email, joindate=joindate, profilepicture=img_path)
        db.session.add(new_member)
        db.session.commit()

    # Fetch and filter members
    sort_by = request.args.get('sortby', 'lastname')
    sort_order = request.args.get('order', 'asc')
    search_query = request.args.get('search', '')

    members = Member.query.filter(
        (Member.firstname.ilike(f"%{search_query}%")) | (Member.lastname.ilike(f"%{search_query}%"))
    ).order_by(db.text(f'{sort_by} {sort_order}')).all()

    return render_template('members.html', members=members, sort_by=sort_by, sort_order=sort_order, search_query=search_query)
