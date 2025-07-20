from gyvatukas.www.ntfy_io import NtfyIO, NtfyIOParams

def test_ntfyio_post():
    client = NtfyIO()
    payload = NtfyIOParams(
        topic="pauliusbaulius-gyvatukas-test",
        message="hello, world!",
        title="test",
        tags=["test", "gyvatukas"],
        priority=1,
    )
    resp = client.post(payload)
    # ntfy.sh returns 200 and a JSON dict with at least an 'id' field for JSON publish
    assert isinstance(resp, dict)
    assert resp.get("id")
    assert resp.get("topic") == "pauliusbaulius-gyvatukas-test"
