from uuid import uuid4

import pytest
from django.apps import apps


@pytest.fixture
def chatbot_models():
    chatbot_app = apps.get_app_config('chatbot')

    yield chatbot_app.get_models()


def test_chatbot_model_count(chatbot_models):
    assert len(list(chatbot_models)) == 1


@pytest.mark.django_db
def test_ax_response_create(chatbot_models):
    for model in chatbot_models:
        if model._meta.model_name == 'axresponse':
            break
    else:
        assert False, 'Model AxResponse is missing.'

    ax_response = model.objects.create(
        ax_uid=uuid4(),
        ax_error=False,
    )

    assert ax_response is not None
    assert isinstance(ax_response.pk, int)
