#coding: utf8
import math


def toi(v):
    try:
        return int(v)
    except:
        return 0


class Paginator(object):

    def __init__(self, objects, number_per_page):
        self.objects = objects

        self.number_per_page = number_per_page
        
        self.count = self.objects.count()
        self.num_pages = math.ceil(self.count / self.number_per_page)

        self.number = 0

    def page(self, num):
        self.number = self._purify_number(num)
        self.objects = self.objects.paginate(self.number, self.number_per_page)
        return self

    def has_previous(self):
        return self.number > 1

    def previous_page_number(self):
        return self._purify_number(self.number - 1)

    def has_next(self):
        return self.number < self.num_pages

    def next_page_number(self):
        return self._purify_number(self.number + 1)

    def _purify_number(self, number):
        try:
            number = int(number)
        except (TypeError, ValueError):
            number = 1

        if number < 1:
            number = 1

        if number > self.num_pages:
            number = self.num_pages

        return number
