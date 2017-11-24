# Model Checking Ethereum Byteode using the Process Analysis Toolkit (PAT)

### Gabriela Merz

This project aims to build a framework for model checking Ethereum bytecode
using the Process Analysis Toolkit (PAT, http://sav.sutd.edu.sg/PAT/?page_id=2660).
PAT is an enhanced simulator, model checker, and refinement checker for concurrent
and real time systems. 

To model check EVM contracts, the opcodes for the bytecode (push, pop, add, etc.) 
are translated in to a CSP#, a language for communicating sequential process, that
PAT can understand. 

As of right now, the main goal is to be able to ensure that a contract will never
run out of gas. In the future, we hope to model check other aspects of EVM contract
code (for instance, protecting against the "recursive call" DAO exploit). 

## TODO List
1. Translate all opcodes
	a. Because our main goal is gas price, environment information calls + system
	calls don't actually "work" as expected, but gas price for using them is 
	decremented appropriately
	b. All base opcodes contain invariant checking (checking the size of the stack), 
	otherwise a failure flag is set
	c. We use PAT's Linear Temporal Logic (LTL) feature to assert that the failure
	flag is never set + that the amount of gas never falls below 0 
2. Decrement gas prices on opcodes appropiately
3. Translate EVM opcodes to CSP opcode in main, run and model-check! (Perhaps a 
	quick python script?) 
4. Unit testing, unit testing, unit testing
5. Find a contract that runs out of gas an sanity check that our model checker 
   also finds that it runs our of gas