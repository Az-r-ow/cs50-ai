from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Not(And(AKnight, AKnave)),
    Or(AKnight, AKnave),
    # If a is a knight then we can assume that he is a knight and a knave
    Implication(AKnight, And(AKnight, AKnave)),
    # If a is a knave then A is not a Knave and a Knight
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Since everything a knave says is false
    # Then if A is claiming to be a knave and he's saying that both of them are knaves
    # And(AKnave, BKnave) should evaluate as false
    # And since a knight does not lie therefore wouldn't lie to being a knave
    # So we know for sure that A is not a Knight
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Starting with base knowledge
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    # If A's claim is True then B's claim is False
    Implication(Or(And(AKnave, BKnave), And(AKnight, BKnight)), Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),

    # And if B's claim is true than A's claim is false
    Implication(Or(And(AKnave, BKnight), And(AKnight, BKnave)), Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),

    # Another implication if someone's sentence is True than that someone must be a knight
    Implication(Or(And(AKnave, BKnave), And(AKnight, BKnight)), AKnight),
    Implication(Or(And(AKnave, BKnight), And(AKnight, BKnave)), BKnight),

    # From that we can conclude that A and B cannot be both knights cause B would be lying and knights don't lie
    Not(And(AKnight, BKnight)),

    # And we can conclude that they cannot both be Knaves because A's claim would be true and Knave's claims are always False
    Not(And(AKnave, BKnave))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Again, Starting with the base knowledge
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),

    # Then with the biconditionals this time that implies that :
    # If B is a Knave therefore A and C are not Knaves and if A and C are not knaves this results in B being a knave
    # Same goes for C
    Biconditional(And(Not(AKnave), Not(CKnave)), BKnave),
    Biconditional(Not(AKnight), CKnave),

    # Assuming that :
    Implication(BKnight, And(AKnave, CKnave)),
    Implication(BKnave, Not(And(AKnave, CKnave))),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)) ,
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave)))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
