from app import create_app
from app.config import Config


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    LLM_API_KEY = "test-key"
    ZEP_API_KEY = "test-zep"
    CORS_ALLOWED_ORIGINS = ["https://allowed.example"]


def test_app_factory_registers_strategy_lab_routes_and_uses_allowlist():
    app = create_app(TestConfig)
    client = app.test_client()

    response = client.get(
        "/api/graph/project/list",
        headers={"Origin": "https://allowed.example"},
    )

    assert response.status_code == 200
    assert response.headers.get("Access-Control-Allow-Origin") == "https://allowed.example"
    assert any("/api/strategy-lab/project/<project_id>" == rule.rule for rule in app.url_map.iter_rules())
