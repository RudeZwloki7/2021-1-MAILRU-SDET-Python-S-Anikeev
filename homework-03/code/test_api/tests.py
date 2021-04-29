import pytest

from test_api.base import ApiBase


@pytest.mark.API
class TestApiLogin(ApiBase):
    authorize = False

    def test_login(self, credentials):
        self.api_client.post_login(*credentials)


@pytest.mark.API
class TestApiCampaign(ApiBase):

    def test_create_campaign(self, generate_name, logo_path):
        self.api_client.post_create_campaign(generate_name, logo_path)


@pytest.mark.API
class TestApiSegment(ApiBase):

    def test_create_segment(self, generate_name):
        self.api_client.post_create_segment(generate_name)

    def test_delete_segment(self, generate_name):
        self.api_client.post_delete_segment(generate_name)
