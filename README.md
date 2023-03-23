# SigmaTau

## Introduction

Security operation teams have a hard time managing alert volumes and tracking the quality 
of signature detections over time.
The quality of signature and ML based systems can be assessed with a solid mathematical 
framework from 
the field of data science and machine learning.

This standard is an extension to the excellent work of [Sigma](https://github.com/SigmaHQ/sigma) 
which enables security teams to include performance metrics in their signature database.

Please refer to the full paper on our [github](https://github.com/priamai/whitepapers/blob/main/2023/02/10/root_evil_fp.md) or [website](https://www.priam.ai/whitepaper).

## Installation
We have not published on pypi yet so for now.

```
git clone https://github.com/priamai/sigmatau
cd sigmatau
pip install .
```


## Metrics
The metrics available are based on the confusion matrix for binary classifiers.
This relies on the confusion matrix and derived measures: precision, recall, f-measure.

## Schema
The schema is implemented as a pydantic model on YML files.

## Example schema

The example below is the famous Mimikatz detection which contains a good list of false positive typical scenarios.
Below that you can find our field called *metrics* which reports the statistical performance of that signature in different 
anonymized environments represented by their id.

```
title: Mimikatz Use
id: 06d71506-7beb-4f22-8888-e2e5e2ca7fd8
status: experimental
description: This method detects mimikatz keywords in different Eventlogs (some of them only appear in older Mimikatz version that are however still used by different threat groups)
references:
    - https://tools.thehacker.recipes/mimikatz/modules
author: Florian Roth (rule), David ANDRE (additional keywords)
date: 2017/01/10
modified: 2022/01/05
tags:
    - attack.s0002
    - attack.lateral_movement
    - attack.credential_access
    - car.2013-07-001
    - car.2019-04-004
    - attack.t1003.002
    - attack.t1003.004
    - attack.t1003.001
    - attack.t1003.006
logsource:
    product: windows
detection:
    keywords:
        - 'dpapi::masterkey'
        - 'eo.oe.kiwi'
        - 'event::clear'
        - 'event::drop'
        - 'gentilkiwi.com'
        - 'kerberos::golden'
        - 'kerberos::ptc'
        - 'kerberos::ptt'
        - 'kerberos::tgt'
        - 'Kiwi Legit Printer'
        - 'lsadump::'
        - 'mimidrv.sys'
        - '\mimilib.dll'
        - 'misc::printnightmare'
        - 'misc::shadowcopies'
        - 'misc::skeleton'
        - 'privilege::backup'
        - 'privilege::debug'
        - 'privilege::driver'
        - 'sekurlsa::'
    filter:
        EventID: 15  # Sysmon's FileStream Events (could cause false positives when Sigma rules get copied on/to a system)
    condition: keywords and not filter
falsepositives:
    - Naughty administrators
    - AV Signature updates
    - Files with Mimikatz in their filename
metrics:
    version: 1.0
    signature_type: 'binary'
    reports:
        - id: '5d556e18-8f9d-4bee-8d5a-f4b557d8d295'
          matrix:
              tp: 0.1
              fp: 0.9
              fn: 0.0
              tn: 0.0
          derived:
              precision: 0.1
              recall: 1.0
              f1: 0.18
          format: ".2f"
          samples: 100

        - id: '5d556e18-8f9d-aabb-8d5a-f4b557d8d295'
          matrix:
              tp: 0.01
              fp: 0.0
              fn: 0.09
              tn: 0.0
          derived:
              precision: 1.0
              recall: 0.1
              f1: 0.18
          format: ".2f"
          samples: 20

        - id: '5d556e18-889d-aabb-8d5a-f4b557d8d295'
          matrix:
              tp: 0.1
              fp: 0.89
              fn: 0.0
              tn: 0.01
          derived:
              precision: 0.10
              recall: 1.0
              f1: 0.18
          format: ".2f"
          samples: 20

level: high

```

The matrix object represents:
* fp = false positive counts
* tp = true positive counts
* fn = false negative counts
* tn = true negative counts

The derived measures are:
* precision
* recall
* F1

The precision format is just a standard way to know the decimal points.

The sample field counts the total events for which the matrix was computed over a period of time.


## Usage
To validate a folder with tau signatures:
```
sigmatau-cli -folder ./tests/rules/tau -t
```

To validate a folder just with the standard sigma signatures:

```
sigmatau-cli -folder ./tests/rules/sigma -s
```


## Author:

Priam AI Cyber ltd.
[Website](https://priam.ai)





