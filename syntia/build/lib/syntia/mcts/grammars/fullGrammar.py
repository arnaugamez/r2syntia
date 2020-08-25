from orderedset import OrderedSet

OP1 = OrderedSet(["bvnot",
                  "bvneg",
                  ])
OP2 = OrderedSet(["bvadd",
                  "bvsub",
                  "bvmul",
                  "bvudiv",
                  "bvsdiv",
                  "bvurem",
                  "bvsrem",
                  "bvshl",
                  "bvlshr",
                  "bvashr",
                  "bvand",
                  "bvor",
                  "bvxor",
                  "zero_extend",
                  "bvconcat",
                  ])

OP3 = OrderedSet(["bvextract",
                  "sign_extend"
                  ])

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