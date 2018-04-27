import pytest


def test_webhooksecret():
    from chatbot.views import AxWebhook

    assert AxWebhook.webhooksecret is None

    with pytest.raises(AttributeError) as exc:
        AxWebhook().get_webhooksecret()

    assert "'Settings' object has no attribute 'AX_WEBHOOKSECRET'" in str(exc)
