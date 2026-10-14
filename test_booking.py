
import requests
import pytest


BASE_URL = "https://restful-booker.herokuapp.com"


def test_get_booking_list():
    response = requests.get(
        f"{BASE_URL}/booking",
        timeout=15
    )

    # 检查 HTTP 请求是否成功
    assert response.status_code == 200

    # 检查响应是否为 JSON 列表
    data = response.json()
    assert isinstance(data, list)

    # 检查列表中的预订记录是否包含 bookingid
    if data:
        assert "bookingid" in data[0]

def test_get_booking_details():
    # 先获取当前存在的预订 ID
    list_response = requests.get(
        f"{BASE_URL}/booking",
        timeout=15
    )
    assert list_response.status_code == 200

    booking_list = list_response.json()
    assert len(booking_list) > 0

    # 选择当前列表中真实存在的 ID
    booking_id = booking_list[0]["bookingid"]

    response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=15
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    # 校验预订信息的关键字段
    assert "firstname" in data
    assert "lastname" in data
    assert "totalprice" in data
    assert "bookingdates" in data

def test_get_nonexistent_booking():
    # 查询一个极不可能存在的预订 ID
    response = requests.get(
        f"{BASE_URL}/booking/999999999",
        timeout=15
    )

    # 不存在的预订应返回 404
    assert response.status_code == 404

def test_get_booking_with_invalid_id():
    # 使用非法的 ID 格式
    response = requests.get(
        f"{BASE_URL}/booking/invalid",
        timeout=15
    )

    # 非法 ID 应返回 404
    assert response.status_code == 404

def test_create_booking():
    payload = {
        "firstname": "Chen",
        "lastname": "Test",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2027-05-01",
            "checkout": "2027-05-05"
        },
        "additionalneeds": "Breakfast"
    }

    response = requests.post(
        f"{BASE_URL}/booking",
        json=payload,
        timeout=15
    )

    # 校验创建成功
    assert response.status_code == 200

    data = response.json()

    # 校验返回了预订 ID
    assert isinstance(data["bookingid"], int)

    # 校验返回的预订信息与提交的数据一致
    booking = data["booking"]
    assert booking["firstname"] == payload["firstname"]
    assert booking["lastname"] == payload["lastname"]
    assert booking["totalprice"] == payload["totalprice"]
    assert booking["bookingdates"] == payload["bookingdates"]

def test_update_booking():
    # 1. 获取认证 Token
    auth_response = requests.post(
        f"{BASE_URL}/auth",
        json={
            "username": "admin",
            "password": "password123"
        },
        timeout=15
    )

    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    # 2. 创建一条专用于本测试的预订
    payload = {
        "firstname": "Chen",
        "lastname": "BeforeUpdate",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2027-05-01",
            "checkout": "2027-05-05"
        },
        "additionalneeds": "Breakfast"
    }

    create_response = requests.post(
        f"{BASE_URL}/booking",
        json=payload,
        timeout=15
    )

    assert create_response.status_code == 200
    booking_id = create_response.json()["bookingid"]

    # 3. 修改这条预订
    updated_payload = {
        "firstname": "Chen",
        "lastname": "AfterUpdate",
        "totalprice": 300,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2027-06-01",
            "checkout": "2027-06-05"
        },
        "additionalneeds": "Lunch"
    }

    update_response = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=updated_payload,
        headers={"Cookie": f"token={token}"},
        timeout=15
    )

    assert update_response.status_code == 200

    # 4. 查询并确认修改生效
    get_response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=15
    )

    assert get_response.status_code == 200
    actual = get_response.json()

    assert actual["lastname"] == "AfterUpdate"
    assert actual["totalprice"] == 300
    assert actual["depositpaid"] is False
    assert actual["bookingdates"] == updated_payload["bookingdates"]

def test_delete_booking():
    # 1. 获取认证 Token
    auth_response = requests.post(
        f"{BASE_URL}/auth",
        json={
            "username": "admin",
            "password": "password123"
        },
        timeout=15
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    # 2. 创建专用于本测试的预订
    payload = {
        "firstname": "Chen",
        "lastname": "DeleteTest",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2027-07-01",
            "checkout": "2027-07-05"
        },
        "additionalneeds": "None"
    }

    create_response = requests.post(
        f"{BASE_URL}/booking",
        json=payload,
        timeout=15
    )
    assert create_response.status_code == 200
    booking_id = create_response.json()["bookingid"]

    # 3. 删除预订
    delete_response = requests.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={token}"},
        timeout=15
    )
    assert delete_response.status_code == 201

    # 4. 验证预订已不存在
    verify_response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=15
    )
    assert verify_response.status_code == 404

@pytest.mark.parametrize(
    "username, password",
    [
        ("wrong_user", "password123"),
        ("admin", "wrong_password"),
        ("", ""),
    ],
)
def test_auth_with_invalid_credentials(username, password):
    response = requests.post(
        f"{BASE_URL}/auth",
        json={
            "username": username,
            "password": password,
        },
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert "reason" in data
    assert data["reason"] == "Bad credentials"
