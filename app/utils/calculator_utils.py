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