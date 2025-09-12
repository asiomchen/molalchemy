## User Manual: PostgreSQL[¶](#user-manual-postgresql "Permalink to this headline")

## Basics[¶](#basics "Permalink to this headline")

### Data representation[¶](#data-representation "Permalink to this headline")

Bingo supports Daylight SMILES with some ChemAxon extensions and MDL (Symyx) Molfile/Rxnfile formats both in the text and binary representation. Please look at the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#data-representation) for details.

### Storage[¶](#storage "Permalink to this headline")

Suppose you have a table with a `text`, `varchar` or `bytea` column containing a Molfiles/Rxnfiles or SMILES with molecules or reactions.

Once you have prepared your table, you can execute `CheckMolecule` or `CheckReaction` to ensure that all the records are valid. These functions return not null string with invalid records corresponding error messages. All molecules or reactions that are in this table will be excluded from the chemical index. You can update these molecules later after indexing.

After you have prepared and checked your table, you can execute `Create Index` to make Bingo search procedures available for you table. The more records the table contains, the longer it takes to create an index.

### Queries[¶](#queries "Permalink to this headline")

You can specify the query molecule as a `varchar` string containing a Molfile (including various query features), a SMILES, or a SMARTS string. For reaction queries, use Rxnfiles, reaction SMILES, or reaction SMARTS.

## Molecules[¶](#molecules "Permalink to this headline")

### Creating an Index[¶](#creating-an-index "Permalink to this headline")

The following command creates the index for text column:

The following command creates the index for bytea (binary) column:

### Updating and Dropping Index[¶](#updating-and-dropping-index "Permalink to this headline")

You can add, remove, or edit records in the table after the index is created. Adding records does not slow down the queries, i.e. the performance will be the same as if you had indexed the whole table at once. No re- indexing is required after adding the records.

After you delete, you must call `autovacuum` utility functions to clean up the index.

### Substructure Search[¶](#substructure-search "Permalink to this headline")

The general form of substructure search query is as follows:

Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#substructure-search) to learn the rules of Bingo substructure matching (including Resonance search, Conformation search, Affine transformation search), and various query features available.

### SMARTS Search[¶](#smarts-search "Permalink to this headline")

The syntax of SMARTS expression search is similar to the ordinary substructure search:

Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#smarts-search) to learn the rules of SMARTS matching in Bingo.

### Exact Search[¶](#exact-search "Permalink to this headline")

The general form of exact search query is as follows:

Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#exact-search) to learn the rules of Bingo exact matching and various flags available for `$parameters` string.

### Tautomer Search[¶](#tautomer-search "Permalink to this headline")

Tautomer search is implemented within Substructure and Exact search functions, and requires `TAU` flag to be specified in `$parameters` string. Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#tautomer-search) to learn the rules of Bingo exact and substructure tautomer matching.

#### Customizing the Rules[¶](#customizing-the-rules "Permalink to this headline")

Your database (to which you have installed Bingo) contains a table called `bingo.bingo_tau_config`. By default it contains 3 records with predefined rules. You can add, remove, or update the defined rules. Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#tautomer-search) to learn the format of the tautomer matching rules.

### Similarity Search[¶](#similarity-search "Permalink to this headline")

The general form of similarity search query is as follows:

By default, the bottom limit is zero and the top limit is 1, which is the maximum possible value of similarity. You can specify `null` in place of `$bottom` or `$top` to disable the lower or upper bound. In most cases, you may want to cancel the upper bound:

Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#similarity-search) to learn more about the metrics.

### Gross Formula Search[¶](#gross-formula-search "Permalink to this headline")

The general form of gross formula search query is as follows:

Please see the corresponding section of the [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#gross-formula-search) to see some examples.

### Molecular Weight Search[¶](#molecular-weight-search "Permalink to this headline")

The general form of molecular weight query is as follows:

To use the bingo index the search query is:

### Format Conversion[¶](#format-conversion "Permalink to this headline")

You can convert a molecule to SMILES string using the function:

You can convert a molecule to Molfile using the function:

The automatic layout procedure is performed to calculate the 2D coordinates of the resulting molecule.

You can convert a molecule to CML format using the function:

### Conversion to Binary Format[¶](#conversion-to-binary-format "Permalink to this headline")

The `bingo.CompactMolecule()` operator can be used for converting Molfiles and SMILES to the internal binary format. The operator works equally well with `text` and `bytea` operands. The operator always returns the `bytea` result.

The `$xyz` parameter must be 0 or 1. If it is 1, the positions of atoms are saved to the binary format. If it is zero, the positions are skipped.

#### Canonical SMILES computation[¶](#canonical-smiles-computation "Permalink to this headline")

You can use the function:

to generate canonical SMILES strings for molecules represented as Molfiles or SMILES strings. Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#canonical-smiles) to learn the benefits of Bingo canonical SMILES format.

### Molecule Fingerprints[¶](#molecule-fingerprints "Permalink to this headline")

You can generate a molecule fingerprint via `bingo.Fingerprint` function. The syntax is the same as for Bingo for Oracle, and it is described [in this section](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#molecule-fingerprints).

### InChI and InChIKey[¶](#inchi-and-inchikey "Permalink to this headline")

You can use `bingo.InChI` and `bingo.InChIKey` function to get InChI and InChIKey strings. The syntax is the same as for Bingo for Oracle, and it is described [in this section](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#inchi-and-inchikey).

## Reactions[¶](#reactions "Permalink to this headline")

### Creating an Index[¶](#id1 "Permalink to this headline")

The following command creates the index for text columns:

The following command creates the index for bytea (binary) columns:

### Reaction Substructure Search[¶](#reaction-substructure-search "Permalink to this headline")

The general form of reaction substructure search query is as follows:

Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#substructure-search-1) to learn the rules of Bingo reaction substructure matching and various query features available.

### Reaction SMARTS Search[¶](#reaction-smarts-search "Permalink to this headline")

The syntax of SMARTS expression search is similar to the ordinary substructure search:

Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#smarts-search-1) to learn the rules of SMARTS matching in Bingo.

### Reaction Exact Search[¶](#reaction-exact-search "Permalink to this headline")

The general form of exact search query is as follows:

Please see the corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#exact-search-1) to learn the rules of Bingo exact matching and various flags available for `$parameters` string.

### Automatic Atom-to-Atom mapping[¶](#automatic-atom-to-atom-mapping "Permalink to this headline")

You can compute reaction AAM by calling the function:

The corresponding section of [Bingo User Manual for Oracle](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#automatic-atom-to-atom-mapping) describes the allowable values of the `$strategy` parameter and shows some examples.

### Format Conversion[¶](#id2 "Permalink to this headline")

You can convert a reaction to reaction SMILES string using the function:

You can convert a reaction SMILES string to Rxnfile using the function:

The automatic layout procedure is performed to calculate the 2D coordinates of the resulting reaction.

You can convert a reaction to a reaction CML using the function:

### Conversion to binary format[¶](#id3 "Permalink to this headline")

The `Bingo.CompactReaction()` operator can be used for converting Rxnfiles and reaction SMILES to internal binary format. The operator works equally well with `text` and `bytea` operands. The operator always returns the `bytea` result.

The `$xyz` parameter must be 0 or 1. If it is 1, the positions of atoms are saved to the binary format. If it is zero, the positions are skipped.

### Reaction Fingerprints[¶](#reaction-fingerprints "Permalink to this headline")

You can generate a reaction fingerprint via `bingo.RFingeprint` function. The syntax is the same as for Bingo for Oracle, and it is described [in this section](https://lifescience.opensource.epam.com/bingo/user-manual-oracle.html#reaction-fingerprints).

## Importing and Exporting Data[¶](#importing-and-exporting-data "Permalink to this headline")

### Importing SDFiles, RDFiles and SMILES[¶](#importing-sdfiles-rdfiles-and-smiles "Permalink to this headline")

You can import a molecule or reaction table from an SDF file. You can also import SDF fields corresponding to each record in the SDF file. Prior to importing, you have to create the table manually:

A simple example of importing the [NCI](http://dtp.nci.nih.gov/docs/3d_database/Structural_information/structural_data.html) 2D compound database would be the following:

Importing RDF files is done with `ImportRDF()` function the same way as SDF files:

Importing multi-line molecule or reaction SMILES file is done the similar way with the `ImportSMILES()` function:

**Note:** When you import the file contents to a table, the old table contents are not removed. Thus, you can import multiple files into the same table.

### Exporting SDFiles and RDFiles[¶](#exporting-sdfiles-and-rdfiles "Permalink to this headline")

You can export a molecule table to a SDF file. You can also export table fields corresponding to each record in the SDF file:

A simple example of exporting the [NCI](http://dtp.nci.nih.gov/docs/3d_database/Structural_information/structural_data.html) 2D compound database would be the following:

Exporting RDF files is done with `ExportRDF()` function the same way as SDF files:

## Utility functions[¶](#utility-functions "Permalink to this headline")

### Extracting Names[¶](#extracting-names "Permalink to this headline")

`bingo.getName` function extracts the molecule or reaction name from Molfile, Rxnfile, or SMILES string.

### Calculating Molecule Properties[¶](#calculating-molecule-properties "Permalink to this headline")

`bingo.getMass` function returns the molecular weight of the given molecule, represented as a Molfile or SMILES string. It has an additional parameter which defines the ‘kind’ of the resulting molecular mass value.

Here are some examples of using the `Bingo.getMass()` operator:

Similarly, `bingo.Gross()` function returns the gross formula of the given molecule

### Checking for Correctness[¶](#checking-for-correctness "Permalink to this headline")

You can use the `bingo.CheckMolecule()` function to check that molecules are presented in acceptable form. If the molecule has some problems (unsupported format, exceeded valence, incorrect stereochemistry), the functions returns a string with the description of the problem. Is the molecule is represented with a correct Molfile or SMILES string, the function returns `null`.

Similarly, you can check reactions for correctness with the `bingo.CheckReaction()` function:

### Reading Files on Server[¶](#reading-files-on-server "Permalink to this headline")

The `Bingo.FileToText()` function accepts a text file path and loads a file from the server file system to PostgreSQL text.

Usually you may want to load the query molecule in the following way:

The `Bingo.FileToBlob()` function accepts a text file path and loads a file from the server file system to PostgreSQL bytea.

## Permissions management[¶](#permissions-management "Permalink to this headline")

Let the schema name **bingo** was specified during installation of the Bingo cartridge. Let the user **test\_user** is going to create the bingo index on a table. There are two objects user will work with to create the bingo index.

So for precise permissions management you need:

### Set permissions for building the index[¶](#set-permissions-for-building-the-index "Permalink to this headline")

## Maintenance[¶](#maintenance "Permalink to this headline")

### Obtaining Bingo Version Number[¶](#obtaining-bingo-version-number "Permalink to this headline")

### Viewing the Log File[¶](#viewing-the-log-file "Permalink to this headline")

All operation of Bingo is logged into the PostgreSQL native LOG. All error and warning messages (not necessarily visible in SQL session) are logged. Some performance measures of the SQL queries are written to the log as well.