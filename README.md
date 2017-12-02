Ethereal model checker: TODOS

“Big Questions"
How de we grab environment information about the contracts gasLimit?
Does PAT support infinite state systems (when a variable can take on any value instead of a create one) and if not / so how do we deal with gas price?
Tranlsation
Finish translating the rest of the etherealmcommands
Python script to translate contract opcodes to our CSP language
Needs to handle jumps
Needs to push/pop arguments appropriately
Arguments represented in hex and sometimes pushes/dups more than one thing
Make sure to cross-reference with CSP script
Write the paper! ShareLatex doc https://www.sharelatex.com/project/5a1c5e3a1f8798792b2f139e