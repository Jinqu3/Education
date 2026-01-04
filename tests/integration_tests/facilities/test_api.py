async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200


async def test_post_facilities(ac):
    facility_title = "Test Facilities"
    response = await ac.post(
        "/facilities",
        json={
            "title": facility_title,
        },
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert "data" in res
    assert res["data"]["title"] == facility_title
