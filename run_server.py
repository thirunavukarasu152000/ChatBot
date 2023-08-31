from dotenv import load_dotenv
load_dotenv()

from app.main import get_app


if __name__ == "__main__":
    app=get_app()
    app.run(debug=True, host='0.0.0.0')
