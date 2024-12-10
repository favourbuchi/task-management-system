from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required, current_user
import datetime
from .models import User, Activity
from . import db
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        activity = request.form.get('task')
        date = request.form.get('date')
        time = request.form.get('time')
        print(activity)
        datetime_str = f'{date} {time}'

        try:
            datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            flash('Invalid date or time format', category='error')
        if datetime_obj < datetime.datetime.now():
            flash("Enter a future date!!!", category='error')
        else:
            new_task = Activity(data=activity, datetime=datetime_obj, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task Added successfully!!!', category='success')
            print("task uploaded to database successfully")
            
    return render_template('home.html', user=current_user)

@views.route('/delete-activity', methods=['POST'])
def delete_activity():
    activity = json.loads(request.data)
    activityId = activity['taskId']
    activity = Activity.query.get(activityId)

    if activity:
        if activity.user_id == current_user.id:
            db.session.delete(activity)
            db.session.commit()

    return json({})