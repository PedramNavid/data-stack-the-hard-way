from datetime import datetime
from typing import List
import random
from faker import Faker
from dataclasses import dataclass
from time import sleep


@dataclass(frozen=True)
class User:
    anonymous_id: str
    user_agent: str
    ip: str


@dataclass(frozen=True)
class PageEvent(User):
    event_id: str
    event_time: datetime
    page_title: str
    page_path: str
    page_url: str


@dataclass(frozen=True)
class TrackEvent(PageEvent):
    event_name: str


class UserGenerator:
    def __init__(self, n_seeds=100):
        self.faker = Faker()
        self.users = set()
        for _ in range(n_seeds):
            self._seed()

    def _seed(self):
        user = User(self.faker.uuid4(),
                self.faker.user_agent(),
                self.faker.ipv4())
        self.users.add(user)

    def user(self) -> User:
        user = self.users.pop()
        self.users.add(user)
        return user

    def todict(self):
        return self.__dict__


class FakePageEvents:
    def __init__(self):
        self.urls = []
        self.faker = Faker()
        self.create_data()

    def create_data(self, n_urls=3) -> None:
        for _ in range(n_urls):
            self.urls.append(self.faker.url(schemes=["https"]))

    def generate(self, user_generator: UserGenerator) -> PageEvent:
        user = user_generator.user()

        page = PageEvent(
            anonymous_id = user.anonymous_id,
            user_agent=user.user_agent,
            ip=user.ip,
            event_id=self.faker.uuid4(),
            event_time=self.faker.date_time_this_year(),
            page_title=self.faker.sentence(),
            page_path=self.faker.uri_path(),
            page_url=random.choice(self.urls),
        )
        return page


class FakeTrackEvents:
    def __init__(self):
        self.urls: List[str] = list()
        self.faker = Faker()
        self.create_data()

    def create_data(self, n_urls=3) -> None:
        for _ in range(n_urls):
            self.urls.append(self.faker.url(schemes=["https"]))

    def generate(self, user_generator: UserGenerator) -> TrackEvent:
        user = user_generator.user()
        page = TrackEvent(
            anonymous_id=user.anonymous_id,
            user_agent=user.user_agent,
            ip=user.ip,
            event_id=self.faker.uuid4(),
            event_time=self.faker.date_time_this_year(),
            event_name=" ".join(self.faker.words(nb=2)),
            page_title=self.faker.sentence(),
            page_path=self.faker.uri_path(),
            page_url=random.choice(self.urls),
        )
        return page


if __name__ == '__main__':
    user_gen = UserGenerator()

    for _ in range(1000):
        page = FakePageEvents()
        track = FakeTrackEvents()

        print(page.generate(user_gen))
        print(track.generate(user_gen))
        sleep(0.1)
