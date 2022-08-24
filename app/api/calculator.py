from app.schemas.calculator import Calculator
from fastapi import APIRouter, HTTPException, status

from app.utils.calculator_utils import is_operator, change_sign

router = APIRouter()
calculator_db: dict = {}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_expression(calculator: Calculator):
    """
    계산기 버튼에서 입력받아 계산식 생성
    1. C 버튼 입력 - 계산식 초기화
    2. 첫 입력이 operator - 올바른 계산식이 아님
    3. 연산자를 연달아 입력하면, 마지막으로 입력한 연산자로 변경
    4. +/- 버튼 입력 - 부호 변경
    """

    if calculator.button == "C":
        calculator_db[calculator.id] = {"expression": [], "sign": False}
    else:
        if calculator.id in calculator_db:
            if len(calculator_db[calculator.id]["expression"]) > 0 and is_operator(calculator_db[calculator.id]["expression"][-1]) and is_operator(calculator.button):
                # operator를 연달아 입력하면, 마지막으로 입력한 연산자로 변경
                calculator_db[calculator.id]["expression"][-1] = calculator.button
            elif len(calculator_db[calculator.id]["expression"]) == 0 and is_operator(calculator.button):
                # 첫 입력이 operator - 올바른 계산식이 아님
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="올바른 수식이 아닙니다."
                )
            else:
                # 부호 변경을 입력받았을 때, 숫자만 부호 변경
                if calculator.button == "sign":
                    change_sign(calculator_db, calculator.id)
                else:
                    calculator_db[calculator.id]["expression"].append(calculator.button)
                    if calculator_db[calculator.id]["sign"]:
                        change_sign(calculator_db, calculator.id)
        else:
            # 첫번째 입력이 operator일 때, 에러 발생
            if is_operator(calculator.button):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="올바른 수식이 아닙니다.")

            calculator_db[calculator.id] = {
                "expression": [],
                "history": [],
                "sign": False,

            }
            if calculator.button == "sign":
                change_sign(calculator_db, calculator.id)
            else:
                calculator_db[calculator.id]["expression"].append(calculator.button)
                if calculator_db[calculator.id]["sign"]:
                    change_sign(calculator_db, calculator.id)

    return {"msg": "수식이 입력되었습니다."}
