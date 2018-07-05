from collections import deque
from unittest import TestCase

from fortnum import Fortnum, class_property, FortnumDescriptor
from fortnum.fortnum import FortnumMeta, UnableToAddRelatedFortnum, FortnumRelation


class FortnumCase(TestCase):
    def setUp(self):
        FortnumMeta._registry = {}  # Allow redeclaration between tests

    def testIn(self):
        child3 = Fortnum

        class Parent(Fortnum):
            child1 = Fortnum("child1")
            child2 = Fortnum("child2")

        self.assertIn(Parent.child1, Parent)
        self.assertIn(Parent.child2, Parent)
        self.assertNotIn(child3, Parent)

    def testDict(self):
        class Fortnum1(Fortnum):
            pass

        class Fortnum2(Fortnum):
            pass

        d = {Fortnum1: Fortnum1, Fortnum2: Fortnum2}

        self.assertEqual(d[Fortnum1], Fortnum1)
        self.assertNotEqual(d[Fortnum2], Fortnum1)
        self.assertNotIn("Fortnum1", d)

    def testParent(self):
        class Child1(Fortnum):
            pass

        class Parent(Fortnum):
            child1 = Child1
            child2 = Fortnum("Child2")

        class GrandParent(Fortnum):
            parent = Parent

        self.assertEqual(Child1.parent, Parent)
        self.assertEqual(Parent.child2.parent, Parent)
        self.assertEqual(Child1.parent.parent, GrandParent)


    # Fortnums can only have one parent and are thus not inherited when the class is extended
    # TODO: review. It is an odd behaviour that the members tag along but are neither "in" nor appears in itteration
    # Allow members to propagate down and ignore the mixed messages about only one parent?
    def testExtendFortnum(self):
        Child1 = Fortnum("child1")
        Child2 = Fortnum("child2")

        class Base(Fortnum):
            key = "test"
            child1 = Child1

        class Extended(Base):
            child2 = Child2

        self.assertIn(Child2, Extended)
        self.assertNotIn(Child1, Extended)
        self.assertNotIn(Child2, Base)
        self.assertEqual(Base.key, Extended.key)

    def testList(self):
        class Parent(Fortnum):
            child1 = Fortnum("Child1")
            child2 = Fortnum("Child2")

        children1 = list(Parent)
        children2 = [Parent.child1, Parent.child2]
        self.assertEqual(len(children1), len(children2))
        for first, second in zip(children1, children2):
            self.assertEqual(first, second)

    def test_adding_variable(self):
        class Extended(Fortnum):
            var1 = None

        Extended1 = Extended("Extended1", var1=2)

        self.assertEqual(Extended1.var1, 2)

    def test_descendants(self):
        class GrandParent(Fortnum):
            class Parent1(Fortnum):
                Child1 = Fortnum("Child1")
                Child2 = Fortnum("Child2")

            class Parent2(Fortnum):
                Child3 = Fortnum("Child3")

        descendants = deque(GrandParent.descendants())

        for descendant in (
                GrandParent.Parent1,
                GrandParent.Parent1.Child1,
                GrandParent.Parent1.Child2,
                GrandParent.Parent2,
                GrandParent.Parent2.Child3
        ):
            self.assertEqual(descendant, descendants.popleft())

    def test_fortnum_property(self):
        class Fortnum1(Fortnum):
            @class_property
            def fun_name(self):
                return self.__name__ + " fun"

        self.assertTrue(type(Fortnum1.fun_name) == str)

    def test_fortnum_relation(self):
        class PhysicalState(Fortnum):
            chemicals = None

        class PhysicalStates(Fortnum):
            item_class = PhysicalState

            liquid = PhysicalState("Liquid")
            gas = PhysicalState("Gas")
            solid = PhysicalState("Solid")

        class Chemical(Fortnum):
            related_name = "chemicals"

        class Chemicals(Fortnum):
            class water(Chemical):
                physical_state = PhysicalStates.liquid
                name = "Vatten"

            class gasoline(Chemical):
                physical_state = PhysicalStates.liquid
                name = "Bensin"

            class air(Chemical):
                physical_state = PhysicalStates.gas
                name = "Luft"

        self.assertTrue(hasattr(PhysicalStates.gas, "chemicals"))
        self.assertIn(Chemicals.gasoline, PhysicalStates.liquid.chemicals)
        self.assertIn(Chemicals.water, PhysicalStates.liquid.chemicals)
        self.assertIn(Chemicals.air, PhysicalStates.gas.chemicals)
        self.assertNotIn(Chemicals.water, PhysicalStates.gas.chemicals)

    def test_fortnum_related_list_relation(self):
        class Fruit(Fortnum):
            persons = []
            hated_by = []

        class Fruits(Fortnum):
            banana = Fruit("Banana")
            apple = Fruit("Apple")
            orange = Fruit("Orange")
            kiwi = Fruit("Kiwi")

        class Person(Fortnum):
            related_name = "persons"

        class John(Person):
            favorite_fruits = FortnumRelation(Fruits.banana, Fruits.orange)
            hated_fruits = FortnumRelation(Fruits.kiwi, related_name="hated_by")

        class Jane(Person):
            favorite_fruites = FortnumRelation(Fruits.apple, Fruits.orange)
            hated_fruits = FortnumRelation(Fruits.kiwi, related_name="hated_by")

        self.assertEqual(list(Fruits.orange.persons), [John, Jane])
        self.assertEqual(list(Fruits.apple.persons), [Jane])
        self.assertEqual(list(Fruits.kiwi.persons), [])
        self.assertEqual(list(Fruits.kiwi.hated_by), [John, Jane])

    def test_unable_to_set_relation(self):
        class PhysicalState(Fortnum):
            chemicals = "not a FortnumRelation"

        class PhysicalStates(Fortnum):
            item_class = PhysicalState

            liquid = PhysicalState("Liquid")
            gas = PhysicalState("Gas")
            solid = PhysicalState("Solid")

        class Chemical(Fortnum):
            related_name = "chemicals"

        with self.assertRaises(UnableToAddRelatedFortnum):
            class Chemicals(Fortnum):
                class water(Chemical):
                    physical_state = PhysicalStates.liquid
                    name = "Vatten"

    def test_sorting(self):
        class Parent(Fortnum):
            child1 = Fortnum("Child1")
            child2 = Fortnum("Child2")
            child3 = Fortnum("Child3")

        self.assertEqual(
            [Parent.child1, Parent.child2, Parent.child3],
            list(sorted([Parent.child2, Parent.child3, Parent.child1]))
        )

    def test_larger_then(self):
        class Parent(Fortnum):
            child1 = Fortnum("Child1")
            child2 = Fortnum("Child2")
            child3 = Fortnum("Child3")

        self.assertTrue(Parent.child3 > Parent.child1)
        self.assertFalse(Parent.child2 > Parent.child3)

    def test_smaller_then(self):
        class Parent(Fortnum):
            child1 = Fortnum("Child1")
            child2 = Fortnum("Child2")
            child3 = Fortnum("Child3")

        self.assertTrue(Parent.child1 < Parent.child3)
        self.assertFalse(Parent.child3 < Parent.child2)

    def test_unable_to_sort_without_common_parent(self):
        class Parent(Fortnum):
            child1 = Fortnum("Child1")
            child2 = Fortnum("Child2")
            child3 = Fortnum("Child3")

        with self.assertRaises(TypeError):
            Parent > Parent.child1

    def test_parent_unique_sorting(self):
        class Parent1(Fortnum):
            child1 = Fortnum("Child1")
            child2 = Fortnum("Child2")
            child3 = Fortnum("Child3")

        class Parent2(Fortnum):
            child3 = Parent1.child3
            child2 = Parent1.child2
            child4 = Fortnum("Child4")

        self.assertTrue(Parent1.child1 < Parent1.child3)
        self.assertTrue(Parent2.child2 < Parent2.child3)
        self.assertTrue(Parent2.child4 > Parent1.child2)

        with self.assertRaises(TypeError):
            Parent2.child4 > Parent1.child1

    def test_root(self):
        class GrandParent(Fortnum):
            class Parent1(Fortnum):
                Child1 = Fortnum("Child1")
                Child2 = Fortnum("Child2")

        self.assertEqual(GrandParent.Parent1.Child1.root(), GrandParent)

    def test_root_root(self):
        class Root(Fortnum):
            Child = Fortnum("Child")

        self.assertEqual(Root.root(), Root)

    def test_ancestors(self):
        child = Fortnum("Child")

        class GrandParent(Fortnum):
            class Parent(Fortnum):
                Child = child

        self.assertEqual(list(child.ancestors()), [GrandParent, GrandParent.Parent])

    def test_ancestors_include_self(self):
        child = Fortnum("Child")

        class GrandParent(Fortnum):
            class Parent(Fortnum):
                Child = child

        self.assertEqual(list(child.ancestors(include_self=True)), [GrandParent, GrandParent.Parent, child])

    def test_ancestors_acending(self):
        child = Fortnum("Child")

        class GrandParent(Fortnum):
            class Parent(Fortnum):
                Child = child

        self.assertEqual(list(child.ancestors(ascending=True)), [GrandParent.Parent, GrandParent])

    def test_family(self):
        child1 = Fortnum("Child1")
        child2 = Fortnum("Child2")

        class GrandParent(Fortnum):
            class Parent(Fortnum):
                Child1 = child1
                Child2 = child2

        self.assertEqual(
            list(GrandParent.Parent.family()),
            [
                GrandParent,
                GrandParent.Parent,
                child1,
                child2
            ]
        )

    def test_item_class(self):
        class Chemical(Fortnum):
            pass

        class Water(Chemical):
            pass

        _oil = Chemical("oil")

        class Chemicals(Fortnum):
            item_class = Chemical

            water = Water
            oil = _oil
            not_a_chemical = Fortnum("not_a_chemical")

        self.assertEqual(list(Chemicals), [Chemicals.water, Chemicals.oil])

    def test_not_abstract(self):
        class Foo(Fortnum):
            pass

        self.assertFalse(Foo.abstract)

    def test_abstract(self):
        class AbstractFoo(Fortnum):
            abstract = True

        self.assertTrue(AbstractFoo.abstract)

    def test_do_not_inherit_abstract(self):
        class AbstractParent(Fortnum):
            abstract = True

        class NotAbstractChild(AbstractParent):
            pass

        self.assertFalse(NotAbstractChild.abstract)


class DescriptorTestCase(TestCase):
    def setUp(self):
        FortnumMeta._registry = {}  # Allow redeclaration between tests
        # clear_registries(Fortnum)

        class Fruits(Fortnum):
            Banana = Fortnum("Banana")
            Tomato = Fortnum("Tomato")
        self.Fruits = Fruits

        class Plants(Fortnum):
            Grass = Fortnum("Grass")
            Banana = Fruits.Banana
            Tomato = Fruits.Tomato
        self.Plants = Plants

        class Obj:
            fruit = FortnumDescriptor("fruits", Fruits, default=Fruits.Banana, allow_none=False)
            plant = FortnumDescriptor("plants", Plants, allow_none=False)

        self.o = Obj()

    def test_default(self):
        self.assertEqual(self.o.fruit, self.Fruits.Banana)
        self.o.fruit = self.Fruits.Tomato
        self.assertEqual(self.o.fruit, self.Fruits.Tomato)

    def test_none_not_allowed(self):
        with self.assertRaises(ValueError):
            self.o.plant = None

    def test_illegal_value(self):
        for value in (
            self.Plants.Grass,
            {},
            1,
            False,
            True
        ):
            with self.assertRaises(ValueError):
                self.o.fruit = value



