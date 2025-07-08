import asyncio
from test_runner.playwright_test import run_test
from test_runner.email_sender import send_email

async def main():
    results = await run_test()
    send_email("Qubed.pk Website Test Report", results)

if __name__ == "__main__":
    asyncio.run(main())
