#!/bin/sh

# Just pipe your characters to this script. The characters should be separated
# by the pipe character.

tr '|' '\t' | sed 'a\\t' | tr '\n' '\t' | aeltei --calibrate
