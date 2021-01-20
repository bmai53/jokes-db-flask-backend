from init import init_app

app, db = init_app()

import routes

if __name__ == "__main__":
    app.run(debug=True)