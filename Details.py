class Details(object):
    _instance = None

    def __init__(self):
        self.days = self.slots = self.courses_happiness = self.professors_courses = \
            self.collision_penalties = self.courses_count = self.courses_profs = None
        self.read_inputs_from_std_in()

    def read_inputs_from_std_in(self):
        self.days, self.slots = (int(num) for num in input().split(" "))

        self.courses_count = int(input())
        self.courses_happiness = []

        inp_parts = input().split(" ")
        for i in range(self.courses_count):
            self.courses_happiness.append(int(inp_parts[i]))

        self.professors_courses = []
        num_of_profs = int(input())
        for i in range(num_of_profs):
            professor_courses = []
            inp_parts = input().split(" ")
            num_of_prof_courses = int(inp_parts[0])
            for j in range(1, num_of_prof_courses + 1):
                professor_courses.append(int(inp_parts[j]) - 1)
            self.professors_courses.append(professor_courses)

        self.collision_penalties = []
        for i in range(self.courses_count):
            inp_parts = input().split(" ")
            collision_penalty = []
            for j in range(self.courses_count):
                collision_penalty.append(int(inp_parts[j]))
            self.collision_penalties.append(collision_penalty)

        self.courses_profs = self.extract_courses_profs()

    def extract_courses_profs(self):
        courses_profs = [[] for i in range(self.courses_count)]
        for i in range(len(self.professors_courses)):
            for j in range(len(self.professors_courses[i])):
                courses_profs[self.professors_courses[i][j]].append(i)

        return courses_profs


def singleton(klass):
    def inner_singleton():
        if klass._instance is None:
            klass._instance = klass()
        return klass._instance

    return inner_singleton


get_details_instance = singleton(Details)
