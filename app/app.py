
from flask import Flask
from .config import Settings

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SETTINGS"] = Settings()

    # Register blueprints
    from .blueprints.rag_bp import rag_bp
    from .blueprints.search_bp import search_bp
    from .blueprints.ingest_bp import ingest_bp

    app.register_blueprint(rag_bp, url_prefix="/rag")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(ingest_bp, url_prefix="/ingest")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

# WSGI entry
app = create_app()
