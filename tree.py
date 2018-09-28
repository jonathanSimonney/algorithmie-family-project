from pprint import pprint


class Person:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age


class Tree:
    def __init__(self, root_element):
        self.elements = {}
        self._id = 1
        self.elements[self._id] = {'id': self._id, 'content': root_element, 'parent_id': -1}
        self._id += 1

    def add_child(self, elem, finder_func):
        placed_elem = self._find_first_single(finder_func)
        if placed_elem is None:
            raise NotImplementedError('you must give a finder_func which finds something!')
        parent_elem_id = placed_elem['id']
        self.elements[self._id] = {'id': self._id, 'content': elem, 'parent_id': parent_elem_id}
        self._id += 1

    def add_ancestor(self, elem, finder_func):
        placed_elem = self._find_first_single(finder_func)
        if placed_elem is None:
            raise NotImplementedError('you must give a finder_func which finds something!')
        children_elem_id = placed_elem['id']
        self.elements[self._id] = {'id': self._id, 'content': elem, 'parent_id': -1}
        self.elements[children_elem_id]['parent_id'] = self._id
        self._id += 1

    def _find_first_single(self, finder_func):
        for key, placed_elem in self.elements.items():
            if finder_func(placed_elem):
                return placed_elem
        return None

    def find_most_by_criteria(self, callback_criteria):
        best_criteria_value = None
        best_elem = None
        for key, placed_elem in self.elements.items():
            if best_criteria_value is None:
                best_criteria_value = callback_criteria(placed_elem)
                best_elem = placed_elem
            elif callback_criteria(placed_elem) > best_criteria_value:
                best_criteria_value = callback_criteria(placed_elem)
                best_elem = placed_elem
        return best_elem['content']

    def find_how_many_respect_criteria(self, callback_criteria):
        ret = 0
        for key, placed_elem in self.elements.items():
            if callback_criteria(placed_elem):
                ret += 1
        return ret

    def list_ancestors(self, finder_func, ret=[]):
        placed_elem = self._find_first_single(finder_func)

        if placed_elem['parent_id'] == -1:
            return ret
        ancestor = self.elements[placed_elem['parent_id']]
        ret.append(ancestor['content'])
        return self.list_ancestors(finder_by_name_generator(ancestor['content'].name), ret)


def finder_by_name_generator(name):
    return lambda placed_elem: placed_elem['content'].name == name


tree = Tree(Person('Amélie', 'woman', 104))
tree.add_child(Person('Roseline', 'woman', 79), finder_by_name_generator('Amélie'))
tree.add_child(Person('Jack', 'man', 86), finder_by_name_generator('Amélie'))
tree.add_child(Person('Olivier', 'man', 59), finder_by_name_generator('Jack'))
tree.add_child(Person('Pascal', 'man', 59), finder_by_name_generator('Jack'))
tree.add_child(Person('Charlotte', 'woman', 22), finder_by_name_generator('Olivier'))
tree.add_child(Person('Angélique', 'woman', 18), finder_by_name_generator('Olivier'))
tree.add_child(Person('Lucien', 'man', 7), finder_by_name_generator('Olivier'))
tree.add_child(Person('Julien', 'man', 33), finder_by_name_generator('Pascal'))
tree.add_child(Person('Caroline', 'woman', 30), finder_by_name_generator('Pascal'))

pprint(vars(tree.find_most_by_criteria(lambda placed_elem: placed_elem['content'].age)))  # get the oldest
pprint(vars(tree.find_most_by_criteria(lambda placed_elem: -placed_elem['content'].age)))  # get the youngest
print(tree.find_how_many_respect_criteria(lambda placed_elem: placed_elem['content'].gender == 'woman'))  # find how many woman there are
pprint(vars(tree.find_most_by_criteria(lambda placed_elem: tree.find_how_many_respect_criteria(lambda inner_placed_elem: inner_placed_elem['parent_id'] == placed_elem['id']))))  # get the one with most children
pprint(tree.list_ancestors(finder_by_name_generator(tree.find_most_by_criteria(lambda placed_elem: -placed_elem['content'].age).name)))  # lister l'ascendance du plus jeune

tree.add_child(Person('NewBorn', 'man', 0.5), finder_by_name_generator('Julien'))
pprint(vars(tree.find_most_by_criteria(lambda placed_elem: -placed_elem['content'].age)))  # get the youngest
