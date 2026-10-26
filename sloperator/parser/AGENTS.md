# Parser instructions

Conventions for `sloperator/parser/parser.py`. The project-wide rules in the
repository's root `AGENTS.md` also apply.

## One method per grammar rule

- Each nonterminal in the grammar in `docs/spec.md` gets exactly one method, named after
  the rule, and that method implements the whole rule. Don't split a rule across helper
  methods: `term` parses `factor (("+" | "-") factor)*` in one loop, and `factor` parses
  `unary (("*" | "/") unary)*` in one loop. There is no `factor_tail` or equivalent.
- A recursive-descent method returns the node it built and only consumes the tokens its
  own rule owns. Nesting is expressed by calling the next method down the precedence
  ladder (`expression` → `logic_or` → `logic_and` → `comparison` → `equality` → `term` →
  `factor` → `unary` → `call` → `primary`), never by re-implementing a lower rule inline.
- Keep the loop shape for left-associative repetition: parse the left operand once, then
  fold each operator into a new `Binary` on the left. Left associativity comes from that
  shape, so don't convert these loops to recursion over the same rule.
- Repetition of a delimited list (parameters, call arguments, block statements) stays in
  the method that owns the construct rather than being split into `*_tail` helpers.
- The token plumbing (`match`, `check`, `advance`, `peek`, `peek_next`, `previous`,
  `at_end`) and the two error helpers (`expect`, `error`) are infrastructure, not grammar
  rules, so they live at the bottom of the class and stay free of rule-specific logic.

## Syntax errors describe the token found

- Every syntax error says what was expected *and* what was actually found. Build messages
  through `self.error(...)`, which appends `, found '<lexeme>'`, so a message passed to
  `expect` should name the expected thing only: `"expected ')' after parameters"`, not
  `"expected ')', found 'x'"`.
- At end of input, `error` reports `, but reached end of file` instead of a trailing
  empty token. Don't special-case EOF at call sites.
- Report the position of the offending token: `expect` raises on `self.peek()`, the token
  that failed to match. The only place a consumed token's position is correct is a
  context violation such as `ship` outside a `clanker`, where the offending token is the
  keyword already advanced past.
- Messages are lowercase, unpunctuated, and phrased from the parser's point of view
  ("expected an expression", "expected '{' after vibe condition"). Include the offending
  lexeme in the message itself (e.g. `duplicate parameter name 'a'`) when the message
  names a specific token.
- `tests/test_parser.py::test_syntax_errors` asserts exact `line` and `message` strings.
  A new error path means a new parametrized case there; changing an existing message
  means updating it in the same change.
