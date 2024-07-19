from flask import Flask, render_template, jsonify, session, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'

mail = Mail(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# Example route to handle Ajax request
@app.route('/ajax-example', methods=['POST'])
def ajax_example():
    # Simulate data processing (replace with actual data retrieval or processing logic)
    data = {'message': 'Data received successfully'}
    return jsonify(data)
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            user_obj = User(user['id'])
            login_user(user_obj, remember='rememberMe' in request.form)
            flash('Logged in successfully.')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('login'))
        
        except sqlite3.IntegrityError:
            flash('Username already taken. Please choose a different one.', 'warning')

    return render_template('register.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Protected route (example: database page)
@app.route('/database')
@login_required
def database():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM custom_table').fetchall()
    conn.close()
    return render_template('database.html', items=items)

# Edit route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cursor.execute('UPDATE custom_table SET name = ?, description = ? WHERE id = ?', (name, description, id))
        conn.commit()
        conn.close()
        flash('Record updated successfully.')
        return redirect(url_for('database'))
    else:
        cursor.execute('SELECT * FROM custom_table WHERE id = ?', (id,))
        item = cursor.fetchone()
        conn.close()
        if item:
            return render_template('edit.html', item=item)
        else:
            flash('Record not found.')
            return redirect(url_for('database'))

# Delete route
@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM custom_table WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Record deleted successfully.')
    return redirect(url_for('database'))

# Send email route
@app.route('/send-email')
def send_email():
    msg = Message('Subject of the Email', sender='your-email@example.com', recipients=['recipient@example.com'])
    msg.body = 'Body of the email goes here'
    mail.send(msg)
    return 'Email sent!'

# Homepage or Index page route
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Ajax route
@app.route('/ajax')
def ajax():
    return render_template('ajax.html')

# Ajax data route
@app.route('/get_data')
def get_data():
    return jsonify({'message': 'Hello from the server!'})

# Checklist page
@app.route('/checklist')
def checklist():
    return render_template('checklist.html')

# Site Description page
@app.route('/site_description')
def site_description():
    return render_template('site_description.html')

# About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Membership area
@app.route('/membership')
@login_required
def membership():
    return render_template('membership.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        # Process the form data (e.g., send an email)
        msg = Message(subject, sender=email, recipients=['info@example.com'])
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        mail.send(msg)
        
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')


# Join route
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tier = request.form['tier']
        # Process the form data (e.g., save to database)
        # For now, we just redirect to the membership page
        return redirect(url_for('membership'))
    return render_template('join.html')

if __name__ == '__main__':
    app.run(debug=True)
