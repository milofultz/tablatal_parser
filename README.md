# Tablatal Parser

I'm rethinking my Track and Tod apps for tracking my tasks, mood, and other
data after checking out [Josh Avanier's Log](https://avanier.now.sh/w/log.html),
[V's Log](https://v-os.ca/timekeeping), 
[Devine Lu Linvega's Horaire](https://wiki.xxiivv.com/site/horaire.html) and
others. I am determined to keep my log plaintext and was not
satisfied with options like CSV or TSV, as they look terrible when reading
in a plain text editor. I eventually found 
[Devine's Tablatal](https://wiki.xxiivv.com/site/tablatal.html) and am looking
forward to using it with my system. 

From Devine's site: "In the Tablatal file, the first line declares the key, the
spacing between each key defines the length of the parameters for all
subsequent lines." It is a much more aesthetically pleasing plaintext data
format, though the tradeoff is malleability, as you must define how large
the field sizes are before getting going (I'll solve this with some kind of
utility if it ever comes up as a problem). 


### Syntax

* Comments are preceded by a semicolon.
* The header line is expected to be all caps and may be preceded by a
  semicolon as if a comment. The spacing of this header line sets the spacing
  for all content that follows.
* The content is everything that follows the header line. Empty fields
  default to None.
  
Examples can be found [here at neauoire's page](https://github.com/XXIIVV
/oscean/tree/master/src/database).  


### Usage

As a CLI, the parser takes in a plaintext Tablatal file (`tbtl`) and
returns a `JSON` file. There is one optional argument `--headers`, which
you can supply a set of custom headers separated by commas for the parser
to use when outputting. For instance, if the beginning of your file
including your headers looks like this:

```
; The horaire is a collection of logs.
; https://wiki.xxiivv.com/site/tablatal.html
;     CODE HOST                 PIC NAME
;     7    12                   33  37
20X09 +300 talk                     Talk at Speakers Series, SNSYC
20X07 +300 talk                     Grundlagen der digitalen Kommunikation
20V08 -332 orca
...
```

The header line is started by a semicolon, which would obfuscate the parser
from giving it a useful name. This can be remedied via the CLI:

`python3 tbtl_parse.py input.tbtl output.json --headers "DATE, CODE, HOST, PIC,
 NAME"`