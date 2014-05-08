# LVR_team5

## Jani, Jaka

### team5_sat_solver
Modul team5_sat_solver vsebuje ogrodje za kontrukcijo in obravnavo logičnih izrazov izjavnega računa. Priložen je reševalnik problema SAT in nekaj primerov prevedb znanih problemov na SAT.
Zavoljo čiste vesti so dodani tudi enotski testi.

### Algoritem
Uporabili smo algoritem [DPLL](https://en.wikipedia.org/wiki/DPLL_algorithm) (Davis–Putnam–Logemann–Loveland).
Algoritem smo nadgradili s sortiranjem  seznama stavkov po velikosti (krajše stavke obdelamo prej) na vsakem koraku in z absorbcijo ponavljajočih se podizrazov.

### Datoteke
V modulu boste našli naslednje datoteke:
- **cnf.py** - vsebuje metodo za pretvorbo poljubnega izraza v konjuktivno normalno obliko in ostale sorodne metode,
- **dpll.py** - vsebuje algoritem DPLL in sorodne metode,
- **operands.py** - razredi za delo z logičnimi izrazi (konjunkcija, disjunkcija itd.),
- **preveba_coloring.py** - prevedba problema barvanja grafa na problem SAT,
- **preveba_hadamard.py** - prevedba problema [Hadamardove matrike](https://en.wikipedia.org/wiki/Hadamard_matrix) na problem SAT,
- **preveba_sudoku.py** - prevedba problema rešvanje zagonetenke *sudoku* na problem SAT,
- **primeri_uporabe.py** - (**TO JE ZANIMIVO**) demonstracija uporabe celotnega projekta, uporabljena večina funkcij iz vseh modulov, dodani so tudi izpisi, ki prikazujejo potek izvajanja programa. Notri so tudi primerjave optimiziranih in neoptimiziranih procedur (npr. prevedbe in resevanja Hadamardove matrike).
- **simplify.py** - metode za poenostavljanje logičnih izrazov,
- **UnitTests.py** - enotski testi,
- **utils.py** - pomožne metode, štoparica za merjenje izvajalnih časov.
               
Pri razvoju smo uporabljali python 2.7.5.
Zunanje odvisnosti: unittest, time, itertools (vse priloženo pythonu).

Spodnja slika prikazuje graf medsebojnih odvisnosti zgoraj navedenih datotek.

[Graf dependecyjev](http://imgur.com/RvuqM2x)

### Uporaba
Glej **primeri_uporabe.py**. Na kratko: gradimo poljuben izraz  z operands ali pa uporabimo eno od prevedb; dobljeno formulo lahko nato obdelujemo z metodami iz cnf.py, simplify.py ali pa preprosto poženemo algoritem iz dpll.py, da dobimo rešitev problema SAT (za dano formulo).

###UnitTests
Datoteka UnitTests je sestavljena iz vec metod (testov), ki testirajo razlicne aspekte programa. Najlazje je teste poganjati v pycharmu, saj nam to lepo izpise teste ter meri njihov cas izvajanja. To naredimo enostavno tako, da kliknemo izven metode z desnim gumbom in pozenemo "Run Unittests in Mytestcase" (opomba. nastavljen moramo imeti interpreter za python, drugace ni tele opcije). Ce zelimo pognati, samo dolocen test (metodo) kliknemo z desnim gumbom na metodo ter jo pozenemo.

####Opomba
Problem sudokuja, je prevelik, da bi ga nas dpll resil v normalnem casu. Formula, ki jo zgeneriramo je pravilna in ustreza resitvi sudokuja. Ce nam ne verjamete jo testirajte na roke ;).

##TLDR
* **primer_uporabe.py** - vstopna točka za igranje s programom, primeri uporabe večine funkcij, obogateni s komentarji (slednji uporabnika vodijo od vpeljave logične spremenljivke do prevedbe in reševanja SAT). Poudarek je na demonstraciji praktične rabe - kako naredim izraz, kako prevebem problem na SAT, kako rešim problem SAT, kako dobim CNF obliko, kako izmerim cas, kako testiram?
* UnitTests.py - pravilnost programa, testi,
* ostale .py datoteke - omogočajo delovanje zgornjih dveh, njihova nameskost je razvidna iz imen.