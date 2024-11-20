from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from extensions import db
from models import Member
from config import Config

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

members_bp = Blueprint('members_bp', __name__)

@members_bp.route('/members', methods=['GET', 'POST'])
def members_page():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        joindate = datetime.now().date()

        file = request.files['profilepicture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile_pics', filename))
            img_path = os.path.join('images/profile_pics', filename).replace("\\", "/")
        else:
            img_path = None

        # Check if a member with the same name already exists
        existing_member = Member.query.filter_by(firstname=firstname, lastname=lastname).first()
        if existing_member:
            flash('A member with this name already exists.', 'error')
        else:
            # Only add a new member if no existing member was found
            new_member = Member(
                firstname=firstname,
                lastname=lastname,
                email=email,
                joindate=joindate,
                profilepicture=img_path
            )
            db.session.add(new_member)
            db.session.commit()
            flash('Member added successfully!', 'success')

    # Handle sorting, searching, and pagination
    sort_by = request.args.get('sortby', 'lastname')
    sort_order = request.args.get('order', 'asc')
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of members per page
    search_query = request.args.get('search', '')

    # Modify the members query with search, sort, and pagination
    members_query = Member.query.filter(
        (Member.firstname.ilike(f'%{search_query}%')) | 
        (Member.lastname.ilike(f'%{search_query}%'))
    ).order_by(db.text(f'{sort_by} {sort_order}'))

    members_pagination = members_query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'members.html',
        members_pagination=members_pagination,
        members=members_pagination.items,
        sort_by=sort_by,
        sort_order=sort_order,
        search_query=search_query,
        page=page,
        total_pages=members_pagination.pages
    )


@members_bp.route('/members/edit', methods=['POST'])
def edit_member():
    member_id = request.form['memberid']
    member = Member.query.get(member_id)
    if member:
        member.firstname = request.form['firstname']
        member.lastname = request.form['lastname']
        member.email = request.form['email']
        db.session.commit()
        flash('Member information updated successfully!', 'success')

    else:
        flash('Member not found.', 'error')

    return redirect(url_for('members_bp.members_page'))
