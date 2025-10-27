from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
DATABASE = 'students.db'

# Initialize DB
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

# Connect to DB
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Home Page
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
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <style>
        body { 
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f2 100%);
            min-height: 100vh;
            padding: 2rem 0;
        }
        .card {
            border: none;
            border-radius: 1.5rem;
            box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.08);
        }
        .card-header {
            background: linear-gradient(45deg, #4158d0 0%, #3b5998 100%);
            border-radius: 1.5rem 1.5rem 0 0 !important;
            padding: 1.5rem;
        }
        .form-control {
            border-radius: 0.75rem;
            padding: 0.75rem 1.25rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            background-color: #f8f9fa;
            transition: all 0.3s ease;
        }
        .form-control:focus {
            background-color: #fff;
            box-shadow: 0 0 0 0.25rem rgba(59, 89, 152, 0.1);
            border-color: rgba(59, 89, 152, 0.4);
        }
        .form-label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 0.5rem;
        }
        .btn {
            border-radius: 0.75rem;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: linear-gradient(45deg, #4158d0 0%, #3b5998 100%);
            border: none;
        }
        .btn-primary:hover {
            background: linear-gradient(45deg, #3b5998 0%, #4158d0 100%);
            transform: translateY(-1px);
        }
        .btn-action {
            padding: 0.5rem 1rem;
            margin: 0 0.25rem;
        }
        .table {
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 2rem;
        }
        .table th {
            background-color: #f8f9fa;
            font-weight: 600;
            padding: 1rem;
            border-bottom: 2px solid #dee2e6;
        }
        .table td {
            padding: 1rem;
            vertical-align: middle;
            border-bottom: 1px solid #dee2e6;
        }
        .table tbody tr {
            transition: all 0.3s ease;
        }
        .table tbody tr:hover {
            background-color: rgba(59, 89, 152, 0.05);
        }
        .alert {
            border-radius: 0.75rem;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
        }
        .loading {
            opacity: 0.7;
            pointer-events: none;
        }
        .student-count {
            color: #6c757d;
            font-size: 0.9rem;
            margin-bottom: 1rem;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="card shadow-lg mb-4">
        <div class="card-header">
            <h2 class="text-white mb-0 text-center">
                <i class="bi bi-mortarboard-fill me-2"></i>Student Management System
            </h2>
        </div>
        <div class="card-body p-4">
            <div id="alertArea"></div>
            
            <form id="addForm" class="row g-3">
                <div class="col-md-4">
                    <label for="name" class="form-label">Student Name</label>
                    <input type="text" class="form-control" id="name" 
                           placeholder="Enter student name" required>
                </div>
                <div class="col-md-4">
                    <label for="year" class="form-label">Year Level</label>
                    <input type="text" class="form-control" id="year" 
                           placeholder="e.g., First Year" required>
                </div>
                <div class="col-md-4">
                    <label for="section" class="form-label">Section</label>
                    <input type="text" class="form-control" id="section" 
                           placeholder="Enter section" required>
                </div>
                <div class="col-12 text-end">
                    <button type="submit" class="btn btn-primary px-4">
                        <i class="bi bi-plus-circle me-2"></i>Add Student
                    </button>
                </div>
            </form>

            <div class="student-count mt-4">
                Total Students: <span class="fw-bold">{{ students|length }}</span>
            </div>

            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead>
                        <tr>
                            <th class="text-center" style="width: 80px">ID</th>
                            <th>Name</th>
                            <th>Year</th>
                            <th>Section</th>
                            <th class="text-end" style="width: 200px">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in students %}
                        <tr id="row-{{ s['id'] }}">
                            <td class="text-center">#{{ s['id'] }}</td>
                            <td>{{ s['name'] }}</td>
                            <td>{{ s['year'] }}</td>
                            <td>{{ s['section'] }}</td>
                            <td class="text-end">
                                <button class="btn btn-outline-primary btn-action edit-btn" 
                                        data-student-id="{{ s['id'] }}">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <button class="btn btn-outline-danger btn-action" 
                                        onclick="deleteStudent({{ s['id'] }})">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" class="text-center text-muted py-4">
                                <i class="bi bi-inbox h4 d-block mb-2"></i>
                                No students added yet. Add your first student above!
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

<script>
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.getElementById('alertArea').appendChild(alertDiv);
    setTimeout(() => alertDiv.remove(), 3000);
}

function setLoading(element, isLoading) {
    if (isLoading) {
        element.classList.add('loading');
        if (element.tagName === 'BUTTON') {
            element.originalText = element.innerHTML;
            element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        }
    } else {
        element.classList.remove('loading');
        if (element.tagName === 'BUTTON' && element.originalText) {
            element.innerHTML = element.originalText;
        }
    }
}

document.getElementById('addForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    try {
        setLoading(submitBtn, true);
        const data = {
            name: document.getElementById('name').value,
            year: document.getElementById('year').value,
            section: document.getElementById('section').value
        };
        
        const res = await fetch('/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            showAlert('Student added successfully!');
            form.reset();
            location.reload();
        } else {
            throw new Error('Failed to add student');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        setLoading(submitBtn, false);
    }
});

async function deleteStudent(id) {
    const row = document.getElementById(`row-${id}`);
    const btns = row.querySelectorAll('button');
    
    if (!confirm('Are you sure you want to delete this student?')) return;
    
    try {
        btns.forEach(btn => setLoading(btn, true));
        const res = await fetch(`/delete/${id}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            row.style.backgroundColor = '#ffe9e9';
            setTimeout(() => {
                row.style.transition = 'opacity 0.5s ease';
                row.style.opacity = '0';
                setTimeout(() => row.remove(), 500);
            }, 100);
            showAlert('Student deleted successfully');
        } else {
            throw new Error('Failed to delete student');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        btns.forEach(btn => setLoading(btn, false));
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers for edit buttons
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const id = this.dataset.studentId;
            editStudent(id);
        });
    });
});

async function editStudent(id) {
    const row = document.getElementById(`row-${id}`);
    const btns = row.querySelectorAll('button');
    
    // Create modal for editing
    const modalHtml = `
        <div class="modal fade" id="editModal-${id}" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Edit Student</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="editForm-${id}">
                            <div class="mb-3">
                                <label class="form-label">Name</label>
                                <input type="text" class="form-control" name="name" 
                                       value="${row.children[1].textContent.trim()}" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Year</label>
                                <input type="text" class="form-control" name="year" 
                                       value="${row.children[2].textContent.trim()}" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Section</label>
                                <input type="text" class="form-control" name="section" 
                                       value="${row.children[3].textContent.trim()}" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="submitEdit(${id})">Save Changes</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to document
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    const modal = new bootstrap.Modal(document.getElementById(`editModal-${id}`));
    modal.show();
    
    // Clean up modal after hiding
    const modalElement = document.getElementById(`editModal-${id}`);
    modalElement.addEventListener('hidden.bs.modal', () => {
        modalElement.remove();
    });
}

async function submitEdit(id) {
    const form = document.getElementById(`editForm-${id}`);
    const modal = bootstrap.Modal.getInstance(document.getElementById(`editModal-${id}`));
    const submitBtn = modal._element.querySelector('.btn-primary');
    
    try {
        setLoading(submitBtn, true);
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            year: formData.get('year'),
            section: formData.get('section')
        };
        
        const res = await fetch(`/edit/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (res.ok) {
            modal.hide();
            showAlert('Student updated successfully');
            location.reload();
        } else {
            throw new Error('Failed to update student');
        }
    } catch (error) {
        showAlert(error.message, 'danger');
    } finally {
        setLoading(submitBtn, false);
    }
}
</script>
</body>
</html>
''', students=students)

# Add Student
@app.route('/add', methods=['POST'])
def add_student():
    data = request.get_json()
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO students (name, year, section) VALUES (?, ?, ?)',
              (data['name'], data['year'], data['section']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student added successfully'})

# Delete Student
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student deleted'})

# Edit Student
@app.route('/edit/<int:id>', methods=['PUT'])
def edit_student(id):
    data = request.get_json()
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE students SET name=?, year=?, section=? WHERE id=?',
              (data['name'], data['year'], data['section'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student updated successfully'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
