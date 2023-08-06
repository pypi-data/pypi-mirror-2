===========================
Ygrep - Grep for Yaml files
===========================

Ygrep is a simple utility that does a Grep-like match to Yaml files. It
understands Yaml hierarchy and shows, for each match, the matching scalar
node along with its descendants and ancestors, effectively cropping the yaml
tree.

For example, given the following Yaml tree::

    invoice: 34843
    date: 2001-01-23
    bill-to: &id001
      given: Chris
      family: Dumars
      address:
        lines: |
          458 Walkman Dr.
          Suite #292
        city: Royal Oak
        state: MI
        postal: 48046

A match for "address" would write::

    bill-to:
      address:
        lines: |
          458 Walkman Dr.
          Suite #292
        city: Royal Oak
        state: MI
        postal: 48046

