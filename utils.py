import random
from math import floor


def get_random_professor(course_index, courses_profs):
    prof_num = int(floor(random.random() * len(courses_profs[course_index])))
    return courses_profs[course_index][prof_num]
