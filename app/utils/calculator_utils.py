from typing import Union


def mock_db_init(cal_db: dict, user_id: int) -> dict:
    """
    db 초기화
    :param cal_db: dict
    :param user_id: int
    :return: dict
    """
    cal_db[user_id] = {
        "expression": [],
        "history": [],
        "sign": False,
    }
    return cal_db[user_id]


def is_operator(button: str) -> bool:
    """
    버튼의 입력값이 operator인지 판별
    :param button: str
    :return: bool
    """
    operator = {"+": True, "-": True, "*": True, "/": True, "%": True}
    if button in operator:
        return True
    return False


def change_sign(cal_db: dict, user_id: int):
    """
    부호 변경 버튼을 입력받으면, 숫자만 부호 변경
    :param cal_db: dict
    :param user_id: int
    """
    if len(cal_db[user_id]["expression"]) == 0 or is_operator(cal_db[user_id]["expression"][-1]):
        cal_db[user_id]["sign"] = not cal_db[user_id]["sign"]
    else:
        if cal_db[user_id]["expression"][-1][0] == '-':
            cal_db[user_id]["expression"][-1] = cal_db[user_id]["expression"][-1][1:]
        else:
            cal_db[user_id]["expression"][-1] = f"-{cal_db[user_id]['expression'][-1]}"
        cal_db[user_id]["sign"] = not cal_db[user_id]["sign"]


def str_to_num(button: str) -> Union[int, float]:
    """
    입력 받은 문자를 정수 또는 실수로 변환
    :param button: str
    :return: int or float
    """
    if button.find('.') > 0:
        return float(button)
    return int(button)


def float_to_int(num: float) -> Union[int, float]:
    """
    연산 결과가 정수일 때
    :param num: float
    :return: int or float
    """
    if float(num).is_integer():
        return int(num)
    return num


def infix_to_postfix(tokens: list) -> list:
    """
    중위 표현식을 후위 표현식으로 변환
    :param tokens: List
    :return: List
    """
    operator = {'+': 1, '-': 1, '*': 2, '/': 2, '%':2}
    postfix = []
    stack = []

    for token in tokens:
        if token in operator:
            if len(stack) == 0 or operator[stack[-1]] < operator[token]:
                stack.append(token)
                continue

            while len(stack) != 0 and operator[stack[-1]] >= operator[token]:
                postfix.append(stack.pop())
            stack.append(token)
            continue

        postfix.append(token)

    while len(stack) != 0:
        postfix.append(stack.pop())

    return postfix


def calculate(tokens: list) -> Union[int, float]:
    """
    후위 표현식 계산
    :param tokens: List
    :return: int or float
    """
    stack = []

    for token in tokens:
        if token == '+':
            stack.append(stack.pop() + stack.pop())
        elif token == '-':
            stack.append(-(stack.pop() - stack.pop()))
        elif token == '*':
            stack.append(stack.pop() * stack.pop())
        elif token == '/':
            rv = stack.pop()
            stack.append(stack.pop() / rv)
        elif token == '%':
            stack.append(stack.pop() / 100)
        else:
            stack.append(str_to_num(token))
    return stack.pop()


def get_expression_result(cal_db: dict, user_id: int) -> str:
    """
    1. 중위표현식 -> 후위표현식으로 변환
    2. 후위표현식 계산
    3. 계산식과 결과 생성
    :param cal_db: dict[List, List]
    :param user_id: int
    :return: str
    """
    postfix = infix_to_postfix(cal_db[user_id]["expression"])
    result = calculate(postfix)

    cal_db[user_id]["expression"].append('=')
    cal_db[user_id]["expression"].append(str(float_to_int(result)))

    expression = " ".join(cal_db[user_id]["expression"])
    print(cal_db[user_id]["history"])
    cal_db[user_id]["history"].append(expression)
    cal_db[user_id]["expression"] = []

    return expression
