from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Set
import itertools
import re
import sys


@dataclass
class Expression:
    text: str
    value: int
    contains: int


def add(e1: Expression, e2: Expression) -> Expression:
    """Add two expressions and return result."""
    return Expression(
        text=f"({e1.text}+{e2.text})",
        value=e1.value + e2.value,
        contains=e1.contains + e2.contains,
    )


def multiply(e1: Expression, e2: Expression) -> Optional[Expression]:
    """Multiply two expressions and return result.
    Will return None in case of uncessary multiply."""
    if e1.value == 1 or e2.value == 1:
        return None
    return Expression(
        text=f"{e1.text}*{e2.text}",
        value=e1.value * e2.value,
        contains=e1.contains + e2.contains,
    )


def subtract(e1: Expression, e2: Expression) -> Optional[Expression]:
    """Subtract two expressions and return result.
    Will return non in case of invalid subtraction."""
    if e1.value <= e2.value:
        return None
    return Expression(
        text=f"({e1.text}-{e2.text})",
        value=e1.value - e2.value,
        contains=e1.contains + e2.contains,
    )


def divide(e1: Expression, e2: Expression) -> Optional[Expression]:
    """Divide two expressions and return result.
    Will return None in case of invalid or uncessary division."""
    if e2.value == 1 or e1.value % e2.value != 0:
        return None
    return Expression(
        text=f"{e1.text}/({e2.text})",
        value=e1.value // e2.value,
        contains=e1.contains + e2.contains,
    )


def create_id(e: Expression, n_numbers: int) -> int:
    return (e.value << n_numbers) + e.contains


def combinations(e1: Expression, e2: Expression) -> List[Expression]:
    """Return all valid combinations of expressions."""
    operations = [add, multiply, subtract, divide]
    combs = [operation(e1, e2) for operation in operations]
    return [comb for comb in combs if comb is not None]


def permutations(
    v1: List[Expression], v2: List[Expression], id_set: Set[int], n_numbers: int
) -> List[Expression]:
    perms = []
    for e1, e2 in itertools.product(v1, v2):
        if e1.contains & e2.contains != 0:
            continue
        for comb in combinations(e1, e2):
            comb_id = create_id(comb, n_numbers)
            if comb_id in id_set:
                continue
            perms.append(comb)
            id_set.add(comb_id)
    return perms


def run_numbers(numbers: List[int], target: int) -> str:
    # Generate base expressions
    n_numbers = len(numbers)
    expression_sets = [[] for _ in numbers]
    expression_sets[0] = [
        Expression(str(num), num, 2**i) for i, num in enumerate(numbers)
    ]
    id_set = set(create_id(e, n_numbers) for e in expression_sets[0])

    # Find all useful combinations
    for i in range(n_numbers):
        for j in range(i):
            expression_sets[i].extend(
                permutations(
                    v1=expression_sets[j],
                    v2=expression_sets[i - j - 1],
                    id_set=id_set,
                    n_numbers=n_numbers,
                )
            )

    # Return best expression
    expressions = []
    for v in expression_sets:
        expressions.extend(v)
    expressions.sort(key=lambda e: abs(e.value - target))
    best_expression = expressions[0]
    return f"{best_expression.text} = {best_expression.value}"


def main():
    print("numbers = ", end="")
    separators = r" , |, | ,|,|  | "
    numbers = re.split(separators, input().strip())
    try:
        numbers = list(map(int, numbers))
        target = int(input("target = "))
    except ValueError:
        sys.exit("error: invalid input")
    print(run_numbers(numbers, target))


if __name__ == "__main__":
    main()
    