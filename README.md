# Migrated to [Codeberg](https://codeberg.org/milofultz/tablatal_parser)

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

From Devine's site: 

> In the Tablatal file, the first line declares the key, the
spacing between each key defines the length of the parameters for all
subsequent lines. 

It is a much more aesthetically pleasing plaintext data
format, though the tradeoff is malleability, as you must define how large
the field sizes are before getting going (I'll solve this with some kind of
utility if it ever comes up as a problem). 

There is both a to- and from-Tablatal utility. Both use a list of dicts as
their starting point, but can also be used directly in the CLI to interface
with JSON files.


### Tablatal Syntax

* Comments are preceded by a semicolon.
* The header line is all caps and may be preceded by a semicolon (see note below re: `--headers`).
* The spacing of the header line sets the spacing for every column.
* The content is everything that follows the header line. Empty fields default to None.
  
Examples can be found [here at neauoire's page](https://github.com/XXIIVV/oscean/tree/master/src/database).  


### Usage

#### TBTL to JSON

`python3 tbtl_json.py ./path/to/input.tbtl [--headers HEADERS]`

#### JSON to TBTL
 
`python3 json_tbtl.py ./path/to/input.tbtl [--headers HEADERS]`
 
#### `--headers` Option

Using `--headers` when *parsing* `tbtl` will allow you to supply a set of
custom headers separated by commas for the parser to use when outputting JSON.

If this option is unused and the header line is found on a commented line, the
first field will be called "ID" by default. For instance, if the beginning
of your file including your headers looks like this:

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

`python3 tbtl_parse.py ./path/to/input.tbtl --headers "DATE, CODE, HOST, PIC, NAME"`

Using `--headers` when *outputting* `tbtl` will allow you to supply the order 
you want your columns to be output. 
