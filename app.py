import os
from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
DATABASE = os.path.join(app.root_path, 'students.db')

# Initialize DB immediately
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year TEXT NOT NULL,
            section TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call init_db at the very start
init_db()

# Connect to DB
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Routes go here...

# -----------------------------
# Home Page
# -----------------------------
@app.route('/')
def home():
    conn = get_db()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template_string('''
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Student Management System</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<style>
body { background: #f0f2f5; padding: 2rem 0; }
.card { border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1); }
.card-header { background: #4158d0; color: white; font-weight: bold; font-size: 1.25rem; text-align: center; }
.btn-action { margin: 0 0.25rem; }
</style>
</head>
<body>
<div class="container">
  <div class="card shadow mb-4">
    <div class="card-header">Student Management System</div>
    <div class="card-body">

      <!-- Add Form -->
      <form id="addForm" class="row g-3 mb-4">
        <div class="col-md-4"><input type="text" class="form-control" id="name" placeholder="Student Name" required></div>
        <div class="col-md-4"><input type="text" class="form-control" id="year" placeholder="Year Level" required></div>
        <div class="col-md-4"><input type="text" class="form-control" id="section" placeholder="Section" required></div>
        <div class="col-12 text-end"><button type="submit" class="btn btn-primary">Add Student</button></div>
      </form>

      <!-- Table -->
      <table class="table table-striped align-middle text-center">
        <thead class="table-primary">
          <tr><th>ID</th><th>Name</th><th>Year</th><th>Section</th><th>Actions</th></tr>
        </thead>
        <tbody>
          {% for s in students %}
          <tr id="row-{{ s['id'] }}">
            <td>{{ s['id'] }}</td>
            <td>{{ s['name'] }}</td>
            <td>{{ s['year'] }}</td>
            <td>{{ s['section'] }}</td>
            <td>
              <button class="btn btn-outline-primary btn-action edit-btn" data-id="{{ s['id'] }}">Edit</button>
              <button class="btn btn-outline-danger btn-action" onclick="deleteStudent({{ s['id'] }})">Delete</button>
            </td>
          </tr>
          {% else %}
          <tr><td colspan="5" class="text-muted">No students added yet!</td></tr>
          {% endfor %}
        </tbody>
      </table>

    </div>
  </div>
</div>

<script>
function showAlert(msg, type='success'){
  alert(msg);
}

// Add Student
document.getElementById('addForm').addEventListener('submit', async e=>{
  e.preventDefault();
  const data = {
    name: document.getElementById('name').value,
    year: document.getElementById('year').value,
    section: document.getElementById('section').value
  };
  const res = await fetch('/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  if(res.ok) location.reload();
});

// Delete Student
async function deleteStudent(id){
  if(!confirm('Delete this student?')) return;
  const res = await fetch(`/delete/${id}`,{method:'DELETE'});
  if(res.ok) location.reload();
}

// Edit Student
document.querySelectorAll('.edit-btn').forEach(btn=>{
  btn.addEventListener('click', async ()=>{
    const id = btn.dataset.id;
    const row = document.getElementById(`row-${id}`);
    const name = row.children[1].textContent;
    const year = row.children[2].textContent;
    const section = row.children[3].textContent;

    const newName = prompt('Enter Name:', name);
    if(newName===null) return;
    const newYear = prompt('Enter Year:', year);
    if(newYear===null) return;
    const newSection = prompt('Enter Section:', section);
    if(newSection===null) return;

    const res = await fetch(`/edit/${id}`,{
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({name:newName, year:newYear, section:newSection})
    });
    if(res.ok) location.reload();
  });
});
</script>
</body>
</html>
''', students=students)

# -----------------------------
# Add Student
# -----------------------------
@app.route('/add', methods=['POST'])
def add_student():
    data = request.get_json()
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO students (name, year, section) VALUES (?, ?, ?)',
              (data['name'], data['year'], data['section']))
    conn.commit()
    conn.close()
    return jsonify({'message':'Student added'})

# -----------------------------
# Delete Student
# -----------------------------
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id=?',(id,))
    conn.commit()
    conn.close()
    return jsonify({'message':'Student deleted'})

# -----------------------------
# Edit Student
# -----------------------------
@app.route('/edit/<int:id>', methods=['PUT'])
def edit_student(id):
    data = request.get_json()
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE students SET name=?, year=?, section=? WHERE id=?',
              (data['name'], data['year'], data['section'], id))
    conn.commit()
    conn.close()
    return jsonify({'message':'Student updated'})

# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    init_db()  # ensure table exists
    app.run(host='0.0.0.0', port=5000, debug=True)


