# provreq-mcmc

This is an extension to the base AEP project, attempting to find the most likely path to one or more techniques using markov chain montecarlo simulations.

Use case is "you have observed X; how did this happen?"

It is developed as part of the [Cyberhunt Project](https://www.mn.uio.no/ifi/english/research/projects/cyberhunt/)

## install

Currently in active development and should be installed from the github repository

```bash
mkdir src; cd src
mkdir provreq-mcmc-data; cd provreq-mcmc-data; wget wget https://github.com/pan-unit42/playbook_viewer/archive/master.zip; cd ..
git clone https://github.com/mnemonic-no/provreq-mcmc.git
git clone https://github.com/mnemonic-no/provreq-data.git
cd provreq-mcmc
python3 -m pip install -e .
```

## Usage example

### Create the stats file

```bash
provreq-mcmc-create-stats --data-dir ~/src/provreq-data/data --provreq-data ~/src/provreq-data/data/threatactors/ --u42-data ~/src/provreq-mcmc-data/master.zip -o ~/src/provreq-mcmc-data/stats.json
```

### Run the tool searching for paths to technique

#### Example for "Lateral Tool Transfer"

```


## What does automation mean for risk management?

The main goal of the research project is to semi-automate the digital risk management process, in order to find new methods for analysis of relevant and available security data. The project also aims to improve the understanding of risk among decision-makers by finding new methods for presenting risk information.

## Contribution

See [CONTRIBUTING.md](CONTRIBUTING.md)

## State of code/Build instruction

This is a repository for collaboration on a research project. The state of the code constantly change during the project. The code should not be used unless clearly marked as ready for production.

Questions regarding the code can be directed at mss_r_d@mnemonic.no

## License

[ISC License](LICENSE)
