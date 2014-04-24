# LVR_team5

## LVR Jani, Jaka

### team5_sat_solver
Modul team5_sat_solver vsebuje ogrodje za delo z logičnimi izrazi, reševalnik problema SAT in nekaj primerov prevedb znanih problemov na problem SAT. Za čisto vest so dodani tudi enotski testi.

### Uporabljeni algoritem
Uporabili smo algoritem [DPLL](https://en.wikipedia.org/wiki/DPLL_algorithm) (Davis–Putnam–Logemann–Loveland). Algoritem smo nadgradili s sortiranjem  seznama stavkov po velikosti (krajše stavke obdelamo prej) na vsakem koraku.

### Datoteke
V modulu boste našli naslednje datoteke:
- **cnf.py** - vsebuje metode za pretvorbo poljubnega izraza v konjuktivno normalno obliko in ostale sorodne metode,
- **dpll.py** - vsebuje algoritem DPLL in sorodne metode,
- **operands.py** - razredi za delo z logičnimi izrazi (konjunkcija, disjunkcija itd.),
- **preveba_coloring.py** - prevedba problema barvanja grafa na problem SAT,
- **preveba_hadamard.py** - prevedba problema [Hadamardove matrike](https://en.wikipedia.org/wiki/Hadamard_matrix) na problem SAT,
- **preveba_sudoku.py** - prevedba problema rešvanje zagonetenke *sudoku* na problem SAT,
- **primeri_uporabe.py** - demonstracija uporabe celotnega modula (**TO JE ZANIMIVO**),
- **simplify.py** - metode za poenostavljanje logičnih izrazov,
- **UnitTests.py** - enotski testi,
- **utils.py** - pomožne metode, štoparica za merjenje izvajalnih časov.

### Uporaba
Glej **primeri_uporabe.py. Na kratko: gradimo poljuben izraz  z operands ali pa uporabimo eno od prevedb; dobljeno formulo lahko nato obdelujemo z metodami iz cnf.py, simplify.py ali pa preprosto poženemo algoritem iz dpll.py, da dobimo rešitev problema SAT (za dano formulo).


