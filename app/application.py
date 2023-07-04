from config import create_app

application = create_app()
app = application

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
