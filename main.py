import re
import time
from datetime import datetime
from typing import Callable, Literal

from playwright.sync_api import Locator, TimeoutError


class CustomExpect:

    def __call__(self, locator: Locator):
        self.locator = locator
        return Expects(self.locator)


custom_expect = CustomExpect()


class Expects:
    def __init__(self, locator: Locator) -> None:
        self.locator = locator
        self.__timeout = 200

    @staticmethod
    def __wait_to_be_true(assertion_time: int = 7000, error_message: str | None = None):
        """
        :param assertion_time: time after which expectation will throw an AssertionError
        :param error_message: what message will be shown after the AssertionError
        :return:
        """
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                time_before = time.time()
                assertion = False
                while assertion is False:
                    assertion = func(*args, **kwargs)
                    if time.time() - time_before >= assertion_time / 1000:
                        break
                assert assertion, error_message
                return assertion
            return wrapper
        return decorator

    @__wait_to_be_true(error_message="Integer doesn't face the requriments")
    def to_have_int(self,
                    comparison: Literal['gt', 'gte', 'lt', 'lte'],
                    than_value: float):
        assertions_list = []
        for locator in self.locator.all():
            try:
                current = int(''.join(re.findall(r'\d+', locator.inner_text(timeout=self.__timeout))))
                if comparison == 'gt':
                    assertions_list.append(current > than_value)
                if comparison == 'gte':
                    assertions_list.append(current >= than_value)
                if comparison == 'lt':
                    assertions_list.append(current < than_value)
                if comparison == 'lte':
                    assertions_list.append(current <= than_value)
            except TimeoutError:
                return False
        return len(set(assertions_list).difference([True])) == 0

    @__wait_to_be_true(error_message="Text doesn't face the requriments")
    def to_have_text(self, comparison: Literal['startswith', 'endswith'], value: str):
        assertions_list = []
        for locator in self.locator.all():
            try:
                if comparison == 'startswith':
                    assertions_list.append(locator.inner_text(timeout=self.__timeout).startswith(value))
                if comparison == 'endswith':
                    assertions_list.append(locator.inner_text(timeout=self.__timeout).endswith(value))
            except TimeoutError:
                return False
        return len(set(assertions_list).difference([True])) == 0

    @__wait_to_be_true(error_message="Time doesn't face the requriments")
    def to_have_time(self, comparison: Literal['not_equal', 'equal', 'before', 'after'], value: datetime):
        assertions_list = []
        for column in self.locator.all():
            try:
                if len(column.inner_text(timeout=self.__timeout)) > 0:
                    current = datetime.strptime(column.inner_text(timeout=200), '%H:%M:%S').time()
                    if comparison == 'not_equal':
                        assertions_list.append(current != value.time())
                    if comparison == 'equal':
                        assertions_list.append(current == value.time())
                    if comparison == 'after':
                        assertions_list.append(current >= value.time())
                    if comparison == 'before':
                        assertions_list.append(current <= value.time())
            except TimeoutError:
                return False
        return len(set(assertions_list).difference([True])) == 0
