stack = '#'
pol_not = ''
steps = []
all_ops = ['+', '-', '*', '/', ')', '#', ',']


class Grammatic:
    def __init__(self, rule, pol_not, cond, proc):
        self.rule = rule  # ('E', 'E+T')
        self.pol_not = pol_not  # 'ET+'
        self.cond = cond  # ('+', '-', '#')
        self.proc = proc  # '+'

    def process(self, seq, seq_i: int, gram_i: int):
        global stack
        global pol_not
        global steps

        # a - is an abstract terminal, so we should replace it with an actual terminal from stack
        rule_1 = self.rule[1]
        if stack[-1].islower() and rule_1 == 'a':
            rule_1 = stack[-1]

        proc = self.proc
        if stack[-1].islower() and proc == 'a':
            proc = stack[-1]

        cur_let = seq[seq_i]

        if stack.endswith(rule_1) and cur_let in self.cond:
            pol_not += proc
            steps.append([stack, cur_let, seq[seq_i+1:], str(gram_i + 1), pol_not])
            stack = stack[:-len(rule_1)] + self.rule[0]
            return True
        return False


grams = [
    Grammatic(rule=('E', 'E+T'), pol_not='ET+', cond=[op for op in all_ops if op not in ('*', '/')], proc='+'),
    Grammatic(rule=('E', 'E-T'), pol_not='ET+', cond=[op for op in all_ops if op not in ('*', '/')], proc='-'),
    Grammatic(rule=('E', 'T'), pol_not='T', cond=[op for op in all_ops if op not in ('*', '/')], proc=''),
    Grammatic(rule=('T', 'T*F'), pol_not='TF*', cond=all_ops[:], proc='*'),
    Grammatic(rule=('T', 'T/F'), pol_not='TF/', cond=all_ops[:], proc='/'),
    Grammatic(rule=('T', 'F'), pol_not='F', cond=all_ops[:], proc=''),
    Grammatic(rule=('F', 'f()'), pol_not='', cond=all_ops[:], proc='[F ARGS 0]'),
    Grammatic(rule=('F', 'f(E)'), pol_not='', cond=all_ops[:], proc='[F ARGS 1]'),  # F - represents specific function
    Grammatic(rule=('F', 'f(E,E)'), pol_not='', cond=all_ops[:], proc='[F ARGS 2]'),
    Grammatic(rule=('F', 'f(E,E,E)'), pol_not='', cond=all_ops[:], proc='[F ARGS 3]'),
    Grammatic(rule=('F', 'sin(E)'), pol_not='', cond=all_ops[:], proc='[SIN]'),  # S - represents sinus
    Grammatic(rule=('F', '-E'), pol_not='', cond=all_ops[:], proc='[UNARY MINUS]'),  # _ - represents unary minus
    Grammatic(rule=('F', 'a'), pol_not='a', cond=all_ops[:], proc='a'),
    Grammatic(rule=('F', '(E)'), pol_not='', cond=all_ops[:], proc=''),
]


def iterate_through_grams(seq, seq_i):
    for gram_i, gram in enumerate(grams):
        if gram.process(seq, seq_i, gram_i):
            return True
    return False