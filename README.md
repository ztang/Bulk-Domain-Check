# Bulk Domain Check

Check bulk domain availability.

## Usage

Check domains:

    python check.py

Check domains with domain list from file:

    python check.py -f file_name

Help Info:

    python check.py -h

Enter your Domain Name Rule to bulk check domains

Domain Rules:
 - N: Number,
 - L: Letter,
 - A: Both number or letter.

e.g.,

 - NNN.com means 3-number .com domains,
 - NLL.cn means 1-number and 2-letter .cn domains,
 - NLN.me means 1-number, 1-letter and 1-number .me domains,
 - AAA.org means all 3-character(both number of letter) .org domains,

After input the domain rules, the script will generate and check all domains that match the rules.

This script support all tlds that has whois server.

Have fun!

If there is any issue please open a new issue, thank you.

## Dependency

 - Ubuntu >= 16.04LTS
 - Python 2.7

And whois tool from Ubuntu:

    sudo apt install whois

## Contact

mail@ztang.com

## Change Log

### [v1] - 2017-06-20

#### Added

 - time_out function
 - read domain list from file
 
#### Changed

 - check_available function
 
### [v0.1] - 2017-06-20

 - First version