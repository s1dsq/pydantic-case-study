#! venv/bin/python3

from dataclasses import dataclass
from datetime import datetime
import json
import typing

@dataclass
class LobstersPost:
    created_at: datetime
    title: str
    url: str
    score: int
    comments_url: str
    tags: list[str]


class ValidationError(Exception):
    def __init__(self, _errors):
        super().__init__(_errors)
        self._errors = _errors

    def errors(self):
        return self._errors


def parse_post(post: dict) -> typing.Union[LobstersPost, None]:
    created_at: datetime = datetime.now()
    title: str = ""
    url: str = ""
    score: int = 0
    comments_url: str = ""
    tags: list[str] = []

    try:
        errors = []
        for k, v in post.items():
            if k == "created_at":
                try:
                    created_at = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f%z")
                except ValueError as e:
                    errors.append("failed to parse datetime" + str(e))
            elif k == "title":
                if isinstance(v, str):
                    title = v
                else:
                    errors.append(f"cannot convert {type(v)} to str")
            elif k == "url":
                if isinstance(v, str):
                    url = v
                else:
                    errors.append(f"cannot convert {type(v)} to str")
            elif k == "score":
                if isinstance(v, int):
                    score = v
                else:
                    errors.append(f"cannot convert {type(v)} to int")
            elif k == "comments_url":
                if isinstance(v, str):
                    comments_url = v
                else:
                    errors.append(f"cannot convert {type(v)} to str")
            elif k == "tags":
                if isinstance(v, list):
                    tags = []
                    for tag in v:
                        if isinstance(tag, str):
                            tags.append(tag)
                        else:
                            errors.append(f"cannot convert {type(tag)} to int")
                else:
                    errors.append(f"cannot convert {type(v)} to list[str]")

        if len(errors) != 0:
            raise ValidationError(errors)
        return LobstersPost(
            created_at=created_at,
            title=title,
            url=url,
            score=score,
            comments_url=comments_url,
            tags=tags,
        )
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
