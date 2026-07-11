from backend.app.parsers.json_parser import json_parser


def test_valid_json():

    raw_response = """
    {
        "sql": "SELECT 1",
        "summary": "Test query",
        "confidence": 0.95,
        "tables_used": [
            "users"
        ],
        "read_only": true
    }
    """

    result = json_parser.parse(raw_response)

    print(result)

    assert result.sql == "SELECT 1"
    assert result.read_only is True