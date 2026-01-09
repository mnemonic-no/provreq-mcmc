# provreq-mcmc

This is an extension to the base provreq project, attempting to find the most likely path to one or more techniques using markov chain montecarlo simulations.

Use case is "you have observed X; how did this happen?"

It is developed as part of the [Cyberhunt Project](https://www.mn.uio.no/ifi/english/research/projects/cyberhunt/)

## install

Currently in active development and should be installed from the github repository

```bash
mkdir src; cd src
mkdir provreq-mcmc-data; cd provreq-mcmc-data; wget https://github.com/pan-unit42/playbook_viewer/archive/master.zip; cd ..
git clone https://github.com/mnemonic-no/provreq-mcmc.git
git clone https://github.com/mnemonic-no/aep.git
cd provreq-mcmc
python3 -m pip install -e .
```

## Usage example

### Create the stats file

```bash
provreq-mcmc-create-stats --data-dir ~/src/aep/data --provreq-data ~/src/aep/data/threatactors/ --u42-data ~/src/provreq-mcmc-data/master.zip -o ~/src/provreq-mcmc-data/stats.json
```

### Run the tool searching for paths to technique

#### Example for "Lateral Tool Transfer"

```bash
[~] provreq-mcmc-montecarlo --top 3 --seed-class "Resource Development,Reconnaissance" -a children --seeds waterhole --agents T1570 --data-dir ~/src/aep/data --promise-descriptions ~/src/aep/data/promise_descriptions.csv -s ~/src/provreq-mcmc-data/stats.json
Using T1583
Using T1584
Using T1585
Using T1586
Using T1587
Using T1588
Using T1589
Using T1590
Using T1591
Using T1592
Using T1593
Using T1594
Using T1595
Using T1596
Using T1597
Using T1598
Using T1608
Using T1583.001
Using T1583.002
Using T1583.003
Using T1583.004
Using T1583.005
Using T1583.006
Using T1583.007
Using T1584.001
Using T1584.002
Using T1584.003
Using T1584.004
Using T1584.005
Using T1584.006
Using T1584.007
Using T1585.001
Using T1585.002
Using T1585.003
Using T1586.001
Using T1586.002
Using T1586.003
Using T1587.001
Using T1587.002
Using T1587.003
Using T1587.004
Using T1588.001
Using T1588.002
Using T1588.003
Using T1588.004
Using T1588.005
Using T1588.006
Using T1589.001
Using T1589.002
Using T1589.003
Using T1590.001
Using T1590.002
Using T1590.003
Using T1590.004
Using T1590.005
Using T1590.006
Using T1591.001
Using T1591.002
Using T1591.003
Using T1591.004
Using T1592.001
Using T1592.002
Using T1592.003
Using T1592.004
Using T1593.001
Using T1593.002
Using T1593.003
Using T1595.001
Using T1595.002
Using T1595.003
Using T1596.001
Using T1596.002
Using T1596.003
Using T1596.004
Using T1596.005
Using T1597.001
Using T1597.002
Using T1598.001
Using T1598.002
Using T1598.003
Skipping T1589_poor_security_practices
Skipping T1589_previous_compromise
Skipping T1591_poor_security_practices
Skipping T1593_poor_security_practices
Skipping T1594_poor_security_practices
Skipping T1597_previous_compromise
Skipping T1598_poor_security_practices
Skipping T1589.001_poor_security_practices
Skipping T1589.001_previous_compromise
Skipping T1589.002_poor_security_practices
Skipping T1589.002_previous_compromise
Skipping T1589.003_poor_security_practices
Skipping T1589.003_previous_compromise
Skipping T1591.001_poor_security_practices
Skipping T1591.002_poor_security_practices
Skipping T1591.003_poor_security_practices
Skipping T1591.004_poor_security_practices
Skipping T1593.001_poor_security_practices
Skipping T1593.002_poor_security_practices
Skipping T1593.003_poor_security_practices
Skipping T1597.001_previous_compromise
Skipping T1597.002_previous_compromise
Skipping T1598.001_poor_security_practices
Skipping T1598.002_poor_security_practices
Skipping T1598.003_poor_security_practices
Pre-seeding with {'info_network_services', 'infrastructure_botnet', 'infrastructure_domain', 'info_network_trust', 'tool_available', 'info_network_config', 'info_network_hosts', 'info_cloud_hosts', 'infrastructure_certificate', 'infrastructure_server', 'infrastructure_trusted_email_account', 'info_cloud_services', 'info_vulnerability', 'info_email_address', 'exploit_available', 'infrastructure_trusted_social_media', 'info_target_employee', 'info_network_shares', 'info_groupname', 'info_username'} from Reconnaissance and Resource Development agent_classs.
Simulating
done in 0:01:35.840656
Simulations ending due to missing requirements.. (stats for runs that did not complete)
╒═════════════════╤═════════╕
│ promise         │   count │
╞═════════════════╪═════════╡
│ access_physical │   14828 │
╘═════════════════╧═════════╛
Top choke points
╒═══════════════════════════════════════════════════════════════════════════════════════╤═════════╕
│ Agent                                                                                 │   Count │
╞═══════════════════════════════════════════════════════════════════════════════════════╪═════════╡
│ T1068: Exploitation for privilege escalation                                          │    8377 │
├───────────────────────────────────────────────────────────────────────────────────────┼─────────┤
│ T1003.003: OS Credential Dumping:NTDS                                                 │    7367 │
├───────────────────────────────────────────────────────────────────────────────────────┼─────────┤
│ T1562.001: Impair Defenses: Disable or Modify System Firewall:Disable or Modify Tools │    6242 │
├───────────────────────────────────────────────────────────────────────────────────────┼─────────┤
│ T1204.002: User Execution:Malicious File                                              │    5584 │
├───────────────────────────────────────────────────────────────────────────────────────┼─────────┤
│ T1571: Non-Standard Port                                                              │    5482 │
╘═══════════════════════════════════════════════════════════════════════════════════════╧═════════╛
Total number of potensial 'paths': 7861
Top 3
7.5% (n=7498)
╒═════════╤══════════════════════════════════════════════════╤════════════════════════════════════════════╤═════════════════════╕
│   stage │ agents                                           │ new promises @end-of-stage                 │ agent_classes       │
╞═════════╪══════════════════════════════════════════════════╪════════════════════════════════════════════╪═════════════════════╡
│       1 │ Phishing (Initial Access)                        │ credentials_user_domain                    │ Initial Access      │
│         │                                                  │ credentials_user_local                     │                     │
│         │                                                  │ tool_delivery                              │                     │
├─────────┼──────────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       2 │ User Execution (Execution)                       │ access_filesystem                          │ Execution           │
│         │                                                  │ access_memory                              │                     │
│         │                                                  │ code_executed                              │                     │
│         │                                                  │ privileges_user_local                      │                     │
├─────────┼──────────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       3 │ Application Layer Protocol (Command and Control) │ access_network                             │ Command and Control │
│         │ Command and Scripting Interpreter (Execution)    │ adversary_controlled_communication_channel │ Execution           │
│         │                                                  │ defense_evasion                            │                     │
│         │                                                  │ file_transfer                              │                     │
│         │                                                  │ persistence                                │                     │
├─────────┼──────────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       4 │ Lateral Tool Transfer (Lateral Movement) [*]     │                                            │ Lateral Movement    │
╘═════════╧══════════════════════════════════════════════════╧════════════════════════════════════════════╧═════════════════════╛
---
6.61% (n=6606)
╒═════════╤══════════════════════════════════════════════════╤════════════════════════════════════════════╤═════════════════════╕
│   stage │ agents                                           │ new promises @end-of-stage                 │ agent_classes       │
╞═════════╪══════════════════════════════════════════════════╪════════════════════════════════════════════╪═════════════════════╡
│       1 │ Phishing (Initial Access)                        │ credentials_user_domain                    │ Initial Access      │
│         │                                                  │ credentials_user_local                     │                     │
│         │                                                  │ tool_delivery                              │                     │
├─────────┼──────────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       2 │ User Execution (Execution)                       │ access_filesystem                          │ Execution           │
│         │                                                  │ access_memory                              │                     │
│         │                                                  │ code_executed                              │                     │
│         │                                                  │ privileges_user_local                      │                     │
├─────────┼──────────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       3 │ Application Layer Protocol (Command and Control) │ access_network                             │ Command and Control │
│         │                                                  │ adversary_controlled_communication_channel │                     │
│         │                                                  │ defense_evasion                            │                     │
│         │                                                  │ file_transfer                              │                     │
│         │                                                  │ persistence                                │                     │
├─────────┼──────────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       4 │ Lateral Tool Transfer (Lateral Movement) [*]     │                                            │ Lateral Movement    │
╘═════════╧══════════════════════════════════════════════════╧════════════════════════════════════════════╧═════════════════════╛
---
3.69% (n=3688)
╒═════════╤═══════════════════════════════════════════════╤════════════════════════════════════════════╤═════════════════════╕
│   stage │ agents                                        │ new promises @end-of-stage                 │ agent_classes       │
╞═════════╪═══════════════════════════════════════════════╪════════════════════════════════════════════╪═════════════════════╡
│       1 │ Phishing (Initial Access)                     │ credentials_user_domain                    │ Initial Access      │
│         │                                               │ credentials_user_local                     │                     │
│         │                                               │ tool_delivery                              │                     │
├─────────┼───────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       2 │ User Execution (Execution)                    │ access_filesystem                          │ Execution           │
│         │                                               │ access_memory                              │                     │
│         │                                               │ code_executed                              │                     │
│         │                                               │ privileges_user_local                      │                     │
├─────────┼───────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       3 │ Command and Scripting Interpreter (Execution) │ access_network                             │ Command and Control │
│         │ Non-Standard Port (Command and Control)       │ adversary_controlled_communication_channel │ Execution           │
│         │                                               │ defense_evasion                            │                     │
│         │                                               │ file_transfer                              │                     │
│         │                                               │ persistence                                │                     │
├─────────┼───────────────────────────────────────────────┼────────────────────────────────────────────┼─────────────────────┤
│       4 │ Lateral Tool Transfer (Lateral Movement) [*]  │                                            │ Lateral Movement    │
╘═════════╧═══════════════════════════════════════════════╧════════════════════════════════════════════╧═════════════════════╛
---
```


## What does automation mean for risk management?

The main goal of the research project is to semi-automate the digital risk management process, in order to find new methods for analysis of relevant and available security data. The project also aims to improve the understanding of risk among decision-makers by finding new methods for presenting risk information.

## Contribution

See [CONTRIBUTING.md](CONTRIBUTING.md)

## State of code/Build instruction

This is a repository for collaboration on a research project. The state of the code constantly change during the project. The code should not be used unless clearly marked as ready for production.

Questions regarding the code can be directed at opensource@mnemonic.no

## License

[ISC License](LICENSE)
