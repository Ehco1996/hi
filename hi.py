import asyncio
import sys
import time
from collections import defaultdict
from dataclasses import dataclass

import aiohttp
import typer
from rich import print

REQ_NUM = 200
TCP_CNT = 50

SUMMARY_TMPL = """
Summary:
Total:          {total_sec} secs
Slowest:        {slowest} secs
Fastest:        {fastest} secs
Average:        {average} secs
Requests/sec:   {qps}

Status code distribution:
{status}
"""


@dataclass
class RequestMetric:
    duration: int = 0  # 毫秒
    status_code: int = 0


class Hi:
    @staticmethod
    def current_milli_time():
        return round(time.time() * 1000)

    def after_milli_time(self, t):
        return self.current_milli_time() - t

    async def send_get_request(
        self, session: aiohttp.ClientSession, url: str
    ) -> RequestMetric:
        m = RequestMetric()
        start = self.current_milli_time()
        async with session.get(url) as resp:
            await resp.text()
            m.duration = self.after_milli_time(start)
            m.status_code = resp.status
            return m

    def print_metrics(slef, total, metrics):
        status_code_dict = defaultdict(int)
        fastest = sys.maxsize
        slowest = -1
        duration_sum = 0
        for m in metrics:
            duration_sum += m.duration
            fastest = min(fastest, m.duration)
            slowest = max(fastest, m.duration)
            status_code_dict[m.status_code] += 1
        status = ""
        for code, cnt in status_code_dict.items():
            status += f"[{code}]        {cnt} responses\n"
        print(
            SUMMARY_TMPL.format(
                total_sec=round(total / 1000, 3),
                fastest=round(fastest / 1000, 3),
                slowest=round(slowest / 1000, 3),
                average=round((duration_sum / 1000) / len(metrics), 3),
                qps=round(len(metrics) / (total / 1000), 3),
                status=status,
            )
        )

    async def async_http_bench(self, url):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=TCP_CNT)
        ) as s:
            tasks = [self.send_get_request(s, url) for _ in range(REQ_NUM)]
            start = self.current_milli_time()
            metrics = await asyncio.gather(*tasks)
            self.print_metrics(self.after_milli_time(start), metrics)

    def http_bench(self, url: str = typer.Argument("url", help="url to send")):
        """say hi to request url"""
        print(f"Send request to {url}")
        asyncio.run(self.async_http_bench(url))


def main():
    h = Hi()
    typer.run(h.http_bench)


if __name__ == "__main__":
    main()
