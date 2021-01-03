# Top-level SaLt State - maps state modules to minions
########################################################################
#
# Compound matcher quick reference:
#
# G *   Grains glob
# E     PCRE minion ID
# P *   Grains PCRE
# L     List of minions
# I *   Pillar glob
# J *   Pillar PCRE
# S     Subnet/IP address
# R     Range cluster
#
# '*' Indicates an alternative delimiter to ':' may
# be specified between the letter and '@' character.

base:
  '*':
    #- system.swapfile
    #- system.packages
    - users
    - homeboy
    - nginx
    - postgres
    #- letsencrypt
    #- postgres
    #
    #
    #
