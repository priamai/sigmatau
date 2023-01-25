# SigmaTau

## Introduction

Security operation teams have a hard time managing alert volumes and tracking the quality 
of signature detections over time.
The quality of signature and ML based systems can be assessed with a solid mathematical 
framework from 
the field of data science and machine learning.

This standard is an extension to the excellent work of [Sigma](https://github.com/SigmaHQ/sigma) 
which enables security teams to include performance metrics in their signature database.

## Metrics
The metrics available are based on the confusiong matrix for binary classifiers.
This relies on the confusion matrix and derived measures: precision, recall, f-measure.

## Schema
The schema is implemented as a pydantic model on YML files.

## Author:

Priam AI Cyber ltd.
[Website](https://priam.ai)





