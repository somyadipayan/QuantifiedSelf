from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import datetime


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    from .models import Tracker
    from . import db
    user = current_user.id
    from .models import Tracker, Log
    tracker = db.session.query(Tracker).with_entities(
        Tracker.name, Tracker.id, Tracker.description).distinct().filter(Tracker.uid == user).all()
    logs = db.session.query(Log).with_entities(
        Log.id).distinct().filter(Log.uid == user).all()
    print(tracker)

    return render_template("home.html", user=current_user, tracker=tracker, tracker_count=len(tracker), log_count=len(logs))


@views.route('/add-tracker', methods=['GET', 'POST'])
@login_required
def add_tracker():
    if request.method == "GET":
        from . import db
        from .models import Tracker
        user = current_user.id
        tracker = db.session.query(Tracker).with_entities(
            Tracker.name, Tracker.id, Tracker.description).distinct().filter(Tracker.uid == user).all()
        return render_template("addtracker.html", user=current_user, tracker=tracker, tracker_count=len(tracker))
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['Action']
        settings = request.form['settings']
        description = request.form['description']

        from .models import Tracker

        tracker = Tracker.query.filter_by(name=name).first()
        user = current_user.id

        if tracker and user == tracker.uid:
            flash('The tracker "' + name + '" already exists', category='error')
            return redirect(url_for('views.add_tracker'))
        else:
            from . import db
            tracker_info = Tracker(
                name=name, description=description, type=type, settings=settings, uid=user)
            db.session.add(tracker_info)
            db.session.commit()
            flash(name + ' Tracker Added', category='success')
            return redirect(url_for('views.home'))


@views.route('/delete-tracker/<int:tid>', methods=['GET', 'POST'])
@login_required
def delete_tracker(tid):
    from .models import Tracker
    tracker = Tracker.query.get(tid)
    from . import db
    db.session.delete(tracker)
    db.session.commit()
    flash(tracker.name + ' Tracker Removed Successfully.', category='success')
    return redirect(url_for('views.home'))


@views.route("/trackerinfo/<int:tid>", methods=["GET", "POST"])
@login_required
def trinfo(tid):
    if request.method == "GET":
        from .models import Tracker, Log
        logs = Log.query.filter(Log.tid == tid).all()
        tracker = Tracker.query.with_entities(
            Tracker.type, Tracker.name).filter(Tracker.id == tid).first()

        return render_template("trackerinfo.html", tracker=tracker, user=current_user, logs=logs, tid=tid)


@views.route('/edit-tracker/<int:tid>', methods=['GET', 'POST'])
@login_required
def edit_tracker(tid):
    user = current_user.id
    from .models import Tracker
    tracker = Tracker.query.get(tid)

    from . import db
    trackers = db.session.query(Tracker).with_entities(
        Tracker.name, Tracker.id, Tracker.description).distinct().filter(Tracker.uid == user).all()
    if request.method == "GET":
        return render_template("edittracker.html", user=current_user, tracker=tracker, tid=tid, trackers=trackers)

    if request.method == 'POST':
        type = request.form['Action']
        settings = request.form['settings']
        description = request.form['description']
        uid = current_user.id
        from . import db
        tracker.description = description
        tracker.type = type
        tracker.settings = settings
        db.session.commit()
        flash('Tracker Updated Successfully.', category='success')
        return redirect(url_for('views.home'))


@views.route('/add-log/<int:tid>', methods=['GET', 'POST'])
@login_required
def add_log(tid):
    from .models import Tracker, Log
    user = current_user.id
    tracker = Tracker.query.get(tid)
    logs = Log.query.filter(Log.tid == tid).all()
    import datetime
    now = datetime.datetime.now()
    options = []
    from . import db
    trackers = db.session.query(Tracker).with_entities(
        Tracker.name, Tracker.id, Tracker.description).distinct().filter(Tracker.uid == user).all()
    if tracker.type == "multiple_choice":
        option = tracker.settings
        options = option.split(',')

    if request.method == "GET":
        return render_template("addlog.html", user=current_user, tracker=tracker, now=now, tid=tid, options=options, trackers=trackers, logs=logs)

    if request.method == 'POST':
        when = request.form['date']
        value = request.form['value']
        note = request.form['note']
        from . import db
        log_info = Log(timestamp=when, value=value, note=note,
                       tid=tid, uid=current_user.id, added_date_time=now)
        db.session.add(log_info)
        db.session.commit()
        flash('New Log Added For ' + tracker.name +
              ' Tracker', category='success')
        return redirect(url_for('views.trinfo', tid=tid))


@views.route('/edit-log/<int:lid>', methods=['GET', 'POST'])
@login_required
def edit_log(lid):
    from .models import Log, Tracker
    from . import db
    options = []
    from . import db
    logs = Log.query.get(lid)
    all_logs = Log.query.filter(Log.tid == logs.tid).all()
    tracker = Tracker.query.get(logs.tid)
    user = current_user.id
    
    if tracker.type == "multiple_choice":
        option = tracker.settings
        options = option.split(',')

    if request.method == 'POST':
        when = request.form.get('date')
        value = request.form.get('value')
        note = request.form.get('note')


        logs.timestamp = when
        logs.value = value
        logs.note = note

        db.session.commit()

        return redirect(url_for('views.trinfo', tid=logs.tid))
    return render_template("editlog.html", user=current_user, tracker=tracker, log=logs, tid=logs.tid, all_logs=all_logs, options=options)


@views.route('/delete-log/<int:lid>', methods=['GET', 'POST'])
@login_required
def delete_log(lid):
    from .models import Log
    loginfo = Log.query.get(lid)
    tid = loginfo.tid
    from . import db
    db.session.delete(loginfo)
    db.session.commit()
    return redirect(url_for('views.trinfo', tid=tid))
