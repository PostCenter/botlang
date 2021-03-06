import copy


class ASTNode(object):
    """
    Language expression
    """
    def accept(self, visitor, environment):
        raise NotImplementedError(
            'Must implement accept(visitor, environment)'
        )

    def __init__(self):
        self.s_expr = None

    def add_code_reference(self, code_reference):
        self.s_expr = code_reference
        return self

    def print_node_type(self):
        raise NotImplementedError

    def copy(self):
        """
        Deep-copies this AST
        :return: an ASTNode
        """
        raise NotImplementedError


class Val(ASTNode):
    """
    Value expression
    """
    def __init__(self, value):
        """
        :param value: any 
        """
        super(ASTNode, self).__init__()
        self.value = value

    def accept(self, visitor, env):
        return visitor.visit_val(self, env)

    def print_node_type(self):
        return 'value'

    def copy(self):
        return Val(self.value).add_code_reference(self.s_expr)


class ListVal(ASTNode):
    """
    Literal list expression
    """
    def __init__(self, elements):
        """
        :param elements: List[Val]
        """
        super(ASTNode, self).__init__()
        self.elements = elements

    def accept(self, visitor, env):
        return visitor.visit_list(self, env)

    def print_node_type(self):
        return 'list'

    def copy(self):
        return ListVal([e.copy() for e in self.elements])\
            .add_code_reference(self.s_expr)


class If(ASTNode):
    """
    'If' conditional
    """
    def __init__(self, cond, if_true, if_false):
        """
        :param cond: ASTNode
        :param if_true: ASTNode
        :param if_false: ASTNode
        """
        super(ASTNode, self).__init__()
        self.cond = cond
        self.if_true = if_true
        self.if_false = if_false

    def accept(self, visitor, env):
        return visitor.visit_if(self, env)

    def print_node_type(self):
        return 'if node'

    def copy(self):
        return If(self.cond.copy(), self.if_true.copy(), self.if_false.copy())\
            .add_code_reference(self.s_expr)


class Cond(ASTNode):
    """
    'Cond' conditional
    """
    def __init__(self, cond_clauses):
        """
        :param cond_clauses: List[CondPredicateClause*, CondElseClause]
        """
        super(ASTNode, self).__init__()
        self.cond_clauses = cond_clauses

    def accept(self, visitor, environment):
        return visitor.visit_cond(self, environment)

    def print_node_type(self):
        return 'cond node'

    def copy(self):
        return Cond([clause.copy() for clause in self.cond_clauses])\
            .add_code_reference(self.s_expr)


class CondPredicateClause(ASTNode):
    """
    'Cond' predicate clause
    """
    def __init__(self, predicate, then_body):
        """
        :param predicate: ASTNode
        :param then_body: ASTNode
        """
        super(ASTNode, self).__init__()
        self.predicate = predicate
        self.then_body = then_body

    def accept(self, visitor, environment):
        return visitor.visit_cond_predicate_clause(self, environment)

    def print_node_type(self):
        return 'cond clause'

    def copy(self):
        return CondPredicateClause(
            self.predicate.copy(),
            self.then_body.copy()
        ).add_code_reference(self.s_expr)


class CondElseClause(ASTNode):
    """
    'Cond' else clause
    """
    def __init__(self, then_body):
        """
        :param then_body: ASTNode 
        """
        super(ASTNode, self).__init__()
        self.then_body = then_body

    def accept(self, visitor, environment):
        return visitor.visit_cond_else_clause(self, environment)

    def print_node_type(self):
        return 'else clause'

    def copy(self):
        return CondElseClause(self.then_body.copy())\
            .add_code_reference(self.s_expr)


class And(ASTNode):
    """
    Logical 'and'
    """
    def __init__(self, cond1, cond2):
        """
        :param cond1: ASTNode 
        :param cond2: ASTNode
        """
        super(ASTNode, self).__init__()
        self.cond1 = cond1
        self.cond2 = cond2

    def accept(self, visitor, env):
        return visitor.visit_and(self, env)

    def print_node_type(self):
        return 'and node'

    def copy(self):
        return And(self.cond1.copy(), self.cond2.copy())\
            .add_code_reference(self.s_expr)


class Or(ASTNode):
    """
    Logical 'or'
    """
    def __init__(self, cond1, cond2):
        """
        :param cond1: ASTNode 
        :param cond2: ASTNode
        """
        super(ASTNode, self).__init__()
        self.cond1 = cond1
        self.cond2 = cond2

    def accept(self, visitor, env):
        return visitor.visit_or(self, env)

    def print_node_type(self):
        return 'or node'

    def copy(self):
        return Or(self.cond1.copy(), self.cond2.copy())\
            .add_code_reference(self.s_expr)


class Id(ASTNode):
    """
    Identifier (variable name)
    """
    def __init__(self, identifier):
        """
        :param identifier: string 
        """
        super(ASTNode, self).__init__()
        self.identifier = identifier

    def accept(self, visitor, env):
        return visitor.visit_id(self, env)

    def print_node_type(self):
        return 'identifier lookup'

    def copy(self):
        return Id(self.identifier).add_code_reference(self.s_expr)


class Fun(ASTNode):
    """
    Function expression
    """
    def __init__(self, params, body):
        """
        :param params: List[string]
        :param body: BodySequence
        """
        super(ASTNode, self).__init__()
        self.params = params
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_fun(self, env)

    def print_node_type(self):
        return 'function definition'

    def copy(self):
        return Fun(
            copy.copy(self.params),
            self.body.copy()
        ).add_code_reference(self.s_expr)


class App(ASTNode):
    """
    Function application
    """
    def __init__(self, fun_expr, arg_exprs):
        """
        :param fun_expr: ASTNode 
        :param arg_exprs: List[ASTNode]
        """
        super(ASTNode, self).__init__()
        self.fun_expr = fun_expr
        self.arg_exprs = arg_exprs

    def accept(self, visitor, env):
        return visitor.visit_app(self, env)

    def print_node_type(self):
        return 'function application'

    def copy(self):
        return App(
            self.fun_expr.copy(),
            [arg.copy() for arg in self.arg_exprs]
        ).add_code_reference(self.s_expr)


class BodySequence(ASTNode):
    """
    Sequence of expressions
    """
    def __init__(self, expressions):
        """
        :param expressions: List[ASTNode] 
        """
        super(ASTNode, self).__init__()
        self.expressions = expressions

    def accept(self, visitor, env):
        return visitor.visit_body(self, env)

    def print_node_type(self):
        return 'expressions body'

    def copy(self):
        return BodySequence(
            [expression.copy() for expression in self.expressions]
        ).add_code_reference(self.s_expr)


class ModuleDefinition(ASTNode):
    """
    Module definition
    """
    def __init__(self, name, body):
        super(ASTNode, self).__init__()
        self.name = name
        self.body = body

    def accept(self, visitor, environment):
        return visitor.visit_module_definition(self, environment)

    def print_node_type(self):
        return 'module definition'

    def copy(self):
        return ModuleDefinition(self.name.copy(), self.body.copy())\
            .add_code_reference(self.s_expr)


class ModuleFunctionExport(ASTNode):
    """
    Module function's export
    """
    def __init__(self, identifiers_to_export):
        super(ASTNode, self).__init__()
        self.identifiers_to_export = identifiers_to_export

    def accept(self, visitor, environment):
        return visitor.visit_module_function_export(self, environment)

    def print_node_type(self):
        return 'module function export'

    def copy(self):
        return ModuleFunctionExport(
            [identifier.copy() for identifier in self.identifiers_to_export]
        ).add_code_reference(self.s_expr)


class ModuleImport(ASTNode):
    """
    Module import
    """
    def __init__(self, module_name):
        super(ASTNode, self).__init__()
        self.module_name = module_name

    def accept(self, visitor, environment):
        return visitor.visit_module_import(self, environment)

    def print_node_type(self):
        return 'module import'

    def copy(self):
        return ModuleImport(self.module_name).add_code_reference(self.s_expr)


class Definition(ASTNode):
    """
    Definition
    """
    def __init__(self, name, expr):
        """
        :param name: string 
        :param expr: ASTNode
        """
        super(ASTNode, self).__init__()
        self.name = name
        self.expr = expr

    def accept(self, visitor, env):
        return visitor.visit_definition(self, env)

    def print_node_type(self):
        return 'definition'

    def copy(self):
        return Definition(self.name, self.expr.copy())\
            .add_code_reference(self.s_expr)


class Local(ASTNode):
    """
    Local definition
    """
    def __init__(self, definitions, body):
        """
        :param definitions: List[Definition]
        :param body: BodySequence
        """
        super(ASTNode, self).__init__()
        self.definitions = definitions
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_local(self, env)

    def print_node_type(self):
        return 'local definition'

    def copy(self):
        return Local(
            [definition.copy() for definition in self.definitions],
            self.body.copy()
        ).add_code_reference(self.s_expr)


class BotNode(ASTNode):
    """
    Bot node expression
    """
    def __init__(self, params, body):
        """
        :param params: List[string] 
        :param body: BodySequence
        """
        super(ASTNode, self).__init__()
        self.params = params
        self.body = body

    def accept(self, visitor, env):
        return visitor.visit_bot_node(self, env)

    def print_node_type(self):
        return 'bot node expression'

    def copy(self):
        return BotNode(
            copy.copy(self.params),
            self.body.copy()
        ).add_code_reference(self.s_expr)


class BotResult(ASTNode):
    """
    Bot node computation result.
    """
    def __init__(self, data, message, next_node):
        super(ASTNode, self).__init__()
        self.data = data
        self.message = message
        self.next_node = next_node

    def accept(self, visitor, env):
        return visitor.visit_bot_result(self, env)

    def print_node_type(self):
        return 'bot result'

    def copy(self):
        return BotResult(
            self.data.copy(),
            self.message.copy(),
            self.next_node.copy()
        ).add_code_reference(self.s_expr)


class SyntaxPattern(ASTNode):
    """
    A pattern in pattern-based macros
    """
    def __init__(self, identifier, arguments):
        """
        :param identifier: string 
        :param arguments: List[string]
        """
        super(ASTNode, self).__init__()
        self.identifier = identifier
        self.arguments = arguments

    def accept(self, visitor, env):
        return visitor.visit_syntax_pattern(self, env)

    def print_node_type(self):
        return 'syntax pattern'

    def copy(self):
        return SyntaxPattern(
            self.identifier,
            copy.copy(self.arguments)
        ).add_code_reference(self.s_expr)


class DefineSyntax(ASTNode):
    """
    Inspired by Racket's define-syntax-rule:
    https://docs.racket-lang.org/guide/pattern-macros.html
    """
    def __init__(self, pattern, template):
        """
        :param pattern: SyntaxPattern
        :param template: SExpr
        """
        super(ASTNode, self).__init__()
        self.pattern = pattern
        self.template = template

    def accept(self, visitor, env):
        return visitor.visit_define_syntax(self, env)

    def print_node_type(self):
        return 'syntax definition'

    def copy(self):
        raise NotImplementedError
