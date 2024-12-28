import time
import asyncio


def question():
    print("sync: 답이 하나도 안 맞잖아")
    time.sleep(3)


def answer():
    print("sync: 하지만 빨랐죠")


async def question_async():
    print("async: 답이 하나도 안 맞잖아")
    await asyncio.sleep(3)


async def answer_async():
    print("async: 하지만 빨랐죠")


def main():
    question()
    answer()


async def main_async():
    await asyncio.gather(question_async(), answer_async())


if __name__ == "__main__":
    main()
    asyncio.run(main_async())
