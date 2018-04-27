import pytest


def test_instant_id():
    from chatbot.views import Ax

    assert Ax.instant_id is None

    with pytest.raises(AttributeError) as exc:
        Ax().get_instantid(request=None)

    assert "'Settings' object has no attribute 'AX_INSTANT_ID'" in str(exc)
