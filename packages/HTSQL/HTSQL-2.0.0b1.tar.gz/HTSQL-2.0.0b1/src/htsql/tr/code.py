#
# Copyright (c) 2006-2010, Prometheus Research, LLC
# Authors: Clark C. Evans <cce@clarkevans.com>,
#          Kirill Simonov <xi@resolvent.net>
#


"""
:mod:`htsql.tr.code`
====================

This module declares space and code nodes.
"""


from ..util import maybe, oneof, listof, tupleof, Node
from ..mark import Mark
from ..entity import TableEntity, ColumnEntity, Join
from ..domain import Domain, BooleanDomain
from .binding import Binding, QueryBinding, SegmentBinding
from .coerce import coerce


class Expression(Node):
    """
    Represents an expression node.

    This is an abstract class; its subclasses are divided into two categories:
    space nodes (see :class:`Space`) and code nodes (see :class:`Code`).
    There are also several expression node types that do not belong to either
    of these categories.

    An expression tree (a DAG) is an intermediate stage of the HTSQL
    translator.  An expression tree is translated from a binding tree by
    the *encoding* process.  It is then translated to a clause structure
    by the *compiling* process.

    The following adapters are associated with the encoding process and
    generate new code and space nodes::

        Encode: (Binding, EncodeState) -> Code
        Relate: (Binding, EncodeState) -> Space

    See :class:`htsql.tr.encode.Encode` and :class:`htsql.tr.encode.Relate`
    for more detail.

    The compiling process works as follows.  Space nodes (and selected code
    nodes) are translated to frame nodes via several intermediate steps::

        Assemble: (Space, AssembleState) -> Term
        Outline: (Term, OutlineState) -> Sketch
        Compile: (Sketch, CompileState) -> Frame

    Code nodes are directly translated to phrase nodes::

        Evaluate: (Code, CompileState) -> Phrase

    See :class:`htsql.tr.assemble.Assemble`, :class:`htsql.tr.outline.Outline`,
    :class:`htsql.tr.compile.Compile`, :class:`htsql.tr.compile.Evaluate`
    for more detail.

    Expression nodes support equality by value (as opposed to to equality
    by identity, which is the default for class instances).  That is, two
    expression nodes are equal if they are of the same type and all their
    (essential) attributes are equal.  Some attributes may be considered
    not essential and do not participate in comparison.  To facilitate
    expression comparison, :class:`htsql.domain.Domain` objects also support
    equality by value.  Expression nodes could also be used as dictionary
    keys.

    The constructor arguments:

    `binding` (:class:`htsql.tr.binding.Binding`)
        The binding node that gave rise to the expression; should be used
        only for presentation or error reporting.

    `equality_vector` (an immutable tuple or ``None``)
        Encapsulates all essential attributes of a node.  Two expression
        nodes are considered equal if they are of the same type and their
        equality vectors are equal.  If ``None``, the node is compared by
        identity.

        Note that the `binding` attribute is not essential and should not
        be a part of the equality vector.

    Other attributes:

    `syntax` (:class:`htsql.tr.syntax.Syntax`)
        The syntax node that gave rise to the expression; for debugging
        purposes only.

    `mark` (:class:`htsql.mark.Mark`)
        The location of the node in the original query; for error reporting.

    `hash` (an integer)
        The node hash; if two nodes are considered equal, their hashes
        must be equal too.
    """

    def __init__(self, binding, equality_vector=None):
        assert isinstance(binding, Binding)
        assert isinstance(equality_vector, maybe(oneof(tuple, int, long)))
        # When `equality_vector` is not set, equality by identity
        # is assumed.  Node that `A is B` <=> `id(A) == id(B)`.
        if equality_vector is None:
            equality_vector = id(self)
        self.binding = binding
        self.syntax = binding.syntax
        self.mark = binding.syntax.mark
        self.equality_vector = equality_vector
        self.hash = hash(equality_vector)

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        # Two nodes are equal if they are of the same type and
        # their equality vectors are equal.  We compare hashes
        # before comparing equality vectors to make it work
        # faster (hopefully) in the more common "not equal"
        # case.
        return (isinstance(other, Expression) and
                self.__class__ is other.__class__ and
                self.hash == other.hash and
                self.equality_vector == other.equality_vector)

    def __str__(self):
        # Display the syntex node that gave rise to the expression.
        return str(self.syntax)


class QueryExpression(Expression):
    """
    Represents a whole HTSQL query.

    `segment` (:class:`SegmentExpression` or ``None``)
        The query segment.
    """

    def __init__(self, segment, binding):
        assert isinstance(segment, maybe(SegmentExpression))
        assert isinstance(binding, QueryBinding)
        super(QueryExpression, self).__init__(binding)
        self.segment = segment


class SegmentExpression(Expression):
    """
    Represents a segment of an HTSQL query.

    `space` (:class:`Space`)
        The space rendered by the segment.

    `elements` (a list of :class:`Code` objects)
        The elements rendered by the segment.
    """

    def __init__(self, space, elements, binding):
        assert isinstance(space, Space)
        assert isinstance(elements, listof(Code))
        assert isinstance(binding, SegmentBinding)
        super(SegmentExpression, self).__init__(binding)
        self.space = space
        self.elements = elements


class Space(Expression):
    """
    Represents a space node.

    A space is an expression that represents an (ordered) set of rows.
    Among others, we consider the following kinds of spaces:

    *The scalar space* `I`
        A space with only one row.

    *A table space* `T`
        Given a table `T`, the space consists of all rows of the table.

    *A cross product space* `A * T`
        Given a table `T` and another space `A`, the cross product space
        consists of pairs `(a, t)` where `a` runs over rows of `A` and
        `t` runs over rows of `T`.

        Note that a table space is a special case of a cross product space:
        `T` is equivalent to `I * T`.

        Table `T` in `A * T` is called *the prominent table* of the space.

    *A join product space* `A . T` or `A .j T`
        Given a space `A` with the prominent table `S`, another table `T`
        and a join condition `j` between tables `S` and `T`, the join
        product space consists of pairs `(a, t)` from `A * T` satisfying
        the join condition `j`.

        Table `T` is called the prominent table of `A . T`.

    *A filtered space* `A ? p`
        Given a space `A` and a predicate `p` defined on `A`, the
        filtered space consists of rows of `A` satisfying condition `p`.

    *An ordered space* `A [e,...]`
        Given a space `A` and a list of expressions `e,...`, the
        ordered space consists of rows of `A` reordered by the values
        of expressions.

    Note that all these examples (except for the scalar space) share the same
    form: they take an existing space, called *the base space* and apply some
    operation to produce a new space.  Thus *any space could be expressed
    as an application of a series of elementary operations to the scalar
    space*.

    Each subclass of :class:`Space` represents an operation that is applied
    to a base space.  We could classify the operations (and therefore
    :class:`Space` subclasses) into two groups: those which keep the row
    shape of the base space and those which expand it.  The latter are
    called *axis spaces*.  We also consider the scalar space an axis space.

    Take an arbitrary space `A` and consider it as a sequence of
    operations applied to the scalar space.  If we then reapply only
    the axis operations from the sequence, we obtain a new space `A'`,
    which we call *the inflation* of `A`.  Note that `A` is a subset
    of the inflated space `A'`.

    Now we can establish how different spaces are related to each other.
    For that we will introduce a notion of *convergency* between two
    arbitrary spaces.  Informally, convergency describes how two spaces
    `A` and `B` can be naturally attached to each other.  When rows
    in `A` and `B` have the same shape, convergency is reduced to equality,
    that is, a row from `A` converges to an equal row from `B` if the latter
    exists.  When rows in `A` and `B` have different shapes, we need
    to determine their longest common prefix.  Then a row from `A`
    converges to all rows from `B` that share the same prefix values.

    Formally, for each pair of spaces `A` and `B`, we define a relation
    `<->` ("converges to") on rows from `A` and `B`, that is, a subset
    of the Cartesian product `A x B`, by the following rules:

    (1) For any space `A`, `<->` is the identity relation on `A`,
        that is, each row converges only to itself.

        For two spaces `A` and `B` where `A` is a subset of `B`,
        each row from `A` converges to an equal row from `B`.  In
        particular, this defines `<->` on any space `A` and its inflated
        space `A'`, as well as on any non-axis space `A` and its base
        space `B`.

    (2) Suppose `A` and `B` are spaces such that `A` is an axis space
        and `B` is the base of `A`.  It means that each element of `A`
        has the form `(b, t)` where `b` is some row from `B`. Then
        row `a` from `A` converges to row `b` from `B` if `a` has the
        form `a = (b, t)` for some `t`.

        By transitivity, we could extend `<->` on `A` and any of its
        *prefix spaces*, that is, the base of `A`, the base of the base
        of `A` and so on.  For instance, let `B` be the base space
        of `A` and let `C` be the base space of `B`.  Then `a` from `A`
        converges to `c` from `C` if there exists row `b` from `B`
        such that `a <-> b` and `b <-> c`.

        In particular, this defines `<->` on an arbitrary space `A`
        and the scalar space `I` since `I` is a prefix for any space.
        By the above definition, any row of `A` converges to the (only)
        row of `I`.

    (3) Finally, we are ready to define `<->` on an arbitrary pair
        of spaces `A` and `B`.  First, suppose that `A` and `B`
        share the same inflated space: `A' = B'`.  Then we could
        define `<->` on `A` and `B` transitively via `A'`: `a` from `A`
        converges to `b` from `B` if there exists `a'` from `A'` such
        that `a <-> a'` and `a' <-> b`.

        In the general case, find the longest prefixes `C` of `A`
        and `D` of `B` such that `C` and `D` have the same
        inflated space: `C' = D'`.  Rules `(1)` and `(2)` establish
        `<->` for the pairs `A` and `C`, `C` and `C' = D'`,
        `C' = D'` and `D`, and `D` and `B`.  We define `<->`
        on `A` and `B` transitively: `a` from `A` converges to
        `b` from `B` if there exist rows `c` from `C`,
        `c'` from `C' = D'`, `d` from `D` such that
        `a <-> c <-> c' <-> d <-> b`.

        Note that it is important that we take among the common inflated
        prefixes the longest one.  Any two spaces have a common inflated
        prefix: the scalar space.  If the scalar space is, indeed, the
        longest common inflated prefix of `A` and `B`, then each
        row of `A` converges to every row of `B`.

    Now we are ready to introduce several very important relations between
    spaces:

    `A` *spans* `B`
        A space `A` spans a space `B` if for every row `a` from `A`:

            `card { b` from `B | a <-> b } <= 1`.

        Informally, it means that the statement::

            SELECT * FROM A

        and the statement::

            SELECT * FROM A LEFT OUTER JOIN B ON (A <-> B)

        produce the same number of rows.

    `A` *dominates* `B`
        A space `A` dominates a space `B` if `A` spans `B` and
        for every row `b` from `B`:

            `card { a` from `A | a <-> b } >= 1`.

        Informally, it implies that the statement::

            SELECT * FROM B INNER JOIN A ON (A <-> B)

        and the statement::

            SELECT * FROM B LEFT OUTER JOIN A ON (A <-> B)

        produce the same number of rows.

    `A` *conforms* `B`
        A space `A` conforms a space `B` if `A` dominates `B`
        and `B` dominates `A`.  Alternatively, we could say
        `A` conforms `B` if the `<->` relation establishes
        a bijection between `A` and `B`.

        Informally, it means that the statement::

            SELECT * FROM A

        and the statement::

            SELECT * FROM B

        produce the same number of rows.

        Note that `A` conforming `B` is not the same as `A` being equal
        to `B`; even if `A` conforms `B`,  rows of `A` and `B` may
        have different shapes, therefore as sets, they are different.

    Now take an arbitrary space `A` and its base space `B`.  We say:

    `A` *contracts* `B`
        A space `A` contracts its base `B` if for any row from `B`
        there is no more than one converging row from `A`.

        Typically, it is non-axis spaces that contract their bases,
        although in some cases, an axis space could do it too.

    `A` *expands* `B`
        A space `A` expands its base `B` if for any row from `B`
        there is at least one converging row from `A`.

        Note that it is possible that a space `A` both contracts and
        expands its base `B`, and also that `A` neither contracts
        nor expands `B`.  The former means that `A` conforms `B`.
        The latter holds, in particular, for the cross product space
        `A * T`.  `A * T` violates the contraction condition when
        `T` contains more than one row and violates the expansion
        condition when `T` has no rows.

    A few words about how rows of a space are ordered.  The default
    (also called *weak*) ordering rules are:

    - a table space `T = I * T` is sorted by the lexicographic order
      of the table primary key;

    - a non-axis space keeps the order of its base;

    - an axis space `A * T` or `A . T` respects the order its base `A`;
      rows with the same base element are sorted by the table order.

    An alternative sort order could be specified explicitly (also called
    *strong* ordering).  Whenever strong ordering is  specified, it
    overrides the weak ordering.  Thus, rows of an ordered space `A [e]`
    are sorted first by expression `e`, and then rows which are not
    differentiated by `e` are sorted using the weak ordering of `A`.
    However, if `A` already has a strong ordering, it must be respected.
    Therefore, the general rule for sorting `A [e]` is:

    - first, sort the space by the strong ordering of `A`;

    - then, by `e`;

    - finally, by the weak ordering of `A`.

    Class attributes:

    `is_axis` (Boolean)
        Indicates whether the space is an axis space, that is, the shape
        of the space rows differs from the shape of its base.

    The constructor arguments:

    `base` (:class:`Space` or ``None``)
        The base space; ``None`` for the scalar space.

    `table` (:class:`htsql.entity.TableEntity` or ``None``)
        The prominent table of the space; ``None`` if the space has no
        prominent table.

    `is_contracting` (Boolean)
        Indicates if the space contracts its base space.

    `is_expanding` (Boolean)
        Indicates if the space expands its base space.

    Other attributes:

    `is_inflated` (Boolean)
        Indicates if the space is an inflation, that is, the space itself
        and all its prefixes are axis spaces.
    """

    is_axis = False

    def __init__(self, base, table, is_contracting, is_expanding,
                 binding, equality_vector=None):
        assert isinstance(base, maybe(Space))
        assert isinstance(table, maybe(TableEntity))
        assert isinstance(is_contracting, bool)
        assert isinstance(is_expanding, bool)
        super(Space, self).__init__(binding, equality_vector)
        self.base = base
        self.table = table
        self.is_contracting = is_contracting
        self.is_expanding = is_expanding
        # Indicates that the space itself and all its prefixes are axes.
        self.is_inflated = (base is None or
                            (base.is_inflated and self.is_axis))

    def ordering(self, with_strong=True, with_weak=True):
        """
        Provides ordering of the space.

        The function returns a list of pairs `(code, direction)`, where
        `code` is a :class:`Code` instance and `direction` is a number ``+1``
        or ``-1``.  The `code` objects specify expressions by which the
        rows are sorted, `direction` indicates the respective order (``+1``
        for ascending, ``-1`` for descending).

        `with_strong` (Boolean)
            If set, include strong (explicit) ordering.

        `with_weak` (Boolean)
            If set, include weak (implicit) ordering.
        """
        # Sanity check on the arguments.
        assert isinstance(with_strong, bool)
        assert isinstance(with_weak, bool)
        # The default implementation inherits ordering from the base space.
        return self.base.ordering(with_strong, with_weak)

    def unfold(self):
        """
        Produces a list of prefix spaces.

        The method returns a list composed of the space itself,
        its base, the base of its base and so on.
        """
        prefixes = []
        prefix = self
        while prefix is not None:
            prefixes.append(prefix)
            # Note: `prefix.base` is None for the scalar space.
            prefix = prefix.base
        return prefixes

    def resembles(self, other):
        """
        Verifies if the spaces represent the same operation.

        Typically, it means that `self` and `other` have the same type
        and equal attributes, but may have different bases.
        """
        # We rely upon an assumption that the equality vector of a space node
        # is a tuple of all its essential attributes and the first element
        # of the tuple is the space base.
        return (isinstance(other, self.__class__) and
                self.equality_vector[1:] == other.equality_vector[1:])

    def inflate(self):
        """
        Produces the inflation of the space.

        If we represent a space as a series of operations sequentially
        applied to the scalar space, the inflation of the space is obtained
        by ignoring any non-axis operations and applying axis operations
        only.
        """
        # Shortcut: check if the space is already an inflation.
        if self.is_inflated:
            return self
        # This is going to become a new inflated space.
        space = None
        # Iterate over all prefixes starting from the scalar space.
        for prefix in reversed(self.unfold()):
            # Skip non-axis operations, reapply axis operations to
            # a new base.
            if prefix.is_axis:
                space = prefix.clone(base=space)
        # This is the inflated space now.
        return space

    def prune(self, other):
        """
        Prunes shared non-axis operations.

        Given spaces `A` and `B`, this function produces a new space
        `A'` such that `A` is a subset of `A'` and the convergence
        of `A` and `B` coincides with the convergence of `A'` and `B`.
        This is done by pruning any non-axis operations of `A` that
        also occurs in `B`.
        """
        # Sanity check on the argument.
        assert isinstance(other, Space)
        # Shortcut: we cannot further prune an inflated space.
        if self.is_inflated:
            return self
        # Unfold the spaces into individual operations.
        my_prefixes = self.unfold()
        their_prefixes = other.unfold()
        # This is going to become the pruned space.
        space = None
        # Iterate until the prefixes are exhausted or diverged.
        while my_prefixes and their_prefixes:
            # Get the next operation.
            my_prefix = my_prefixes[-1]
            their_prefix = their_prefixes[-1]
            # Compare the prefixes.
            if my_prefix.resembles(their_prefix):
                # So both prefixes represent the same operation.
                # If it is an axis operation, apply it; otherwise,
                # discard it.
                # FIXME: may break if the space contains a non-matching
                # `limit/offset` operation?
                if my_prefix.is_axis:
                    space = my_prefix.clone(base=space)
                my_prefixes.pop()
                their_prefixes.pop()
            elif not their_prefix.is_axis:
                # The prefixes represent different operations and `B`'s prefix
                # is not an axis.  Discard it, we will try the next prefix.
                # FIXME: we may miss an opportunity to compare `B`'s prefix
                # with other `A`'s prefixes.  It is not a big deal though,
                # we do not need to generate an optimal result here.
                their_prefixes.pop()
            elif not my_prefix.is_axis:
                # The prefixes represent different operations, `B`'s prefix
                # is an axis, and `A`'s prefix is not.  Here we apply the
                # `A`'s prefix.
                space = my_prefix.clone(base=space)
                my_prefixes.pop()
            else:
                # The prefixes are both axes and differ from each other.
                # At this point, The prefixes diverge and are not
                # comparable anymore.  Break from the loop.
                break
        # Reapply the unprocessed prefixes.
        while my_prefixes:
            my_prefix = my_prefixes.pop()
            space = my_prefix.clone(base=space)
        # We have a pruned space here.
        return space

    def spans(self, other):
        """
        Verifies if the space spans another space.
        """
        # Sanity check on the argument.
        assert isinstance(other, Space)
        # Shortcut: any space spans itself.
        if self is other or self == other:
            return True
        # Extract axis prefixes from both spaces.
        my_axes = [prefix for prefix in self.unfold() if prefix.is_axis]
        their_axes = [prefix for prefix in other.unfold() if prefix.is_axis]
        # Iterate until the axes are exhausted or diverged.
        while my_axes and their_axes:
            # Check if the next pair of axes represent the same operation.
            if my_axes[-1].resembles(their_axes[-1]):
                # If so, go compare the next pair of axes.
                my_axes.pop()
                their_axes.pop()
            else:
                # Otherwise, the axes diverge.
                break
        # At this point, all processed pairs of axes converge by identity.
        # If the other space has no more axes left, it is spanned.  Otherwise,
        # it is spanned only if its remaining unprocessed axes represent
        # contracting operations.
        for their_axis in their_axes:
            if not their_axis.is_contracting:
                return False
        return True

    def conforms(self, other):
        """
        Verifies if the space conforms another space.
        """
        # Sanity check on the argument.
        assert isinstance(other, Space)
        # Shortcut: any space conforms itself.
        if self is other or self == other:
            return True
        # Unfold the spaces into individual operations.
        my_prefixes = self.unfold()
        their_prefixes = other.unfold()
        # Iterate until the prefixes are exhausted or diverged.
        while my_prefixes and their_prefixes:
            # Get the next pair of prefixes.
            my_prefix = my_prefixes[-1]
            their_prefix = their_prefixes[-1]
            # Compare the prefixes.
            if my_prefix.resembles(their_prefix):
                # If the prefixes represent the same operation, we could
                # proceed to the next pair of prefixes.
                my_prefixes.pop()
                their_prefixes.pop()
            elif (my_prefix.is_contracting and
                  my_prefix.is_expanding and
                  not my_prefix.is_axis):
                # Ok, the prefixes represent different operations, but
                # one of them is not an axis and does not change the
                # cardinality of its base.  We could skip this prefix
                # and proceed further.
                my_prefixes.pop()
            elif (their_prefix.is_contrating and
                  their_prefix.is_expanding and
                  not their_prefix.is_axis):
                # Same with the other prefix.
                their_prefixes.pop()
            else:
                # The prefixes start to diverge; break from the loop.
                break
        # If all prefixes are processed, the spaces conform each other.
        # Otherwise, they conform each other only if the remaining unprocessed
        # prefixes do not change the cardinality of their bases.
        for prefix in my_prefixes + their_prefixes:
            if not (prefix.is_contracting and prefix.is_expanding):
                return False
        return True

    def dominates(self, other):
        """
        Verifies if the space dominates another space.
        """
        # Sanity check on the argument.
        assert isinstance(other, Space)
        # Shortcut: any space dominates itself.
        if self is other or self == other:
            return True
        # Unfold the spaces into individual operations.
        my_prefixes = self.unfold()
        their_prefixes = other.unfold()
        # Iterate until the prefixes are exhausted or diverged.
        while my_prefixes and their_prefixes:
            # Get the next pair of prefixes.
            my_prefix = my_prefixes[-1]
            their_prefix = their_prefixes[-1]
            # Compare the prefixes.
            if my_prefix.resembles(their_prefix):
                # If the prefixes represent the same operation, we could
                # proceed to the next pair of prefixes.
                my_prefixes.pop()
                their_prefixes.pop()
            elif their_prefix.is_contrating and not their_prefix.is_axis:
                # We got prefixes representing different operations; however
                # the dominated prefix represents a non-axis operation that
                # does not increase the cardinality of its base.  Therefore
                # we could ignore this prefix and proceed further.
                # operation.
                their_prefixes.pop()
            else:
                # The prefixes start to diverge; break from the loop.
                break
        # If all prefixes are processed, the space dominates the other.
        # Otherwise, it is only possible if the remaining prefixes of
        # the space do not decrease the base cardinality while the
        # remaining prefixes of the other space do not increase the
        # base cardinality.
        for my_prefix in my_prefixes:
            if not my_prefix.is_expanding:
                return False
        for their_prefix in their_prefixes:
            if not their_prefix.is_contracting:
                return False
        return True

    def concludes(self, other):
        """
        Verifies if the other space is a prefix of the space.
        """
        # Sanity check on the argument.
        assert isinstance(other, Space)
        # Shortcut: any space is its own prefix.  We compare by identity
        # first because `==` is a costly operation (premature optimization?).
        if self is other or self == other:
            return True
        # Iterate over all prefixes of the space comparing them with
        # the given other space.
        space = self
        while space is not None:
            if space == other:
                return True
            space = space.base
        # None of the prefixes matched, the spaces must be unrelated.
        return False


class ScalarSpace(Space):
    """
    Represents a scalar space.

    A scalar space `I` contains one row ``()``.  Any other space
    is generated by applying a sequence of elementary operations
    to `I`.

    `base` (always ``None``)
        The scalar space (and only the scalar space) has no base.
    """

    # Scalar space is an axis space.
    is_axis = True

    def __init__(self, base, binding):
        # We keep `base` among constructor arguments despite it being
        # always equal to `None` to make
        #   space = space.clone(base=new_base)
        # work even for scalar spaces.
        assert base is None
        # Note that we must satisfy the assumption that the first element
        # of the equality vector is the space base (used by `Space.resembles`).
        super(ScalarSpace, self).__init__(
                    base=None,
                    table=None,
                    is_contracting=False,
                    is_expanding=False,
                    binding=binding,
                    equality_vector=(base,))

    def ordering(self, with_strong=True, with_weak=True):
        # The scalar space does not impose any ordering.
        return []

    def __str__(self):
        # Display a table expression in an algebraic form.
        return "I"


class ProductSpace(Space):
    """
    Represents a product space.

    A product space is a subset of a Cartesian product between the base
    space and a table.  This is an abstract class, see concrete subclasses
    :class:`CrossProductSpace` and :class:`JoinProductSpace`.

    `table` (:class:`htsql.entity.TableEntity`)
        The prominent table of the product.
    """

    # All subclasses of `ProductSpace` are axis spaces.
    is_axis = True

    def ordering(self, with_strong=True, with_weak=True):
        # A product space complements the weak ordering of its base with
        # implicit table ordering.

        # Sanity check on the arguments.
        assert isinstance(with_strong, bool)
        assert isinstance(with_weak, bool)

        # A list of pairs `(code, direction)`.
        order = []

        if with_strong:
            # Product space inherits its strong ordering from the base.
            order += self.base.ordering(with_strong=True, with_weak=False)

        if with_weak:
            # Product space takes the weak ordering from its base.
            order += self.base.ordering(with_strong=False, with_weak=True)
            # And complement it with the table ordering (but only if
            # the cardinality of the space may increase).
            if not self.is_contracting:
                # List of columns which provide the default table ordering.
                columns = []
                # When possible, we take the columns from the primary key
                # of the table.
                if self.table.primary_key is not None:
                    column_names = self.table.primary_key.origin_column_names
                    columns = [self.table.columns[column_name]
                               for column_name in column_names]
                # However when the primary key does not exist, we use columns
                # of the first unique key comprised of non-nullable columns.
                else:
                    for key in self.table.unique_keys:
                        column_names = key.origin_column_names
                        key_columns = [self.table.columns[column_name]
                                       for column_name in column_names]
                        if all(not column.is_nullable
                               for column in key_columns):
                            columns = key_columns
                            break
                # If neither the primary key nor unique keys with non-nullable
                # columns exist, we have one option left: sort by all columns
                # of the table.
                if not columns:
                    columns = list(self.table.columns)
                # Add weak table ordering.
                for column in columns:
                    code = ColumnUnit(column, self, self.binding)
                    order.append((code, +1))

        return order


class CrossProductSpace(ProductSpace):
    """
    Represents a cross product space.

    A cross product space `A * T` consists of all pairs `(a, t)` where
    `a` is a row of the base space `A` and `t` is a row of the table `T`.

    `base` (:class:`Space`)
        The base space.

    `table` (:class:`htsql.entity.TableEntity`)
        The prominent table.
    """

    def __init__(self, base, table, binding):
        super(CrossProductSpace, self).__init__(
                    base=base,
                    table=table,
                    is_contracting=False,
                    is_expanding=False,
                    binding=binding,
                    equality_vector=(base, table))

    def __str__(self):
        # Display:
        #   (<base> * schema.table)
        return "(%s * %s)" % (self.base, self.table)


class JoinProductSpace(ProductSpace):
    """
    Represents a join product space.

    Let `A` be a space with the prominent table `S`, `j` be a join
    condition between tables `S` and `T`.  A join product space `A .j T`
    (or `A . T` when the join condition is implied) of the space `A`
    and the table `T` consists of all pairs `(a, t)`, where `a` is a row
    from `A` of the form `a = (..., s)` and `t` is a row from `T` such
    that `s` and `t` satisfy the join condition `j`.

    `base` (:class:`Space`)
        The base space.

    `join` (:class:`htsql.entity.Join`)
        The join condition.
    """

    def __init__(self, base, join, binding):
        assert isinstance(join, Join)
        # Check that the join origin is the prominent table of the base.
        assert isinstance(base, Space) and base.table is join.origin
        super(JoinProductSpace, self).__init__(
                    base=base,
                    table=join.target,
                    is_contracting=join.is_contracting,
                    is_expanding=join.is_expanding,
                    binding=binding,
                    equality_vector=(base, join))
        self.join = join

    def __str__(self):
        # Display:
        #   (<base> . schema.table)
        return "(%s . %s)" % (self.base, self.table)


class FilteredSpace(Space):
    """
    Represents a filtered space.

    A filtered space `A ? f`, where `A` is the base space and `f` is
    a predicate expression on `A`, consists of rows of `A` satisfying
    the condition `f`.

    `base` (:class:`Space`)
        The base space.

    `filter` (:class:`Code`)
        The predicate expression.
    """

    def __init__(self, base, filter, binding):
        assert isinstance(filter, Code)
        assert isinstance(filter.domain, BooleanDomain)
        super(FilteredSpace, self).__init__(
                    base=base,
                    table=base.table,
                    is_contracting=True,
                    is_expanding=False,
                    binding=binding,
                    equality_vector=(base, filter))
        self.filter = filter

    def __str__(self):
        # Display:
        #   (<base> ? <filter>)
        return "(%s ? %s)" % (self.base, self.filter)


class ConvergedSpace(Space):
    """
    Represents a converged space.

    A converged space `A ^ B`, where `A` and `B` are spaces, consists of
    rows from `A` that have at least one convergent row from `B`.
    """

    def __init__(self, base, filter, binding):
        assert isinstance(filter, Space)
        super(ConvergedSpace, self).__init__(
                    base=base,
                    table=base.table,
                    is_contracting=True,
                    is_expanding=False,
                    binding=binding,
                    equality_vector=(base, filter))
        self.filter = filter

    def __str__(self):
        # Display:
        #   (<base> ^ <filter>)
        return "(%s ^ %s)" % (self.base, self.filter)


class OrderedSpace(Space):
    """
    Represents an ordered space.

    An ordered space `A [e,...;p:q]` is a space with explicitly specified
    strong ordering.  It also may extract a slice of the base space.

    `base` (:class:`Space`)
        The base space.

    `order` (a list of pairs `(code, direction)`)
        Expressions to sort the space by.

        Here `code` is an :class:`Code` instance, `direction` is either
        ``+1`` (indicates ascending order) or ``-1`` (indicates descending
        order).

    `limit` (a non-negative integer or ``None``)
        If set, the space extracts the first `limit` rows from the base
        space (with respect to the space ordering).  The remaining rows
        are discarded.

    `offset` (a non-negative integer or ``None``)
        If set, indicates that when extracting rows from the base space,
        the first `offset` rows should be skipped.
    """

    # FIXME: Non-commutativity of the ordered space may affect `prune`
    # and other functions.  Add class attribute `is_commutative`?

    def __init__(self, base, order, limit, offset, binding):
        assert isinstance(order, listof(tupleof(Code, int)))
        assert isinstance(limit, maybe(int))
        assert isinstance(offset, maybe(int))
        assert limit is None or limit >= 0
        assert offset is None or offset >= 0
        super(OrderedSpace, self).__init__(
                    base=base,
                    table=base.table,
                    is_contracting=True,
                    is_expanding=(limit is None and offset is None),
                    binding=binding,
                    equality_vector=(base, tuple(order)))
        self.order = order
        self.limit = limit
        self.offset = offset

    def ordering(self, with_strong=True, with_weak=True):
        order = []
        if with_strong:
            order += self.base.ordering(with_strong=True, with_weak=False)
            order += self.order
        if with_weak:
            order += self.base.ordering(with_strong=False, with_weak=True)
        return order

    def __str__(self):
        # Display:
        #   <base> [<code>,...;<offset>:<limit>+<offset>]
        indicators = []
        if self.order:
            indicator = ",".join(str(code) for code, dir in self.order)
            indicators.append(indicator)
        if self.limit is not None and self.offset is not None:
            indicator = "%s:%s+%s" % (self.offset, self.offset, self.limit)
            indicators.append(indicator)
        elif self.limit is not None:
            indicator = ":%s" % self.limit
            indicators.append(indicator)
        elif self.offset is not None:
            indicator = "%s:" % self.offset
            indicators.append(indicator)
        indicators = ";".join(indicators)
        return "%s [%s]" % (self.base, indicators)


class Code(Expression):
    """
    Represents a code expression.

    A code expression is a function on spaces.  Specifically, it is a
    functional (possibly of several variables) that maps a space
    (or a Cartesian product of several spaces) to some scalar domain.
    :class:`Code` is an abstract base class for all code expressions;
    see its subclasses for concrete types of expressions.

    Among all code expressions, we distinguish *unit expressions*:
    elementary functions on spaces.  There are two kinds of units:
    columns and aggregate functions (see :class:`Unit` for more detail).
    Every non-unit code could be expressed as a composition of a scalar
    function and one or several units:

        `f = F(u(a),v(b),...)`,

    where
    
    - `f` is a code expression;
    - `F` is a scalar function;
    - `a`, `b`, ... are elements of spaces `A`, `B`, ...;
    - `u`, `v`, ... are unit expressions on `A`, `B`, ....

    `domain` (:class:`htsql.domain.Domain`)
        The co-domain of the code expression.

    `units` (a list of :class:`Unit`)
        The unit expressions of which the code is composed.
    """

    def __init__(self, domain, units, binding, equality_vector=None):
        assert isinstance(domain, Domain)
        assert isinstance(units, listof(Unit))
        super(Code, self).__init__(binding, equality_vector)
        self.domain = domain
        self.units = units


class LiteralCode(Code):
    """
    Represents a literal value.

    `value` (valid type depends on the domain)
        The value.

    `domain` (:class:`htsql.domain.Domain`)
        The value type.
    """

    def __init__(self, value, domain, binding):
        super(LiteralCode, self).__init__(
                    domain=domain,
                    units=[],
                    binding=binding,
                    equality_vector=(value, domain))
        self.value = value

    def __str__(self):
        # The actual value is often more helpful than the expression
        # that generated it.
        return repr(self.value)


class EqualityCodeBase(Code):
    """
    Represents an equality operator.

    This is an abstract class for the ``=`` and ``==`` operators.

    `lop` (:class:`Code`)
        The left operand.

    `rop` (:class:`Code`)
        The right operand.
    """

    def __init__(self, lop, rop, binding):
        assert isinstance(lop, Code)
        assert isinstance(rop, Code)
        super(EqualityCodeBase, self).__init__(
                    # We rely on that an engine-specific Boolean type
                    # always exists.
                    domain=coerce(BooleanDomain()),
                    # Units of a complex expression are usually a composition
                    # of argument units.  Note that duplicates are allowed.
                    units=(lop.units+rop.units),
                    binding=binding,
                    equality_vector=(lop, rop))
        self.lop = lop
        self.rop = rop


class EqualityCode(EqualityCodeBase):
    """
    Represents the "equality" (``=``) operator.

    The regular "equality" operator treats ``NULL`` as a special value:
    if any of the arguments is ``NULL``, the result is also ``NULL``.
    """


class TotalEqualityCode(EqualityCodeBase):
    """
    Represents the "total equality" (``==``) operator.

    The "total equality" operator treats ``NULL`` as a regular value.
    """


class ConnectiveCodeBase(Code):
    """
    Represents an N-ary logical connective.

    This is an abstract class for "AND" (``&``) and "OR" (``|``) operators.

    `ops` (a list of :class:`Code`)
        The operands.
    """

    def __init__(self, ops, binding):
        assert isinstance(ops, listof(Code))
        assert all(isinstance(op.domain, BooleanDomain) for op in ops)
        # Extract all units from the arguments.
        units = []
        for op in ops:
            units.extend(op.units)
        super(ConnectiveCodeBase, self).__init__(
                    # We rely on that an engine-specific Boolean type
                    # always exists.
                    domain=coerce(BooleanDomain()),
                    units=units,
                    binding=binding,
                    equality_vector=tuple(ops))
        self.ops = ops


class ConjunctionCode(ConnectiveCodeBase):
    """
    Represents the logical "AND" (``&``) operator.
    """


class DisjunctionCode(ConnectiveCodeBase):
    """
    Represents the logical "OR" (``|``) operator.
    """


class NegationCode(Code):
    """
    Represents the logical "NOT" (``!``) operator.

    `op` (:class:`Code`)
        The operand.
    """

    def __init__(self, op, binding):
        assert isinstance(op, Code)
        assert isinstance(op.domain, BooleanDomain)
        super(NegationCode, self).__init__(
                    # We rely on that an engine-specific Boolean type
                    # always exists.
                    domain=coerce(BooleanDomain()),
                    units=op.units,
                    binding=binding,
                    equality_vector=(op,))
        self.op = op


class CastCode(Code):
    """
    Represents a type conversion operator.

    `base` (:class:`Code`)
        The expression to convert.

    `domain` (:class:`htsql.domain.Domain`)
        The target domain.
    """

    def __init__(self, base, domain, binding):
        super(CastCode, self).__init__(
                    domain=domain,
                    units=base.units,
                    binding=binding,
                    equality_vector=(base, domain))
        self.base = base


class FunctionCode(Code):
    """
    Represents a function or an operator expression.

    This is an abstract class; see subclasses for concrete function types.

    `domain` (:class:`htsql.domain.Domain`)
        The function co-domain.

    `arguments` (a dictionary)
        A mapping from argument names to argument values.  Among values,
        we expect other :class:`Code` objects or lists of :class:`Code`
        objects.
    """

    def __init__(self, domain, binding, **arguments):
        # Extract the units and the equality vector from the arguments.
        # FIXME: messy, add some formal definition of the argument structure
        # and/or a walker operator?
        units = []
        equality_vector = [domain]
        for key in sorted(arguments):
            value = arguments[key]
            # Argument values are expected to be `Code` objects,
            # list of `Code` objects or some other (immutable) objects.
            if isinstance(value, Code):
                units.extend(value.units)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, Code):
                        units.extend(item.units)
                value = tuple(value)
            equality_vector.append((key, value))
        equality_vector = tuple(equality_vector)

        super(FunctionCode, self).__init__(
                    domain=domain,
                    units=units,
                    binding=binding,
                    equality_vector=equality_vector)
        self.arguments = arguments
        # For convenience, we permit access to function arguments using
        # object attributes.
        for key in arguments:
            setattr(self, key, arguments[key])


class Unit(Code):
    """
    Represents a unit expression.

    A unit is an elementary function on a space.  There are two kinds
    of units: columns and aggregates; see subclasses :class:`ColumnUnit`,
    :class:`AggregateUnit`, and :class:`CorrelatedUnit` for more detail.

    Note that it is easy to *trasfer* a unit code from one space to another.
    Specifically, suppose a unit `u` is defined on a space `A` and `B`
    is another space such that `B` spans `A`.  Then for each row `b`
    from `B` there is no more than one row `a` from `A` such that `a <-> b`.
    Therefore we could define `u` on `B` as follows:

    - `u(b) = u(a)` if there exists `a` from `A` such that `a <-> b`;
    - `u(b) =` ``NULL`` if there is no rows in `A` convergent to `b`.

    When a space `B` spans the space `A` of a unit `u`, we say that
    `u` is *singular* on `B`.  By the previous argument, `u` could be
    transferred to `B`.  Thus any unit is well-defined not only on its
    own space, but also on any space where it is singular.

    `space` (:class:`Space`)
        The space on which the unit is defined.

    `domain` (:class:`htsql.domain.Domain`)
        The unit co-domain.
    """

    def __init__(self, space, domain, binding, equality_vector=None):
        assert isinstance(space, Space)
        super(Unit, self).__init__(
                    domain=domain,
                    units=[self],
                    binding=binding,
                    equality_vector=equality_vector)
        self.space = space

    def singular(self, space):
        """
        Verifies if the unit is singular (well-defined) on the given space.
        """
        return space.spans(self.space)


class ColumnUnit(Unit):
    """
    Represents a column unit.

    A column unit is a function on a space that returns a column of the
    prominent table of the space.

    `column` (:class:`htsql.entity.ColumnEntity`)
        The column produced by the unit.

    `space` (:class:`Space`)
        The unit space.  Note that the prominent table of the space
        must coincide with the table of the column.
    """

    def __init__(self, column, space, binding):
        assert isinstance(column, ColumnEntity)
        assert (space.table is not None and
                (space.table.schema_name, space.table.name)
                    == (column.schema_name, column.table_name))
        super(ColumnUnit, self).__init__(
                    space=space,
                    domain=column.domain,
                    binding=binding,
                    equality_vector=(column, space))
        self.column = column


class AggregateUnitBase(Unit):
    """
    Represents an aggregate unit.

    Aggregate units express functions on sets.  Specifically, let `A` and `B`
    be spaces such that `B` spans `A`, but  `A` does not span `B`, and
    let `g` be a function that takes subsets of `B` as an argument.  Then
    we could define an aggregate unit `u` on `A` as follows:

        `u(a) = g({b | a <-> b})`

    Here, for each row `a` from `A`, we take the subset of convergent
    rows from `B` and apply `g` to it; the result is the value of `u(a)`.

    The space `A` is the unit space, the space `B` is called *the plural
    space* of an aggregate unit, and `g` is called *the composite expression*
    of an aggregate unit.

    `composite` (:class:`Code`)
        The composite expression of the aggregate unit.

    `plural_space` (:class:`Space`)
        The plural space of the aggregate unit, that is, the space
        which subsets form the argument of the composite expression.

    `space` (:class:`Space`)
        The space on which the unit is defined.
    """

    def __init__(self, composite, plural_space, space, binding):
        assert isinstance(composite, Code)
        assert isinstance(plural_space, Space)
        # FIXME: consider lifting the requirement that the plural
        # space spans the unit space.  Is it really necessary?
        assert plural_space.spans(space)
        assert not space.spans(plural_space)
        super(AggregateUnitBase, self).__init__(
                    space=space,
                    domain=composite.domain,
                    binding=binding,
                    equality_vector=(composite, plural_space, space))
        self.composite = composite
        self.plural_space = plural_space
        self.space = space


class AggregateUnit(AggregateUnitBase):
    """
    Represents a regular aggregate unit.

    A regular aggregate unit is expressed in SQL using an aggregate
    expression with ``GROUP BY`` clause.
    """


class CorrelatedUnit(AggregateUnitBase):
    """
    Represents a correlated aggregate unit.

    A correlated aggregate unit is expressed in SQL using a correlated
    subquery.
    """


