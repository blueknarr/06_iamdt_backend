from fastapi.testclient import TestClient
from app.api.calculator import calculator_db
from app.main import app

client = TestClient(app)


def click_c_btn():
    """
    0번 유저
    C 버튼을 누르면 초기화
    """
    response = client.post(
        "/api/v1/calculator",
        json={
            "id": 0,
            "button": "C"
        },
    )
    assert response.status_code == 201
    assert response.json() == {"msg": "수식이 입력되었습니다."}


def test_input_error_operator_first():
    """
    0번 유저
    첫 입력을 operator로 입력했을 때, 올바른 수식이 아님
    """
    test_input = ["+", "-", "*", "/", "%"]
    for op in test_input:
        response = client.post(
            "/api/v1/calculator",
            json={
                "id": 0,
                "button": op
            },
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "올바른 수식이 아닙니다."}
    click_c_btn()


def test_input_without_sign():
    """
    0번 유저
    정상적으로 수식을 입력했을 때
    """
    test_input = ["1", "*", "2", "+", "3"]
    for op in test_input:
        response = client.post(
            "/api/v1/calculator",
            json={
                "id": 0,
                "button": op
            },
        )
        assert response.status_code == 201
        assert response.json() == {"msg": "수식이 입력되었습니다."}
    click_c_btn()


def test_input_with_sign():
    """
    0번 유저
    sign: +/- 버튼, 버튼을 누르면 부호를 바꾼다.
    """
    test_input = ["1", "*", "2", "sign", "+", "3"]
    for op in test_input:
        response = client.post(
            "/api/v1/calculator",
            json={
                "id": 0,
                "button": op
            },
        )
        assert response.status_code == 201
        assert response.json() == {"msg": "수식이 입력되었습니다."}
    click_c_btn()


def test_get_incorrect_expression():
    """
    0번 유저
    수식이 완성되지 않았을 때 에러 발생
    """
    test_input = ["1", "*", "2", "+"]
    for op in test_input:
        response = client.post(
            "/api/v1/calculator",
            json={
                "id": 0,
                "button": op
            },
        )
        assert response.status_code == 201
        assert response.json() == {"msg": "수식이 입력되었습니다."}

    response = client.get(
        "/api/v1/calculator/0/result",
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "올바른 수식이 아닙니다."}
    click_c_btn()


def test_get_correct_expression_without_sign():
    """
    0번 유저
    올바른 수식일 때, 계산식과 결과값 전달
    infix -> postfix 성공
    """
    test_input = ["1", "*", "2", "+", "3"]
    for op in test_input:
        response = client.post(
            "/api/v1/calculator",
            json={
                "id": 0,
                "button": op
            },
        )
        assert response.status_code == 201
        assert response.json() == {"msg": "수식이 입력되었습니다."}

    response = client.get(
        "/api/v1/calculator/0/result",
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "계산 결과: 1 * 2 + 3 = 5"}
    click_c_btn()


def test_get_correct_expression_with_sign():
    """
    0번 유저
    올바른 수식일 때, 계산식과 결과값 전달
    infix -> postfix 성공
    sign: +/- 버튼 입력
    """
    test_input = ["1", "*", "2", "sign", "+", "3"]
    for op in test_input:
        response = client.post(
            "/api/v1/calculator",
            json={
                "id": 0,
                "button": op
            },
        )
        assert response.status_code == 201
        assert response.json() == {"msg": "수식이 입력되었습니다."}

    response = client.get(
        "/api/v1/calculator/0/result",
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "계산 결과: 1 * -2 + 3 = 1"}


def test_get_expression_history():
    """
    0번 유저
    계산식 목록 가져옴
    """
    response = client.get(
        "/api/v1/calculator/0",
    )
    assert response.status_code == 200
    assert response.json() == {"msg": ['1 * -2 + 3 = 1']}


def test_get_expression_history_error():
    """
    1번 유저
    계산식 목록이 없는 유저가 계산식 목록을 요청했을 때
    """
    response = client.get(
        "/api/v1/calculator/1",
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "계산기를 사용한 이력이 없습니다."}