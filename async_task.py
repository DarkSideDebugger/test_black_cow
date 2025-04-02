import asyncio
import aiohttp


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            return result


async def fetch_with_timeout(url, timeout=1.0):
    try:
        result = await asyncio.wait_for(fetch_url(url), timeout=timeout)
        print(f"Success for {url}: {result}")
        return result
    except asyncio.TimeoutError:
        print(f"Error: Request to {url} timed out after {timeout} seconds")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None


async def main(urls):
    tasks = [fetch_with_timeout(url) for url in urls]
    results = await asyncio.gather(*tasks)

    success_count = sum(1 for res in results if res is not None)
    print(f"Successfully fetched {success_count} out of {len(urls)} URLs")
    return success_count


if __name__ == "__main__":
    urls_list = [
        # Timeout url so the order doesn't matter, and it doesn't affect the results
        "https://httpbin.org/delay/2"
        # Valid urls
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
        # Timeout url
        "https://httpbin.org/delay/2"
    ]
    asyncio.run(main(urls_list))
