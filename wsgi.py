from app import create_app
from icons import load_icons

app = create_app()

@app.context_processor
def inject_icons():
    return {'icons': load_icons()}

if __name__ == "__main__":
    app.run()
