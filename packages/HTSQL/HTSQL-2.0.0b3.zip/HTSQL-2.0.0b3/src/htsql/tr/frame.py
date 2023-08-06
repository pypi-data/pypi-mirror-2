#
# Copyright (c) 2006-2010, Prometheus Research, LLC
# Authors: Clark C. Evans <cce@clarkevans.com>,
#          Kirill Simonov <xi@resolvent.net>
#


"""
:mod:`htsql.tr.frame`
=====================

This module declares frame and phrase nodes.
"""


from ..util import listof, tupleof, maybe, Clonable, Comparable, Printable
from ..entity import TableEntity, ColumnEntity
from ..domain import Domain, BooleanDomain
from .coerce import coerce
from .code import Expression
from .term import Term, QueryTerm


class Clause(Comparable, Clonable, Printable):
    """
    Represents a SQL clause.

    This is an abstract class; its subclasses are divided into two categories:
    frames (see :class:`Frame`) and phrases (see :class:`Phrase`).

    A clause tree represents a SQL statement and is the next-to-last
    structure of the HTSQL translator.  A clause tree is translated from
    the term tree and the code graph by the *assembling* process.  It is then
    translated to SQL by the *serializing* process.

    The following adapters are associated with the assembling process and
    generate new clause nodes::

        Assemble: (Term, AssemblingState) -> Frame
        Evaluate: (Code, AssemblingState) -> Phrase

    See :class:`htsql.tr.assemble.Assemble` and
    :class:`htsql.tr.assemble.Evaluate` for more detail.

    The following adapter is associated with the serializing process::

        Serialize: (Clause, SerializingState) -> str

    See :class:`htsql.tr.serialize.Serialize` for more detail.

    Clause nodes support equality by value.

    The constructor arguments:

    `expression` (:class:`htsql.tr.code.Expression`)
        The expression node that gave rise to the clause; for debugging
        and error reporting only.

    `equality_vector` (an immutable tuple or ``None``)
        Encapsulates all essential attributes of a node.  Two clauses are
        equal if and only if they are of the same type and their equality
        vectors are equal.  If ``None``, the clause is compared by identity.

        Note that the `expression` attribute is not essential and should
        not be a part of the equality vector.

    Other attributes:

    `binding` (:class:`htsql.tr.binding.Binding`)
        The binding node that gave rise to the expression; for debugging
        purposes only.

    `syntax` (:class:`htsql.tr.syntax.Syntax`)
        The syntax node that gave rise to the expression; for debugging
        purposes only.

    `mark` (:class:`htsql.mark.Mark`)
        The location of the node in the original query; for error reporting.

    `hash` (an integer)
        The node hash; if two nodes are considered equal, their hashes
        must be equal too.
    """

    def __init__(self, expression, equality_vector=None):
        assert isinstance(expression, Expression)
        super(Clause, self).__init__(equality_vector)
        self.expression = expression
        self.binding = expression.binding
        self.syntax = expression.syntax
        self.mark = expression.mark

    def __str__(self):
        return str(self.expression)


class Frame(Clause):
    """
    Represents a SQL frame.

    A *frame* is a node in the query tree, that is, one of these:

    - a top level ``SELECT`` clause, the root of the tree;
    - a nested ``SELECT`` clause, a branch of the tree;
    - a table or a scalar (``DUAL``) clause, a leaf of the tree.

    :class:`Frame` is an abstract case class, see subclasses for concrete
    frame types.

    Each frame node has a unique (in the context of the whole tree) identifier
    called the *tag*.  Tags are used to refer to frame nodes indirectly.

    As opposed to phrases, frame nodes are always compared by identity.

    Class attributes:

    `is_leaf` (Boolean)
        Indicates that the frame is terminal (either a table or a scalar).

    `is_scalar` (Boolean)
        Indicates that the frame is a scalar frame.

    `is_table` (Boolean)
        Indicates that the frame is a table frame.

    `is_branch` (Boolean)
        Indicates that the frame is non-terminal (either nested or a segment).

    `is_nested` (Boolean)
        Indicates that the frame is a nested branch frame.

    `is_segment` (Boolean)
        Indicates that the frame is the segment frame.

    Constructor arguments:

    `kids` (a list of :class:`Frame`)
        A list of child frames.

    `term` (:class:`htsql.tr.term.Term`)
        The term node that gave rise to the frame.

    Other attributes:

    `tag` (an integer)
        A unique identifier of the frame; inherited from the term.

    `space` (:class:`htsql.tr.code.Space`)
        The space represented by the frame; inherited from the term.

    `baseline` (:class:`htsql.tr.code.Space`)
        The baseline space of the frame; inherited from the term.
    """

    is_leaf = False
    is_scalar = False
    is_table = False
    is_branch = False
    is_nested = False
    is_segment = False

    def __init__(self, kids, term):
        # Sanity check on the arguments.
        assert isinstance(kids, listof(Frame))
        assert isinstance(term, Term)
        super(Frame, self).__init__(term.expression)
        self.kids = kids
        self.term = term
        # Extract semantically important attributes of the term.
        self.tag = term.tag
        self.space = term.space
        self.baseline = term.baseline

    def __str__(self):
        return str(self.term)


class LeafFrame(Frame):
    """
    Represents a leaf frame.

    This is an abstract class; for concrete subclasses, see
    :class:`ScalarFrame` and :class:`TableFrame`.
    """

    is_leaf = True

    def __init__(self, term):
        super(LeafFrame, self).__init__([], term)


class ScalarFrame(LeafFrame):
    """
    Represents a scalar frame.

    In SQL, a scalar frame is embodied by a special one-row ``DUAL`` table.
    """

    is_scalar = True


class TableFrame(LeafFrame):
    """
    Represents a table frame.

    In SQL, table frames are serialized as tables in the ``FROM`` list.

    `table` (:class:`htsql.entity.TableEntity`)
        The table represented by the frame.
    """

    is_table = True

    def __init__(self, table, term):
        assert isinstance(table, TableEntity)
        super(TableFrame, self).__init__(term)
        self.table = table


class BranchFrame(Frame):
    """
    Represents a branch frame.

    This is an abstract class; for concrete subclasses, see
    :class:`NestedFrame` and :class:`SegmentFrame`.

    In SQL, a branch frame is serialized as a top level (segment)
    or a nested ``SELECT`` statement.

    `include` (a list of :class:`Anchor`)
        Represents the ``FROM`` clause.

    `embed` (a list of :class:`NestedFrame`)
        Correlated subqueries that are used in the frame.

        A correlated subquery is a sub-``SELECT`` statement that appears
        outside the ``FROM`` list.  The `embed` list keeps all correlated
        subqueries that appear in the frame.  To refer to a correlated
        subquery from a phrase, use :class:`EmbeddingPhrase`.

    `select` (a list of :class:`Phrase`)
        Represents the ``SELECT`` clause.

    `where` (:class:`Phrase` or ``None``)
        Represents the ``WHERE`` clause.

    `group` (a list of :class:`Phrase`)
        Represents the ``GROUP BY`` clause.

    `having` (:class:`Phrase` or ``None``)
        Represents the ``HAVING`` clause.

    `order` (a list of pairs `(phrase, direction)`)
        Represents the ``ORDER BY`` clause.

        Here `phrase` is a :class:`Phrase` instance, `direction`
        is either ``+1`` (indicates ascending order) or ``-1``
        (indicates descending order).

    `limit` (a non-negative integer or ``None``)
        Represents the ``LIMIT`` clause.

    `offset` (a non-negative integer or ``None``)
        Represents the ``OFFSET`` clause.
    """

    is_branch = True

    def __init__(self, include, embed, select,
                 where, group, having, order, limit, offset, term):
        # Note that we do not require `include` list to be non-empty,
        # thus an instance of `BranchFrame` could actually be a leaf
        # in the frame tree!
        assert isinstance(include, listof(Anchor))
        # Check that the join condition on the first subframe is no-op.
        if include:
            assert include[0].is_cross
        assert isinstance(embed, listof(NestedFrame))
        assert isinstance(select, listof(Phrase)) and len(select) > 0
        assert isinstance(where, maybe(Phrase))
        assert isinstance(group, listof(Phrase))
        assert isinstance(having, maybe(Phrase))
        assert isinstance(order, listof(tupleof(Phrase, int)))
        assert isinstance(limit, maybe(int))
        assert isinstance(offset, maybe(int))
        assert limit is None or limit >= 0
        assert offset is None or offset >= 0
        kids = [anchor.frame for anchor in include] + embed
        super(BranchFrame, self).__init__(kids, term)
        self.include = include
        self.embed = embed
        self.select = select
        self.where = where
        self.group = group
        self.having = having
        self.order = order
        self.limit = limit
        self.offset = offset


class NestedFrame(BranchFrame):
    """
    Represents a nested ``SELECT`` statement.
    """

    is_nested = True


class SegmentFrame(BranchFrame):
    """
    Represents a top-level ``SELECT`` statement.
    """

    is_segment = True


class Anchor(Clause):
    """
    Represents a ``JOIN`` clause.

    `frame` (:class:`Frame`)
        The joined frame.

    `condition` (:class:`Phrase` or ``None``)
        The join condition.

    `is_left` (Boolean)
        Indicates that the join is ``LEFT OUTER``.

    `is_right` (Boolean)
        Indicates that the join is ``RIGHT OUTER``.

    Other attributes:

    `is_inner` (Boolean)
        Indicates that the join is ``INNER`` (that is, not left or right).

    `is_cross` (Boolean)
        Indicates that the join is ``CROSS`` (that is, inner without
        any join condition).
    """

    def __init__(self, frame, condition, is_left, is_right):
        assert isinstance(frame, Frame) and not frame.is_segment
        assert isinstance(condition, maybe(Phrase))
        assert condition is None or isinstance(condition.domain, BooleanDomain)
        assert isinstance(is_left, bool) and isinstance(is_right, bool)
        super(Anchor, self).__init__(frame.expression)
        self.frame = frame
        self.condition = condition
        self.is_left = is_left
        self.is_right = is_right
        self.is_inner = (not is_left and not is_right)
        self.is_cross = (self.is_inner and condition is None)


class QueryFrame(Clause):
    """
    Represents the whole HTSQL query.

    `segment` (:class:`SegmentFrame` or ``None``)
        The query segment.
    """

    def __init__(self, segment, term):
        assert isinstance(segment, maybe(SegmentFrame))
        assert isinstance(term, QueryTerm)
        super(QueryFrame, self).__init__(term.expression)
        self.segment = segment
        self.term = term


class Phrase(Clause):
    """
    Represents a SQL expression.

    `domain` (:class:`htsql.domain.Domain`)
        The co-domain of the expression.

    `is_nullable` (Boolean)
        Indicates if the expression may evaluate to ``NULL``.
    """

    def __init__(self, domain, is_nullable, expression, equality_vector):
        assert isinstance(domain, Domain)
        assert isinstance(is_nullable, bool)
        super(Phrase, self).__init__(expression, equality_vector)
        self.domain = domain
        self.is_nullable = is_nullable


class LiteralPhrase(Phrase):
    """
    Represents a literal value.

    `value` (valid type depends on the domain)
        The value.

    `domain` (:class:`htsql.domain.Domain`)
        The value type.
    """

    def __init__(self, value, domain, expression):
        # Note: `NULL` values are represented as `None`.
        is_nullable = (value is None)
        equality_vector = (value, domain)
        super(LiteralPhrase, self).__init__(domain, is_nullable, expression,
                                            equality_vector)
        self.value = value


class NullPhrase(LiteralPhrase):
    """
    Represents a ``NULL`` value.

    ``NULL`` values are commonly generated and checked for, so for
    convenience, they are extracted in a separate class.  Note that
    it is also valid for a ``NULL`` value to be represented as a regular
    :class:`LiteralPhrase` instance.
    """

    def __init__(self, domain, expression):
        super(NullPhrase, self).__init__(None, domain, expression)


class TruePhrase(LiteralPhrase):
    """
    Represents a ``TRUE`` value.

    ``TRUE`` values are commonly generated and checked for, so for
    convenience, they are extracted in a separate class.  Note that
    it is also valid for a ``TRUE`` value to be represented as a regular
    :class:`LiteralPhrase` instance.
    """

    def __init__(self, expression):
        domain = coerce(BooleanDomain())
        super(TruePhrase, self).__init__(True, domain, expression)


class FalsePhrase(LiteralPhrase):
    """
    Represents a ``FALSE`` value.

    ``FALSE`` values are commonly generated and checked for, so for
    convenience, they are extracted in a separate class.  Note that
    it is also valid for a ``FALSE`` value to be represented as a regular
    :class:`LiteralPhrase` instance.
    """

    def __init__(self, expression):
        domain = coerce(BooleanDomain())
        super(FalsePhrase, self).__init__(False, domain, expression)


class EqualityPhraseBase(Phrase):
    """
    Represents an equality operator.

    This is an abstract class for ``=``, ``!=``, ``==``, ``!==`` operators.

    Class attributes:

    `is_regular` (Boolean)
        Indicates that the operator is regular: if any of the arguments is
        ``NULL``, the value is also ``NULL``.

    `is_total` (Boolean)
        Indicates that the operator is total: no exception for ``NULL`` values.

    `is_positive` (Boolean)
        Indicates that the phrase represents an equality operator.

    `is_negative` (Boolean)
        Indicates that the phrase represents an inequality operator.

    Constructor arguments:

    `lop` (:class:`Phrase`)
        The left operand.

    `rop` (:class:`Phrase`)
        The right operand.
    """

    is_regular = False
    is_total = False
    is_positive = False
    is_negative = False

    def __init__(self, lop, rop, expression):
        assert isinstance(lop, Phrase)
        assert isinstance(rop, Phrase)
        domain = coerce(BooleanDomain())
        is_nullable = self.is_regular and (lop.is_nullable or rop.is_nullable)
        equality_vector = (lop, rop)
        super(EqualityPhraseBase, self).__init__(domain, is_nullable,
                                                 expression, equality_vector)
        self.lop = lop
        self.rop = rop


class EqualityPhrase(EqualityPhraseBase):
    """
    Represents the "equality" (``=``) operator.

    The regular "equality" operator treats ``NULL`` as a special value:
    if any of the arguments is ``NULL``, the result is also ``NULL``.
    """

    is_regular = True
    is_positive = True


class InequalityPhrase(EqualityPhraseBase):
    """
    Represents the "inequality" (``!=``) operator.

    The regular "inequality" operator treats ``NULL`` as a special value:
    if any of the arguments is ``NULL``, the result is also ``NULL``.
    """

    is_regular = True
    is_negative = True


class TotalEqualityPhrase(EqualityPhraseBase):
    """
    Represents the "total equality" (``==``) operator.

    The "total equality" operator treats ``NULL`` as a regular value.
    """

    is_total = True
    is_positive = True


class TotalInequalityPhrase(EqualityPhraseBase):
    """
    Represents the "total inequality" (``!==``) operator.

    The "total inequality" operator treats ``NULL`` as a regular value.
    """

    is_total = True
    is_negative = True


class ConnectivePhraseBase(Phrase):
    """
    Represents an N-ary logical connective.

    This is an abstract class for ``AND`` and ``OR`` operators.

    `ops` (a list of :class:`Phrase`)
        The operands.

    Class attributes:

    `is_contjunction` (Boolean)
        Indicates that the phrase represents the ``AND`` operator.

    `is_disjunction` (Boolean)
        Indicates that the phrase represents the ``OR`` operator.
    """

    is_conjunction = False
    is_disjunction = False

    def __init__(self, ops, expression):
        assert isinstance(ops, listof(Phrase))
        assert all(isinstance(op.domain, BooleanDomain) for op in ops)
        domain = coerce(BooleanDomain())
        is_nullable = any(op.is_nullable for op in ops)
        equality_vector = tuple(ops)
        super(ConnectivePhraseBase, self).__init__(domain, is_nullable,
                                                   expression, equality_vector)
        self.ops = ops


class ConjunctionPhrase(ConnectivePhraseBase):
    """
    Represents the logical ``AND`` operator.
    """

    is_conjunction = True


class DisjunctionPhrase(ConnectivePhraseBase):
    """
    Represents the logical ``OR`` operator.
    """

    is_disjunction = True


class NegationPhrase(Phrase):
    """
    Represents the logical ``NOT`` operator.

    `op` (:class:`Phrase`)
        The operand.
    """

    def __init__(self, op, expression):
        assert isinstance(op, Phrase)
        assert isinstance(op.domain, BooleanDomain)
        domain = coerce(BooleanDomain())
        is_nullable = op.is_nullable
        equality_vector = (op,)
        super(NegationPhrase, self).__init__(domain, is_nullable, expression,
                                             equality_vector)
        self.op = op


class IsNullPhraseBase(Phrase):
    """
    Represents the ``IS NULL`` and ``IS NOT NULL`` operators.

    `op` (:class:`Phrase`)
        The operand.

    Class attributes:

    `is_positive` (Boolean)
        Indicates that the phrase represents the ``IS NULL`` operator.

    `is_negative` (Boolean)
        Indicates that the phrase represents the ``IS NOT NULL`` operator.
    """

    is_positive = False
    is_negative = False

    def __init__(self, op, expression):
        assert isinstance(op, Phrase)
        domain = coerce(BooleanDomain())
        is_nullable = False
        equality_vector = (op,)
        super(IsNullPhraseBase, self).__init__(domain, is_nullable, expression,
                                               equality_vector)
        self.op = op


class IsNullPhrase(IsNullPhraseBase):
    """
    Represents the ``IS NULL`` operator.

    The ``IS NULL`` operator produces ``TRUE`` when its operand is ``NULL``,
    ``FALSE`` otherwise.
    """

    is_positive = True


class IsNotNullPhrase(IsNullPhraseBase):
    """
    Represents the ``IS NOT NULL`` operator.

    The ``IS NOT NULL`` operator produces ``FALSE`` when its operand is
    ``NULL``, ``TRUE`` otherwise.
    """

    is_negative = True


class IfNullPhrase(Phrase):
    """
    Represents the ``IFNULL`` operator.

    The ``IFNULL`` operator takes two operands, returns the first one
    if it is not equal to ``NULL``, otherwise returns the second operand.

    `lop` (:class:`Phrase`)
        The first operand.

    `rop` (:class:`Phrase`)
        The second operand.
    """

    def __init__(self, lop, rop, domain, expression):
        assert isinstance(lop, Phrase)
        assert isinstance(rop, Phrase)
        assert isinstance(domain, Domain)
        # Note: the result could be `NULL` only if both arguments are nullable
        # (as opposed to most regular functions).
        is_nullable = (lop.is_nullable and rop.is_nullable)
        equality_vector = (lop, rop)
        super(IfNullPhrase, self).__init__(domain, is_nullable, expression,
                                           equality_vector)
        self.lop = lop
        self.rop = rop


class NullIfPhrase(Phrase):
    """
    Represents the ``NULLIF`` operator.

    The ``NULLIF`` operator takes two operands, returns the first one
    if it is not equal to the second operand, otherwise returns ``NULL``.

    `lop` (:class:`Phrase`)
        The first operand.

    `rop` (:class:`Phrase`)
        The second operand.
    """

    def __init__(self, lop, rop, domain, expression):
        assert isinstance(lop, Phrase)
        assert isinstance(rop, Phrase)
        assert isinstance(domain, Domain)
        # Note: the result could be `NULL` even when both arguments are not
        # nullable.
        is_nullable = True
        equality_vector = (lop, rop)
        super(NullIfPhrase, self).__init__(domain, is_nullable, expression,
                                           equality_vector)
        self.lop = lop
        self.rop = rop


class CastPhrase(Phrase):
    """
    Represents the ``CAST`` operator.

    `base` (:class:`Phrase`)
        The expression to convert.

    `domain` (:class:`htsql.domain.Domain`)
        The target domain.
    """

    def __init__(self, base, domain, is_nullable, expression):
        assert isinstance(base, Phrase)
        equality_vector = (base, domain, is_nullable)
        super(CastPhrase, self).__init__(domain, is_nullable, expression,
                                         equality_vector)
        self.base = base


class FunctionPhrase(Phrase):
    """
    Represents a function or an operator expression.

    This is an abstract class; see subclasses for concrete functions and
    operators.

    `domain` (:class:`htsql.domain.Domain`)
        The function co-domain.

    `arguments` (a dictionary)
        A mapping from argument names to argument values.  Among values,
        we expect :class:`Phrase` objects or lists of :class:`Phrase` objects.
    """

    def __init__(self, domain, is_nullable, expression, **arguments):
        # Extract the equality vector from the arguments (FIXME: messy).
        equality_vector = [domain]
        for key in sorted(arguments):
            value = arguments[key]
            # Argument values are expected to be `Phrase` objects,
            # lists of `Phrase` objects or some other (immutable) objects.
            if isinstance(value, list):
                value = tuple(value)
            equality_vector.append((key, value))
        equality_vector = tuple(equality_vector)
        super(FunctionPhrase, self).__init__(domain, is_nullable, expression,
                                             equality_vector)
        self.arguments = arguments
        # For convenience, we permit access to function arguments using
        # object attributes.
        for key in arguments:
            setattr(self, key, arguments[key])


class ExportPhrase(Phrase):
    """
    Represents a value exported from another frame.

    This is an abstract class; for concrete subclasses, see
    :class:`ColumnPhrase`, :class:`ReferencePhrase`, and
    :class:`EmbeddingPhrase`.

    `tag` (an integer)
        The tag of the frame that exports the value.
    """

    def __init__(self, tag, domain, is_nullable, expression, equality_vector):
        assert isinstance(tag, int)
        super(ExportPhrase, self).__init__(domain, is_nullable, expression,
                                           equality_vector)
        self.tag = tag


class ColumnPhrase(ExportPhrase):
    """
    Represents a column exported from a table frame.

    `tag` (an integer)
        The tag of the table frame.

        The tag must point to an immediate child of the current frame.

    `class` (:class:`htsql.entity.ColumnEntity`)
        The column to export.
    """

    def __init__(self, tag, column, is_nullable, expression):
        assert isinstance(column, ColumnEntity)
        domain = column.domain
        equality_vector = (tag, column)
        super(ColumnPhrase, self).__init__(tag, domain, is_nullable,
                                           expression, equality_vector)
        self.column = column


class ReferencePhrase(ExportPhrase):
    """
    Represents a value exported from a nested sub-``SELECT`` frame.

    `tag` (an integer)
        The tag of the nested frame.

        The tag must point to an immediate child of the current frame.

    `index` (an integer)
        The position of the exported value in the ``SELECT`` clause.
    """

    def __init__(self, tag, index, domain, is_nullable, expression):
        assert isinstance(index, int) and index >= 0
        equality_vector = (tag, index)
        super(ReferencePhrase, self).__init__(tag, domain, is_nullable,
                                              expression, equality_vector)
        self.index = index


class EmbeddingPhrase(ExportPhrase):
    """
    Represents an embedding of a correlated subquery.

    `tag` (an integer)
        The tag of the nested frame.

        The tag must point to one of the subframes contained in the
        `embed` list of the current frame.
    """

    def __init__(self, tag, domain, is_nullable, expression):
        equality_vector = (tag,)
        super(EmbeddingPhrase, self).__init__(tag, domain, is_nullable,
                                              expression, equality_vector)


