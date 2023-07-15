from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Import and register the routes
from routes import sports_routes, events_routes, selections_routes

app.register_blueprint(sports_routes)
app.register_blueprint(events_routes)
app.register_blueprint(selections_routes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
