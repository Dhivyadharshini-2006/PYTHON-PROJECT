from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Dummy data storage (Normally, you'd use a database)
employees = []
attendance_records = []
leave_requests = []
tasks = [] 
meetings = []
kudos_list = [] +                                                                                                                       

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    username = request.form['username']
    password = request.form['password']
    
    # Simple login check
    if username == 'admin' and password == 'password':
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/attendance')
def attendance_page():
    return render_template('attendance.html', attendance=attendance_records, leaves=leave_requests)

@app.route('/check_in', methods=['POST'])
def check_in():
    name = request.form['name']
    now = datetime.now()
    attendance_records.append({
        'name': name,
        'check_in': now.strftime("%Y-%m-%d %H:%M:%S"),
        'check_out': None
    })
    return redirect(url_for('attendance_page'))

@app.route('/check_out', methods=['POST'])
def check_out():
    name = request.form['name']
    for record in reversed(attendance_records):
        if record['name'] == name and record['check_out'] is None:
            record['check_out'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    return redirect(url_for('attendance_page'))

@app.route('/submit_leave', methods=['POST'])
def submit_leave():
    name = request.form['name']
    reason = request.form['reason']
    date = request.form['date']
    leave_requests.append({
        'name': name,
        'reason': reason,
        'date': date,
        'status': 'Pending'
    })
    return redirect(url_for('attendance_page'))

# Employee Management Routes
@app.route('/employees')
def employee_page():
    return render_template('employee.html', employees=employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    position = request.form['position']
    department = request.form['department']
    employees.append({
        'name': name,
        'position': position,
        'department': department
    })
    return redirect(url_for('employee_page'))

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    name = request.form['name']
    employees[:] = [e for e in employees if e['name'] != name]
    return redirect(url_for('employee_page'))

# Dummy logout route (just for simulation)
@app.route('/logout')
def logout():
    return redirect(url_for('login'))
tasks = []  # Place this at the top of your file if not present already

@app.route('/tasks')
def task_page():
    return render_template('task_management.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    assigned_to = request.form['assigned_to']
    priority = request.form['priority']
    tasks.append({
        'task_name': task_name,
        'assigned_to': assigned_to,
        'priority': priority,
        'status': 'In Progress'
    })
    return redirect('/tasks')

@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    task_name = request.form['task_name']
    new_status = request.form['status']
    for task in tasks:
        if task['task_name'] == task_name:
            task['status'] = new_status
            break
    return redirect('/tasks')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_name = request.form['task_name']
    global tasks
    tasks = [t for t in tasks if t['task_name'] != task_name]
    return redirect('/tasks')
@app.route('/meetings')
def meeting_page():
    return render_template('meeting_scheduler.html', meetings=meetings)

# Route to schedule a new meeting
@app.route('/schedule_meeting', methods=['POST'])
def schedule_meeting():
    title = request.form['title']
    date = request.form['date']
    time = request.form['time']
    attendees = request.form['attendees']
    room = request.form['room']
    
    meetings.append({
        'title': title,
        'date': date,
        'time': time,
        'attendees': attendees,
        'room': room
    })
    return redirect('/meetings')
import os
from flask import send_from_directory

# Folder to store uploaded documents
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for document management page
@app.route('/documents')
def documents():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('document_management.html', files=files)

# Route to upload a document
@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'document' not in request.files:
        return redirect('/documents')
    
    file = request.files['document']
    if file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    return redirect('/documents')

# Route to download a document
@app.route('/uploads/<filename>')
def download_document(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


 # In-memory list to store kudos

@app.route('/kudos')
def kudos_page():
    return render_template('kudos.html', kudos=kudos_list)

@app.route('/post_kudos', methods=['POST'])
def post_kudos():
    from_user = request.form['from']
    to_user = request.form['to']
    message = request.form['message']

    kudos_list.append({
        'from': from_user,
        'to': to_user,
        'message': message
    })
    return redirect(url_for('kudos_page'))






@app.route('/reports')
def reports():
    total_employees = len(employees)
    total_attendance = len(attendance_records)
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task['status'].lower() == 'completed')
    pending_tasks = total_tasks - completed_tasks

    return render_template('reports.html', total_employees=total_employees,
                           total_attendance=total_attendance,
                           total_tasks=total_tasks,
                           completed_tasks=completed_tasks,
                           pending_tasks=pending_tasks)




if __name__ == '__main__':
    app.run(debug=True)
