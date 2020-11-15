***r2syntia*** is a proof-of-concept integration of the program synthesis tool Syntia into the reverse engineering framework radare2. I developed it as a demonstration for my BSc thesis [*Code deobfuscation by program synthesis-aided simplification of Mixed Boolean-Arithmetic expressions*](https://github.com/arnaugamez/tfg).

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

# More
***UPDATE***: After exploring a bit on plugin dev, and wanting to support Cutter as well, I think it makes more sense (and could be easier) to have a Cutter plugin that can act itself as an r2pipe python callable script in the way in works now within r2. This idea is taken from https://github.com/CheckPointSW/Cyber-Research/blob/master/Malware/APT32/APT32GraphDeobfuscator.py.

Thus, the following tasks roughly sum up what could be done in order to make r2syntia a slightly better integration.
  - [ ] Create Cutter plugin as a compatible r2pipe callable script for r2
  - [ ] Add support for tuning Syntia configuration parameters
  - [ ] Add support for synthesizing multiple output variables
  
However, as this was intended as a proof-of-concept for my BSc thesis, which is not actually using latest advances on program synthesis for code deobfuscation (as already noted in my BSc thesis), I am not finding much time to work through improving it. Anyway, I leave the previous tasks just in case I find some free time to get into it, even if only as a way of playing with Cutter plugin's creation. Also, feel free to implement any of the previous tasks and send a PR, if you feel like doing so. But please note: I don't think I will be coming back to it anytime soon.
