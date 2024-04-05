# SpellVar

This is a program that is meant to allow you to create an manage your own lists of spelling variances, phrases and mistakes, categorize them by region and analyze given text against your list of variances.

Variances can be added one at a time or in bulk using a CSV file. The variances should include a word or phrase, and a region that word or phrase belongs to.

All variations are stored in a SQL Lite 3 database in the same file as the main.py file. The database is named spelling_variances.db by default.
