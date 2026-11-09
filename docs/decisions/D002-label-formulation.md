---
id: D002
title: Label formulation (multi-label vs single label)
status: open
date: 2026-11-09
decided_by: ""
owner: Guidelines & quality track
changes_proposal: false
follow_up:
  - Run the pilot with question-based multi-label annotation (guidelines v0)
  - Measure share of segments with 2+ labels and per-label agreement, then decide
  - Compare with prior work (ViClaim multi-label; CheckThat! check-worthiness)
---
## Question
Does each segment get any subset of {check-worthy claim, non-check-worthy claim, opinion} (multi-label, proposal Table 3), or exactly one of four labels including "other" (single label, as proposal §6.1 reads)?

## Status
Not decided. The supervisor asked for practical testing or a comparison with earlier projects first.

## Proposal for the pilot (not a decision)
Annotate with four yes/no questions (guidelines v0). This captures multi-label data; a single-label view can be derived later with a precedence rule, but not the reverse. Full comparison: Drive file 02, Part 3.
