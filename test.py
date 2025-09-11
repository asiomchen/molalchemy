import datamol as dm

# convert smiles to smarts
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"
smarts = dm.to_smarts(dm.to_mol(smiles))
print("smarts:", smarts)