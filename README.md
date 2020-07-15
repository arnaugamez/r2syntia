***r2syntia*** is a proof-of-concept integration of the program synthesis tool Syntia into the reverse engineering framework radare2. I developed it as a demonstration for my BSc thesis *Code deobfuscation by program synthesis-aided simplification of Mixed Boolean-Arithmetic expressions*, which will be publicly available soon.

The current interface is rather limited by the way the script is invoked. The plan is to make it into a native r2 plugin in the near future (hopefully before end of summer) which will permit configuring and leveraging more aspects that are already available within Syntia.

A Dockerfile is included to ease the installation process for quick testing. It will build a container with all the tools, requirements and test files placed in `/opt` folder.

# Manual installation

Currently, r2syntia.py is provided as a single file script.

## Dependencies

We assume a GNU/Linux system with python3 installation; python2 support is not guaranteed.

### radare2
```
git clone https://github.com/radareorg/radare2.git
cd radare2
./sys/install.sh
```

#### r2pipe
```
pip3 install r2pipe
```

### Syntia

I am using a slightly modified version of Syntia, based on top of https://github.com/mrphrazer/syntia. The most notable modifications have been made to the `mcts/grammar.py` file in order to be able to easily describe the grammar to be used externally, as well as some minor tuning to retrieve information in a more relevant way. Currently, the modified version of Syntia is assumed to be placed in the same directory as r2syntia.py script (as it is placed in this repository). However, it could be easily installed as a system-wide python module. Its installation would be automated when the r2 plugin is ready, and probably moved to a separate repository forked from Syntia repo.

#### Requirements

```
pip3 install orderedset
pip3 install z3-solver
```

# Usage

Inside an r2 shell, launch r2syntia script file with the following arguments in order:

- bit size
- start offset
- finish offset
- input variables
- output variable

Variables can be registers or memory locations. In case of memory locations, you should define them inside brackets, supporting addressing through registers with respect to their values at the start offset (for input variables) and at the finish offset (for output variable).

## Examples

Call r2syntia with bit size `64`, start offset `0x0041b264`, finish offset `0x0041b327`, input variables `rdi rsi rdx rcx r8`  and output variable `rax`.

```
#!pipe python ./r2syntia.py 64 0x0041b264 0x0041b327 rdi rsi rdx rcx r8 rax
```

Call r2syntia with bit size `64`, start offset `0x0041b264`, finish offset `0x0041b327`, input variables `[rbp-0x8] [rbp-0x10] [rbp-0x18] [rbp-0x20] [rbp-0x28]`  and output variable `rax`

```
#!pipe python ./r2syntia.py 64 0x0041b280 0x0041b327 [rbp-0x8] [rbp-0x10] [rbp-0x18] [rbp-0x20] [rbp-0x28] rax
```

The examples above apply to the file `obfuscated` under the `test_files` folder.

# Known issues and tentative road map

- [x] Add support for memory locations to be used as I/O variables
- [ ] Add support for variables of different bit size (WIP)
- [ ] Create r2 plugin and add it into r2pm:
  - [ ] Add support for synthesizing multiple output variables
  - [ ] Add support for tuning Syntia configuration parameters

I put last two items inside the r2 plugin one, as these should be trivial to implement it if we get access to custom r2 configuration variables by registering r2syntia as an r2 core plugin. Another benefits from it would be the ability to tune verbosity level and input grammar file without having to hardcode it (as it is now) or adding even more arguments to r2syntia pipe calling.
