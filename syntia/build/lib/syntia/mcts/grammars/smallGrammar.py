from orderedset import OrderedSet

OP1 = OrderedSet(["bvnot",
                  "bvneg",
                  ])

OP2 = OrderedSet(["bvadd",
                  "bvsub",
                  "bvmul",
                  "bvand",
                  "bvor",
                  "bvxor"
                  ])

OP3 = OrderedSet()

COMMUTATIVE_OPS = OrderedSet(["bvadd",
                              "bvmul",
                              "bvand",
                              "bvor",
                              "bvxor"])

NON_TERMINALS = OrderedSet(["u8",
                            "u16",
                            "u32",
                            "u64",
                            ])