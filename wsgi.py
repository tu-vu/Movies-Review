""" Application entry point. """
from Movies_Review import create_app

app = create_app()

if __name__ == "__main__":
    app.run()