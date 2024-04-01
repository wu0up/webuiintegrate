import aiohttp, logging, json
from config import configs as p


async def requestsApi(method,
                      url,
                      body=None,
                      headers={},
                      verify=p.SKIP_TLS,
                      timeout=p.IFPS_TIME_OUT):

    try:
        if body is not None and not isinstance(body, dict):
            body = json.loads(body)
        async with aiohttp.ClientSession() as session:
            async with getattr(session,
                               method.lower())(url,
                                               headers=headers,
                                               json=body,
                                               ssl=p.SKIP_TLS) as response:
                res = await response.json()
                r_status = response.status
                return res, r_status

    except Exception as e:
        res = e
        r_status = 500
        logging.error(f"[REQ] url res: {e}, {url}")
        return res, r_status
