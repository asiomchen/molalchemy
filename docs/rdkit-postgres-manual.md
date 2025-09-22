## The RDKit database cartridge[¶](#the-rdkit-database-cartridge "Link to this heading")

## What is this?[¶](#what-is-this "Link to this heading")

This document is a tutorial and reference guide for the RDKit PostgreSQL cartridge.

If you find mistakes, or have suggestions for improvements, please either fix them yourselves in the source document (the .md file) or send them to the mailing list: [rdkit-discuss@lists.sourceforge.net](mailto:rdkit-discuss%40lists.sourceforge.net) (you will need to subscribe first)

## Tutorial[¶](#tutorial "Link to this heading")

### Introduction[¶](#introduction "Link to this heading")

### Creating databases[¶](#creating-databases "Link to this heading")

#### Configuration[¶](#configuration "Link to this heading")

The timing information below was collected on a commodity desktop PC (Dell Studio XPS with a 2.9GHz i7 CPU and 8GB of RAM) running Ubuntu 12.04 and using PostgreSQL v9.1.4. The database was installed with default parameters.

To improve performance while loading the database and building the index, I changed a couple of postgres configuration settings in postgresql.conf :

And to improve search performance, I allowed postgresql to use more memory than the extremely conservative default settings:

#### Creating a database from a file[¶](#creating-a-database-from-a-file "Link to this heading")

In this example I show how to load a database from the SMILES file of commercially available compounds that is downloadable from emolecules.com at URL [http://downloads.emolecules.com/free/](http://downloads.emolecules.com/free/)

If you choose to repeat this exact example yourself, please note that it takes several hours to load the 6 million row database and generate all fingerprints.

First create the database and install the cartridge:

Now create and populate a table holding the raw data:

Create the molecule table, but only for SMILES that the RDKit accepts:

The last step is only required if you plan to do substructure searches.

#### Loading ChEMBL[¶](#loading-chembl "Link to this heading")

Start by downloading and installing the postgresql dump from the ChEMBL website [ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest](ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest)

Connect to the database, install the cartridge, and create the schema that we’ll use:

Create the molecules and build the substructure search index:

Create some fingerprints and build the similarity search index:

Here is a group of the commands used here (and below) in one block so that you can just paste it in at the psql prompt:

### Substructure searches[¶](#substructure-searches "Link to this heading")

Example query molecules taken from the [eMolecules home page](http://www.emolecules.com/):

Notice that the last two queries are starting to take a while to execute and count all the results.

Given we’re searching through 1.7 million compounds these search times aren’t incredibly slow, but it would be nice to have them quicker.

One easy way to speed things up, particularly for queries that return a large number of results, is to only retrieve a limited number of results:

#### SMARTS-based queries[¶](#smarts-based-queries "Link to this heading")

Oxadiazole or thiadiazole:

This is slower than the pure SMILES query, this is generally true of SMARTS-based queries.

#### Using Stereochemistry[¶](#using-stereochemistry "Link to this heading")

Note that by default stereochemistry is not taken into account when doing substructure queries:

This can be changed using the rdkit.do\_chiral\_sss configuration variable:

#### Tuning queries[¶](#tuning-queries "Link to this heading")

It is frequently useful to be able to exert a bit more control over substructure queries without having to construct complex SMARTS queries. The cartridge function `mol_adjust_query_properties()` can be used to do just this. Here is an example of the default behavior, using a  
query for 2,6 di-substituted pyridines:

By default `mol_adjust_query_properties()` makes the following changes to the molecule:

We can control the behavior by providing an additional JSON argument. Here’s an example where we disable the additional degree queries:

or where we don’t add the additional degree queries to ring atoms or dummies (they are only added to chain atoms):

The options available are:

The various `Flags` arguments mentioned above, which control where particular options are applied, are constructed by combining operations from the list below with the `|` character.

### Similarity searches[¶](#similarity-searches "Link to this heading")

Basic similarity searching:

Usually we’d like to find a sorted listed of neighbors along with the accompanying SMILES. This SQL function makes that pattern easy:

#### Adjusting the similarity cutoff[¶](#adjusting-the-similarity-cutoff "Link to this heading")

By default, the minimum similarity returned with a similarity search is 0.5. This can be adjusted with the rdkit.tanimoto\_threshold (and rdkit.dice\_threshold) configuration variables:

### Using the MCS code[¶](#using-the-mcs-code "Link to this heading")

The most straightforward use of the MCS code is to find the maximum common substructure of a group of molecules:

The same thing can be done with a SMILES column:

It’s also possible to adjust some of the parameters to the FMCS algorithm, though this is somewhat more painful as of this writing (the 2017\_03 release cycle). Here are a couple of examples:

```
chembl_25=# select fmcs_smiles(str,'{"Threshold":0.8}') from
chembl_25-#    (select string_agg(m::text,' ') as str from rdk.mols
chembl_25(#    join compound_records using (molregno) where doc_id=4) as str ;

                                                                           fmcs_smiles                                                                            
------------------------------------------------------------------------------------------------------------------------------------------------------------------
 [#6]-[#6]-[#8]-[#6](-[#6](=[#8])-[#7]-[#6](-[#6])-[#6](-,:[#6])-,:[#6])-[#6](-[#8])-[#6](-[#8])-[#6](-[#8]-[#6]-[#6])-[#6]-[#7]-[#6](-[#6])-[#6](-,:[#6])-,:[#6]
(1 row)

Time: 9673.949 ms
chembl_25=#
chembl_25=# select fmcs_smiles(str,'{"AtomCompare":"Any"}') from
chembl_25-#    (select string_agg(m::text,' ') as str from rdk.mols
chembl_25(#    join compound_records using (molregno) where doc_id=4) as str ;
                                                                              fmcs_smiles                                                                               
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 [#6]-,:[#6,#7]-[#8,#6]-[#6,#7](-[#6,#8]-[#7,#6]-,:[#6,#7]-,:[#6,#7]-,:[#7,#6]-,:[#6])-[#6,#7]-[#6]-[#6](-[#8,#6]-[#6])-[#6,#7]-[#7,#6]-[#6]-,:[#6,#8]-,:[#7,#6]-,:[#6]
(1 row)

Time: 304.332 ms
```

*Note* The combination of `"AtomCompare":"Any"` and a value of `"Threshold"` that is less than 1.0 does a quite generic search and can results in very long search times. Using `"Timeout"` with this combination is recommended:

Available parameters and their default values are:

## Reference Guide[¶](#reference-guide "Link to this heading")

### New Types[¶](#new-types "Link to this heading")

### Parameters[¶](#parameters "Link to this heading")

### Operators[¶](#operators "Link to this heading")

#### Similarity search[¶](#similarity-search "Link to this heading")

#### Substructure and exact structure search[¶](#substructure-and-exact-structure-search "Link to this heading")

#### Molecule comparison[¶](#molecule-comparison "Link to this heading")

*Note* Two molecules are compared by making the following comparisons in order. Later comparisons are only made if the preceding values are equal:

\# Number of atoms # Number of bonds # Molecular weight # Number of rings

If all of the above are the same and the second molecule is a substructure of the first, the molecules are declared equal, Otherwise (should not happen) the first molecule is arbitrarily defined to be less than the second.

There are additional operators defined in the cartridge, but these are used for internal purposes.

### Functions[¶](#functions "Link to this heading")

#### Fingerprint Related[¶](#fingerprint-related "Link to this heading")

##### Generating fingerprints[¶](#generating-fingerprints "Link to this heading")

##### Working with fingerprints[¶](#working-with-fingerprints "Link to this heading")

##### Fingerprint I/O[¶](#fingerprint-i-o "Link to this heading")

#### Molecule Related[¶](#molecule-related "Link to this heading")

##### Molecule I/O and Validation[¶](#molecule-i-o-and-validation "Link to this heading")

+   is\_valid\_smiles(smiles) : returns whether or not a SMILES string produces a valid RDKit molecule.
    
+   is\_valid\_ctab(ctab) : returns whether or not a CTAB (mol block) string produces a valid RDKit molecule.
    
+   is\_valid\_smarts(smarts) : returns whether or not a SMARTS string produces a valid RDKit molecule.
    
+   is\_valid\_mol\_pkl(bytea) : returns whether or not a binary string (bytea) can be converted into an RDKit molecule. (*available from Q3 2012 (2012\_09) release*)
    
+   mol\_from\_smiles(smiles) : returns a molecule for a SMILES string, NULL if the molecule construction fails.
    
+   mol\_from\_smarts(smarts) : returns a molecule for a SMARTS string, NULL if the molecule construction fails.
    
+   mol\_from\_ctab(ctab, bool default false) : returns a molecule for a CTAB (mol block) string, NULL if the molecule construction fails. The optional second argument controls whether or not the molecule’s coordinates are saved.
    
+   mol\_from\_pkl(bytea) : returns a molecule for a binary string (bytea), NULL if the molecule construction fails. (*available from Q3 2012 (2012\_09) release*)
    
+   qmol\_from\_smiles(smiles) : returns a query molecule for a SMILES string, NULL if the molecule construction fails. Explicit Hs in the SMILES are converted into query features on the attached atom.
    
+   qmol\_from\_ctab(ctab, bool default false) : returns a query molecule for a CTAB (mol block) string, NULL if the molecule construction fails. Explicit Hs in the SMILES are converted into query features on the attached atom. The optional second argument controls whether or not the molecule’s coordinates are saved.
    
+   mol\_to\_smiles(mol) : returns the canonical SMILES for a molecule.
    
+   mol\_to\_cxsmiles(mol) : returns the CXSMILES for a molecule (*available from 2021\_09 release*).
    
+   mol\_to\_smarts(mol) : returns SMARTS string for a molecule.
    
+   mol\_to\_cxsmarts(mol) : returns the CXSMARTS for a molecule (*available from 2021\_09 release*).
    
+   mol\_to\_pkl(mol) : returns binary string (bytea) for a molecule. (*available from Q3 2012 (2012\_09) release*)
    
+   mol\_to\_ctab(mol,bool default true, bool default false) : returns a CTAB (mol block) string for a molecule. The optional second argument controls whether or not 2D coordinates will be generated for molecules that don’t have coordinates. The optional third argument (available since the 2021\_09 release) controls whether or not a V3000 ctab should be generated.
    
+   mol\_to\_v3kctab(mol,bool default true) : returns a CTAB (mol block) string for a molecule. The optional second argument controls whether or not 2D coordinates will be generated for molecules that don’t have coordinates (*available from 2021\_09 release*).
    
+   mol\_to\_svg(mol,string default ‘’,int default 250, int default 200, string default ‘’) : returns an SVG with a drawing of the molecule. The optional parameters are a string to use as the legend, the width of the image, the height of the image, and a JSON with additional rendering parameters. (*available from the 2016\_09 release*)
    
+   mol\_to\_json(string) : returns the commonchem JSON for a molecule. (*available from the 2021\_09 release*)
    
+   mol\_from\_json(string) : returns a molecule for a commonchem JSON string, NULL if the molecule construction fails. (*available from the 2021\_09 release*)
    

##### Substructure operations[¶](#substructure-operations "Link to this heading")

##### Descriptors[¶](#descriptors "Link to this heading")

+   mol\_amw(mol) : returns the AMW for a molecule.
    
+   mol\_exactmw(mol) : returns the exact MW for a molecule (*available from 2021\_09 release*).
    
+   mol\_logp(mol) : returns the MolLogP for a molecule.
    
+   mol\_tpsa(mol) : returns the topological polar surface area for a molecule (*available from Q1 2011 (2011\_03) release*).
    
+   mol\_labuteasa(mol) : returns Labute’s approximate surface area (ASA) for a molecule (*available from 2021\_09 release*).
    
+   mol\_fractioncsp3(mol) : returns the fraction of carbons that are sp3 hybridized (*available from 2013\_03 release*).
    
+   mol\_hba(mol) : returns the number of Lipinski H-bond acceptors (i.e. number of Os and Ns) for a molecule.
    
+   mol\_hbd(mol) : returns the number of Lipinski H-bond donors (i.e. number of Os and Ns that have at least one H) for a molecule.
    
+   mol\_numatoms(mol) : returns the total number of atoms in a molecule.
    
+   mol\_numheavyatoms(mol) : returns the number of heavy atoms in a molecule.
    
+   mol\_numrotatablebonds(mol) : returns the number of rotatable bonds in a molecule (*available from Q1 2011 (2011\_03) release*).
    
+   mol\_numheteroatoms(mol) : returns the number of heteroatoms in a molecule (*available from Q1 2011 (2011\_03) release*).
    
+   mol\_numrings(mol) : returns the number of rings in a molecule (*available from Q1 2011 (2011\_03) release*).
    
+   mol\_numaromaticrings(mol) : returns the number of aromatic rings in a molecule (*available from 2013\_03 release*).
    
+   mol\_numaliphaticrings(mol) : returns the number of aliphatic (at least one non-aromatic bond) rings in a molecule (*available from 2013\_03 release*).
    
+   mol\_numsaturatedrings(mol) : returns the number of saturated rings in a molecule (*available from 2013\_03 release*).
    
+   mol\_numaromaticheterocycles(mol) : returns the number of aromatic heterocycles in a molecule (*available from 2013\_03 release*).
    
+   mol\_numaliphaticheterocycles(mol) : returns the number of aliphatic (at least one non-aromatic bond) heterocycles in a molecule (*available from 2013\_03 release*).
    
+   mol\_numsaturatedheterocycles(mol) : returns the number of saturated heterocycles in a molecule (*available from 2013\_03 release*).
    
+   mol\_numaromaticcarbocycles(mol) : returns the number of aromatic carbocycles in a molecule (*available from 2013\_03 release*).
    
+   mol\_numaliphaticcarbocycles(mol) : returns the number of aliphatic (at least one non-aromatic bond) carbocycles in a molecule (*available from 2013\_03 release*).
    
+   mol\_numsaturatedcarbocycles(mol) : returns the number of saturated carbocycles in a molecule (*available from 2013\_03 release*).
    
+   mol\_numspiroatoms : returns the number of spiro atoms in a molecule (*available from 2015\_09 release*).
    
+   mol\_numbridgeheadatoms : returns the number of bridgehead atoms in a molecule (*available from 2015\_09 release*).
    
+   mol\_inchi(mol) : returns an InChI for the molecule. (*available from the 2011\_06 release, requires that the RDKit be built with InChI support*).
    
+   mol\_inchikey(mol) : returns an InChI key for the molecule. (*available from the 2011\_06 release, requires that the RDKit be built with InChI support*).
    
+   mol\_formula(mol,bool default false, bool default true) : returns a string with the molecular formula. The second argument controls whether isotope information is included in the formula; the third argument controls whether “D” and “T” are used instead of \[2H\] and \[3H\]. (*available from the 2014\_03 release*)
    
+   mol\_nm\_hash(mol,string default ‘’) : returns a string with a hash for the molecule. The second argument controls the hash type. Legal values are ‘AnonymousGraph’, ‘ElementGraph’, ‘CanonicalSmiles’, ‘MurckoScaffold’, ‘ExtendedMurcko’, ‘MolFormula’, ‘AtomBondCounts’, ‘DegreeVector’, ‘Mesomer’, ‘HetAtomTautomer’, ‘HetAtomProtomer’, ‘RedoxPair’, ‘Regioisomer’, ‘NetCharge’, ‘SmallWorldIndexBR’, ‘SmallWorldIndexBRL’, ‘ArthorSubstructureOrder\`. The default is ‘AnonymousGraph’.
    

##### Connectivity Descriptors[¶](#connectivity-descriptors "Link to this heading")

##### MCS[¶](#mcs "Link to this heading")

#### Other[¶](#other "Link to this heading")

There are additional functions defined in the cartridge, but these are used for internal purposes.

## Using the Cartridge from Python[¶](#using-the-cartridge-from-python "Link to this heading")

The recommended adapter for connecting to postgresql is pyscopg2 ([https://pypi.python.org/pypi/psycopg2](https://pypi.python.org/pypi/psycopg2)).

Here’s an example of connecting to our local copy of ChEMBL and doing a basic substructure search:

That returns a SMILES for each molecule. If you plan to do more work with the molecules after retrieving them, it is much more efficient to ask postgresql to give you the molecules in pickled form:

These pickles can then be converted into molecules:

## License[¶](#license "Link to this heading")

This document is copyright (C) 2013-2023 by Greg Landrum and other RDKit contributors.

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0 License. To view a copy of this license, visit [http://creativecommons.org/licenses/by-sa/4.0/](http://creativecommons.org/licenses/by-sa/4.0/) or send a letter to Creative Commons, 543 Howard Street, 5th Floor, San Francisco, California, 94105, USA.

The intent of this license is similar to that of the RDKit itself. In simple words: “Do whatever you want with it, but please give us some credit.”