# frs

This contains a Python package for managing conversions of Family Resources Survey data into OpenFisca-UK compatible (entity-level) datasets. There are two main direct uses:

- Use the ```frs``` command to manage FRS datasets stored locally
- Import the package and use the ```frs.load()``` function to return the generated datasets

## Command-line Tool

Instructions for usage:

```
usage: frs [-h] [--path PATH] {status,gen,regen}

Utility for managing Family Resources Survey microdata

positional arguments:
  {status,gen,regen}  The action to take on stored data

optional arguments:
  -h, --help          show this help message and exit
  --path PATH         The path to the FRS data
```

### Viewing status

```frs status``` prints out a summary of the status of the stored datasets. For example, when newly installed, it should output:

```
FRS status:
        FRS TAB files stored?                           No
        FRS OpenFisca-UK input files generated?         No
        OpenFisca-UK input files outdated?              N/A
```

When FRS data is loaded with ```frs gen```, it should output:

```
FRS status:
        FRS TAB files stored?                           Yes
        FRS OpenFisca-UK input files generated?         Yes
        OpenFisca-UK input files outdated?              No (files generated with current version, 0.2.0)
```

### Generating datasets

Run ```frs gen --path [PATH_TO_FRS_TAB_FILES]``` to generate the input datasets. The output should look like this:

```
Storing FRS files: 100%|██████████████████████████████████████████████████████████████████████| 23/23 [00:00<00:00, 97.44it/s]
Stored FRS source files successfully.
Generating OpenFisca-UK input datasets:
Reading adult.tab: 33238it [00:02, 11676.03it/s]
Reading benunit.tab: 22406it [00:00, 31335.18it/s]
Reading child.tab: 9849it [00:00, 33614.09it/s]
Reading job.tab: 20494it [00:00, 33871.75it/s]
Reading pension.tab: 10248it [00:00, 120552.48it/s]
Reading benefits.tab: 38475it [00:00, 83630.24it/s]
Reading accounts.tab: 65391it [00:00, 225508.67it/s]
Reading assets.tab: 18432it [00:00, 198199.28it/s]
Reading maint.tab: 438it [00:00, 109534.05it/s]
Reading chldcare.tab: 7285it [00:00, 145566.87it/s]
Writing person.csv file: 100%|███████████████████████████████████████████████████████| 43087/43087 [00:00<00:00, 59506.24it/s] 
Reading extchild.tab: 778it [00:00, 194699.79it/s]
Writing benunit.csv file: 100%|█████████████████████████████████████████████████████| 22406/22406 [00:00<00:00, 147388.99it/s] 
Reading househol.tab: 19169it [00:00, 23990.09it/s]
Writing household.csv file: 100%|███████████████████████████████████████████████████| 19169/19169 [00:00<00:00, 147383.17it/s]
```

## Importing FRS data

Importing entity-level datasets as DataFrames can be done with:

```
import frs
person_df, benunit_df, household_df = frs.load()
```

Note that ```frs.load()``` will raise an exception if the data has not been generated.