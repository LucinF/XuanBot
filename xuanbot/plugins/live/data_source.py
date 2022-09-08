import json
import httpx

live_headers = {"Origin": "https://live.bilibili.com", "Accept": "application/json, text/plain, */*",
                "Connection": "close",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "Referer": "https://live.bilibili.com/", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Dest": "empty",
                "DNT": "1", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9",
                "Sec-Fetch-Mode": "cors"}

live_url = "https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"


async def get_live_status_list(uids) -> dict:
    data = json.dumps({'uids': uids})
    async with httpx.AsyncClient() as client:
        response = await client.post(headers=live_headers, url=live_url, data=data)   # type: ignore
        # print(response.json()["data"])
        return response.json()["data"]