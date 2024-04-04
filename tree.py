"""CSC111 Winter 2024 Project 2

Module Description
==================
This module contains the Tree class as well as various methods and functions to build
and traverse the decision tree.

Copyright and Usage Information
===============================
This file is Copyright (c) 2024 Akanksha Anand Iyengar, Leilia Ho, Diana Akhmedova, Herena Li
"""
from __future__ import annotations

import csv
import ast
from typing import Any, Optional
from recipes import Recipe


# @check_contracts
class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree)
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.__contains__(1)
        True
        >>> t.__contains__(5)
        True
        >>> t.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def remove(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Do nothing if the item is not in this tree.
        Return whether the given item was deleted.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()  # delete the root
            return True
        else:
            for subtree in self._subtrees:
                deleted = subtree.remove(item)
                if deleted and subtree.is_empty():
                    # The item was deleted and the subtree is now empty.
                    # We should remove the subtree from the list of subtrees.
                    # Note that mutate a list while looping through it is
                    # EXTREMELY DANGEROUS!
                    # We are only doing it because we return immediately
                    # afterward, and so no more loop iterations occur.
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:
                    # The item was deleted, and the subtree is not empty.
                    return True

            # If the loop doesn't return early, the item was not deleted from
            # any of the subtrees. In this case, the item does not appear
            # in this tree.
            return False

    def _delete_root(self) -> None:
        """Remove the root item of this tree.

        Preconditions:
            - not self.is_empty()
        """
        if self._subtrees == []:
            self._root = None
        else:
            # Strategy: Promote a subtree (the rightmost one is chosen here).
            # Get the last subtree in this tree.
            last_subtree = self._subtrees.pop()

            self._root = last_subtree._root
            self._subtrees.extend(last_subtree._subtrees)

    ############################################################################
    # Part 2.1: Tree methods
    ############################################################################
    def __repr__(self) -> str:
        """Return a one-line string representation of this tree.

        >>> t = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t
        Tree(2, [Tree(4, []), Tree(5, [])])
        """

        if self.is_empty():  # tree is empty
            return 'Tree(None, [])'
        elif not self._subtrees:  # tree is a single value
            return f'Tree({self._root}, [])'
        else:  # tree has at least one subtree
            subtree_list = []
            for subtree in self._subtrees:
                subtree_list.append(subtree.__repr__())
            subtree_rep = ', '.join(subtree_list)
            return f'Tree({self._root}, [{subtree_rep}])'

    def insert_sequence(self, items: list) -> None:
        """Insert the given items into this tree.

        The inserted items form a chain of descendants, where:
            - items[0] is a child of this tree's root
            - items[1] is a child of items[0]
            - items[2] is a child of items[1]
            - etc.

        Do nothing if items is empty.

        The root of this chain (i.e. items[0]) should be added as a new subtree within this tree, as long as items[0]
        does not already exist as a child of the current root node. That is, create a new subtree for it
        and append it to this tree's existing list of subtrees.

        If items[0] is already a child of this tree's root, instead recurse into that existing subtree rather
        than create a new subtree with items[0]. If there are multiple occurrences of items[0] within this tree's
        children, pick the left-most subtree with root value items[0] to recurse into.

        Hints:

        To do this recursively, you'll need to recurse on both the tree argument
        (from self to a subtree) AND on the given items, using the "first" and "rest" idea
        from RecursiveLists. To access the "rest" of a built-in Python list, you can use
        list slicing: items[1:len(items)] or simply items[1:], or you can use a recursive helper method
        that takes an extra "current index" argument to keep track of the next move in the list to add.

        Preconditions:
            - not self.is_empty()

        >>> t = Tree(111, [])
        >>> t.insert_sequence([1, 2, 3])
        >>> print(t)
        111
          1
            2
              3
        >>> t.insert_sequence([1, 3, 5])
        >>> print(t)
        111
          1
            2
              3
            3
              5
        """

        if not items:
            return None
        elif self.is_empty():
            self.add_sequence_empty_tree(items)
        elif items[0] not in [sub._root for sub in self._subtrees]:
            new_tree = Tree(None, [])
            new_tree.add_sequence_empty_tree(items)
            self._subtrees.append(new_tree)
        else:
            for subtree in self._subtrees:
                if items[0] == subtree._root:
                    subtree.insert_sequence(items[1:])
                    return None

        return None

    def add_sequence_empty_tree(self, items: list) -> None:
        """Insert the given items into this empty tree. Helper method for insert_sequence.

        Preconditions:
            - self.is_empty()

        >>> t = Tree(None, [])
        >>> t.add_sequence_empty_tree([1, 2, 3])
        >>> print(t)
        1
          2
            3
        """
        if not items:
            return None
        elif len(items) == 1:
            self._root = items[0]
        else:
            self._root = items[0]
            new_tree = Tree(None, [])
            new_tree.add_sequence_empty_tree(items[1:])
            self._subtrees = [new_tree]

        return None

    def check_equality(self, features: list) -> list:
        """Returns a list of the values of the leaves of the tree with the same ancestors as the given list of items,
        excluding the root of the tree. If the tree is empty or the ancestors are not the same, return an empty list.

        Helper method for run_animal_guesser.

        Preconditions:
            - len(items) == (height of the tree - 2)
            - height of the tree > 2
            - all children of the root have the same length
        """
        # main/side/dessert -> difficulty (5 10 20 30+) -> time (30 80 160 240 240+) -> cal (500-2000+)
        if self.is_empty() or features == []:
            return []
        else:
            leaves = []
            for subtree in self._subtrees:
                item = features[0]
                is_int = item.isdigit()
                has_plus = '+' in subtree._root

                if item == subtree._root and not subtree._subtrees[0]._subtrees:
                    subtree.append_leaves(leaves)
                elif item == subtree._root:
                    leaves.extend(subtree.check_equality(features[1:]))

                elif (has_plus and int(item) >= int(subtree._root[:len(subtree._root) - 1]) and
                      not subtree._subtrees[0]._subtrees):
                    subtree.append_leaves(leaves)
                elif has_plus and int(item) >= int(subtree._root[:len(subtree._root) - 1]):
                    leaves.extend(subtree.check_equality(features[1:]))

                elif not has_plus and is_int and int(item) <= int(subtree._root) and not subtree._subtrees[0]._subtrees:
                    subtree.append_leaves(leaves)
                elif not has_plus and is_int and int(item) <= int(subtree._root):
                    leaves.extend(subtree.check_equality(features[1:]))

            return leaves

    def append_leaves(self, lst: list) -> None:
        """Append the roots of the subtrees of this tree to the given list. Helper method for check_equality.
        """
        for sub in self._subtrees:
            lst.append(sub._root)


# @check_contracts
def build_decision_tree(file: str) -> Tree:
    """Build a decision tree storing the recipe data from the given file.

    Preconditions:
        - file is the path to a csv file in the format of the filtered_merged.csv
    """
    tree = Tree('', [])  # The start of a decision tree

    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row

        for row in reader:
            name = row[5]
            cooking_time = int(row[6])
            ratings = row[3].split(',')
            average_rating = sum(int(rating) for rating in ratings) // len(ratings)
            ingredients = ast.literal_eval(row[14])
            steps = ast.literal_eval(row[12])
            calories = float(ast.literal_eval(row[10])[0])
            tags = ast.literal_eval(row[9])
            recipe = Recipe(name, cooking_time, average_rating, ingredients, steps, calories, tags)
            new_branch = []

            # food preference
            tags = ast.literal_eval(row[9])
            if 'main-dish' in tags:
                new_branch.append('main dish')
            elif 'side-dishes' in tags:
                new_branch.append('side dish')
            elif 'desserts' in tags:
                new_branch.append('dessert')
            else:
                new_branch.append('other')

            # difficulty
            n_steps = int(row[11])
            if n_steps < 5:
                new_branch.append('5')
            elif n_steps < 10:
                new_branch.append('10')
            elif n_steps < 20:
                new_branch.append('20')
            elif n_steps < 30:
                new_branch.append('30')
            else:
                new_branch.append('30+')

            # amount of time
            if cooking_time < 30:
                new_branch.append('30')
            elif cooking_time < 80:
                new_branch.append('80')
            elif cooking_time < 160:
                new_branch.append('160')
            elif cooking_time < 160:
                new_branch.append('240')
            else:
                new_branch.append('240+')

            # calories
            if calories < 500:
                new_branch.append('500')
            elif calories < 1000:
                new_branch.append('1000')
            elif calories < 1500:
                new_branch.append('1500')
            elif calories < 2000:
                new_branch.append('2000')
            else:
                new_branch.append('2000+')

            new_branch.append(recipe)
            tree.insert_sequence(new_branch)
    return tree


def filter_recipes(recipes: list[Recipe], allergens: list[str], diet: list[str], food: list[str], cuisine: list[str],
                   other: list[str]) -> list[Recipe]:
    """Return a filtered list of recipes based on the provided allergy and diet preference data.
    """
    filtered_recipes = {}
    final = {}
    # for recipe in recipes:
    #     if not any(allergen in ingredient for allergen in allergens for ingredient in recipe.ingredients):
    #         # if len(food) >= 1 and any(f in recipe.name for f in food):
    #         #     filtered_recipes[recipe] = 0
    #         # else:
    #         filtered_recipes[recipe] = 0
    #
    # for recipe in filtered_recipes:
    #     if diet in recipe.tags:
    #         final[recipe] = 0
    for recipe in recipes:
        if allergens != [''] and any([allergen in ingredient for allergen in allergens
                                            for ingredient in recipe.ingredients]):
            # recipes.remove(recipe)
            pass
        elif len(food) >= 1 and any(f in recipe.name for f in food):
            filtered_recipes[recipe] = 0
        else:
            filtered_recipes[recipe] = 0

    for recipe in filtered_recipes:
        if diet not in recipe.tags:
            final[recipe] = 0

    for recipe in final:
        includes_tags = [o for o in other if o in recipe.tags]
        has_cuisine = any(c in recipe.tags for c in cuisine)
        final[recipe] += len(includes_tags)
        if has_cuisine:
            final[recipe] += 1

    sorted_final = sorted(final.items(), key=lambda x: x[1], reverse=True)
    return [r[0] for r in sorted_final]


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all('tree.py', config={
        'max-line-length': 120,
        'extra-imports': ['csv', 'ast', 'recipes'],
        'allowed-io': ['build_decision_tree']
    })
