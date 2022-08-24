# iamdt_backend



FastAPI 프레임워크를 이용한 계산기 API 서버 구현

## 

## 목차

- [개발 기간](#--개발-기간--)  
- [프로젝트 설명 및 분석](#-프로젝트)
- [API 사용법](#API) 
  <br><br>

<h2> ⌛ 개발 기간  </h2> 

 2022/08/22  ~ 2022/08/25
<br><br>
  </div> 


# 💻 프로젝트

  ### 문제 정의 및 해결 방법

  - 계산기의 버튼 누르면 서버 API를 호출하고, `=` 를 입력하면 계산식과 결과를 전달한다.

    - `POST`  method를 이용해 계산기 버튼 값을 입력받아 계산식을 저장함. 
    - `GET` method를 이용해 `=` 를 입력하면 계산식과 결과값 보여줌.
  - 계산식 입력 및 수식 계산
      - 입력받은 계산식은 List에 `String` 으로 저장 
    - 스택 자료구조를 이용해 계산식을 infix -> postfix로 변경
      - 예) 1 * 2 + 3 = 12*3+ 
    - postfix식을 계산하여 결과값 도출
      - 스택을 이용해 계산
    - 계산식에서 결과값을 정수 or 실수 판별하여 형변환
      - 예) 1 + 2.1 - 0.1 = 3.0 -> 1 + 2.1 - 0.1 = 3
    - 부호 버튼 처리
      - 부호 상태를 저장하는 변수를 만들어 부호 변경
  - 예외 상황 처리
      - Exception 또는 raise 사용
    - 올바른 계산식이 아닐 때,  `=`를 입력받아 계산 결과를 요청할 때
      - 1 + 2 *
    - 첫번째 입력을 operator로 받을 때
      - +, -, *, /
    - ZeroDivisionError
      - 8 / 0
    - 계산식을 만든 이력이 없는 유저가 계산 수식 목록을 요청할 때
  - pytest로 테스트 진행  (8개 pass)

    - 첫번째 입력을 operator로 했을 경우
    - 수식을 입력하는 도중에 부호 버튼을 입력했을 경우
    - 수식을 입력하는 도중에 부호 버튼을 입력하지 않을 경우
    - 수식이 완성되지 않았을 때, `=`버튼을 누른 경우
    - 올바른 수식이 완성되고, `=`버튼을 누른 경우 (부호 버튼 입력 안함)
    - 올바른 수식이 완성되고, `=`버튼을 누른 경우 (부호 버튼 입력)
    - 계산식을 만든 유저가 수식 목록을 요청한 경우
    - 계산식을 만들지 않은 유저가 수식 목록을 요청한 경우

<br>

### DB

- Dictionary type의 Mocking DB 생성

  ```json
    {
      "user_id":{
            "expression": ["1", "+", "2", "*", "1.0"],  
            "history": [],
            "sign": "False"
        }
    }
  ```

<br>
<br>

  ### 실행 방법

```python
git clone https://github.com/blueknarr/iamdt_backend.git

# 폴더 변경
cd iamdt_backend\

# 패키지 설치
pip install -r requirements.txt

# app 실행
uvicorn app.main:app --reload
    
```

<br>

  - 계산기 UI에서 숫자 또는 기호 입력 받아 계산식 만들기
      - "id": 숫자 입력
          - 예) "id": 0

<img src="https://user-images.githubusercontent.com/44389424/186443883-f4a5ac9d-94c8-46d0-8f7d-03b37b50fb61.JPG"/>

<br>

  - 계산식에 대한 결과 받기
      - user_id에 "id" 입력
          - 예) 0

<img src="https://user-images.githubusercontent.com/44389424/186443908-d1b44f44-1177-4dcb-a9dc-8f2beba00a00.JPG" />

<br>

  - 계산 목록 조회
      - user_id에 "id" 입력
          - 예) 0

<img src="https://user-images.githubusercontent.com/44389424/186443923-c5807988-5518-42f0-a8ea-eb47c8ca1261.JPG"/>

<br>
<br>



  ### API 명세서

| METHOD | URI                                 | 기능             |
| ------ | ----------------------------------- | ---------------- |
| GET    | /api/v1/calculator/{user_id}/result | 계산식 결과 조회 |
| GET    | /api/v1/calculator/{user_id}        | 계산식 목록 조회 |
| POST   | /api/v1/calculator                  | 계산식 생성      |

<br>
<br>

## API

API 사용법을 안내합니다.



### 계산식 결과 조회 

계산식 결과를 조회합니다. 계산기 UI에서  `=` 버튼을 누르면 을 `GET`으로 계산식과 결과를 요청하고, 성공 시 응답 바디에 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
GET /api/v1/calculator/{user_id}/result HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter:Path

| Name    | Type  | Description | Required |
| :------ | :---- | :---------- | :------- |
| user_id | `Int` | 유저 아이디 | O        |




#### Response

| Name   | Type   | Description      |
| :----- | :----- | :--------------- |
| result | `Dict` | 등록 결과 메세지 |



#### Result

##### Response: 성공

```json
{
  "msg": "수식이 입력되었습니다."
}
```

##### Response: 실패

```json
{
  "detail": "올바른 수식이 아닙니다."
}
```

<br>

### 계산식 목록 조회 

계산식 목록을 조회합니다.  `GET`으로 계산식 목록을 요청하고, 성공 시 응답 바디에 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
GET /api/v1/calculator/{user_id} HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter:Path

| Name    | Type  | Description | Required |
| :------ | :---- | :---------- | :------- |
| user_id | `Int` | 유저 아이디 | O        |




#### Response

| Name   | Type   | Description      |
| :----- | :----- | :--------------- |
| result | `Dict` | 등록 결과 메세지 |



#### Result

##### Response: 성공

```json
{
  "msg": "['1 * 2 + 3 = 5']"
}
```

##### Response: 실패

```json
{
  "detail": "계산기를 사용한 이력이 없습니다."
}
```

<br>

### 계산식 생성 

계산식을 생성합니다. 계산기 UI에서 버튼을 입력하면  `POST`로 api 서버로 전달하고, 성공 시 응답 바디에 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/v1/calculator HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter:Path

| Name    | Type  | Description | Required |
| :------ | :---- | :---------- | :------- |
| user_id | `Int` | 유저 아이디 | O        |




#### Response

| Name   | Type   | Description      |
| :----- | :----- | :--------------- |
| result | `Dict` | 등록 결과 메세지 |



#### Result

##### Response: 성공

```json
{
  "msg": "수식이 입력되었습니다."
}
```

##### Response: 실패

```json
{
  "detail": "올바른 수식이 아닙니다."
}
```

<br>