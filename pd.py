#! venv/bin/python3
from datetime import datetime
import json
import typing

from pydantic import BaseModel, ValidationError


class LobstersPost(BaseModel):
    created_at: datetime
    title: str
    url: str
    score: int
    comments_url: str
    tags: list[str]


def parse_post(post: dict) -> typing.Union[LobstersPost, None]:
    try:
        p = LobstersPost(**post)
        return p
    except ValidationError as e:
        print(e.errors())
        return None


def main():
    hottest = []
    with open("hottest.json") as f:
        hottest = json.load(f)

    posts: list[LobstersPost] = []
    for h in hottest:
        p = parse_post(h)
        if isinstance(p, LobstersPost):
            posts.append(p)
    for p in posts:
        print(p.title)


if __name__ == "__main__":
    main()
