import pytest
from gyvatukas.www.github_com import GithubComNoAuth


class TestGithubComNoAuth:
    """Test unauthenticated GitHub client."""

    def test_init(self):
        client = GithubComNoAuth()
        assert client is not None

    @pytest.mark.integration
    def test_convert_md_to_html(self):
        """Test markdown to HTML conversion returns valid HTML."""
        client = GithubComNoAuth()
        result = client.convert_md_to_html("# Hello, world!")

        # Check that we got HTML output
        assert result.startswith("<")
        assert "h1" in result
        assert "Hello, world!" in result

    def test_api_version_header(self):
        """Test API version header generation."""
        headers = GithubComNoAuth._get_api_version_header()
        assert "X-GitHub-Api-Version" in headers
        assert headers["X-GitHub-Api-Version"] == "2022-11-28"

    def test_base_headers(self):
        """Test base headers generation."""
        client = GithubComNoAuth()
        headers = client._get_base_headers()

        assert "Accept" in headers
        assert "X-GitHub-Api-Version" in headers
        assert headers["Accept"] == "application/vnd.github+json"

    def test_auth_headers_no_auth(self):
        """Test auth headers for unauthenticated client."""
        client = GithubComNoAuth()
        headers = client._get_auth_headers()
        assert headers == {}
