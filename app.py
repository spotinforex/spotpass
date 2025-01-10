from flask import Flask, render_template
from auth import auth_routes
from password_flask import password_routes

app = Flask(__name__, template_folder='templates')  # specify the template folder

    # Register Blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(password_routes, url_prefix='/password')

app.config['TESTING'] = True

    # Route for rendering a test template (just an example)
@app.route('/')
def home():
        return render_template('index.html')  # Renders an HTML file named index.html in the templates folder

if __name__ == "__main__":
    app.run(debug=True)
