import pytest
import asyncio
from unittest.mock import patch
from async_task import fetch_url, fetch_with_timeout, main


class MockResponse:
    def __init__(self, json_data, status=200):
        self.json_data = json_data
        self.status = status

    async def json(self):
        return self.json_data


@pytest.mark.asyncio
async def test_fetch_url():
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_response = MockResponse({"id": 1, "title": "Test"})
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await fetch_url("https://test.com/api")
        assert result == {"id": 1, "title": "Test"}


@pytest.mark.asyncio
async def test_fetch_with_timeout_success():
    with patch('async_task.fetch_url') as mock_fetch:
        mock_fetch.return_value = {"data": "success"}
        result = await fetch_with_timeout("https://test.com/api")
        assert result == {"data": "success"}


@pytest.mark.asyncio
async def test_fetch_with_timeout_timeout():
    with patch('async_task.fetch_url') as mock_fetch:
        mock_fetch.side_effect = asyncio.TimeoutError()
        result = await fetch_with_timeout("https://test.com/api")
        assert result is None


@pytest.mark.asyncio
async def test_main_mixed_results():
    with patch('async_task.fetch_with_timeout') as mock_fetch:
        async def side_effect(url):
            if url == "https://test.com/1":
                return {"id": 1}
            else:
                return None

        mock_fetch.side_effect = side_effect

        urls = ["https://test.com/1", "https://test.com/2"]
        success_count = await main(urls)

        assert success_count == 1