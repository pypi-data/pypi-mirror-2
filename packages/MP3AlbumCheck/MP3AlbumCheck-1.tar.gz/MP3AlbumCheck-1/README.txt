# MP3AlbumCheck

* * *

## What is it?

MP3AlbumCheck is a Python package that contains a small [FreeDB][1]/CDDB interface class and a CLI wrapper to tag MP3 files.

## Why?

Like most people, I store my digital albums in MP3 format and in individual folders. I like to be able to confirm and validate that the album matches the CD equivilent.

## How it Works

MP3AlbumCheck takes a directory of MP3s, calculates the CDDB ID and checks the FreeDB database to see if there is a match. If there is, the choice(s) are displayed. You then have the ability to re-tag your album with the information retrieved from FreeDB: 
    
    $ mp3albumcheck
    A mandatory option is missing
    
    Usage: mp3albumcheck [options]
    
    Options:
    -h, --help         show this help message and exit
    -t, --tag          tag results
    -d DIR, --dir=DIR  directory of mp3s
    
    
    $ mp3albumcheck -d Mad\ Professor\ -\ No\ Protection -t
    Found  9  results for 680bb108:
      [1]  730b9d08   Massive Attack / No Protection
      [2]  680bb308   Massive Attack Vs. Mad Professor / No Protection
      [3]  6f0bb308   Massive Attack Vs. Mad Professor / No Protection
      [4]  6f0bb308   Massive Attack / No Protection
      [5]  6f0bb308   Massive Attack / No Protection
      [6]  6e0bb308   Massive Attack / No Protection
      [7]  6f0bb408   Massive Attack / No Protection: Massive Attack Vs. Mad Professor
      [8]  6f0bb408   Massive Attack / No Protection: Massive Attack vs. Mad Professor
      [9]  6e0bba08   Desconocido / Desconocido
    Pick a result (-1 to exit): 2
    Radiation Ruling The Nation (Protection)
    Bumper Ball Dub (Karmacoma)
    Trinity Dub (Three)
    Cool Monsoon (Weather Storm)
    Eternal Feedback (Sly)
    Moving Dub (Better Things)
    I Spy (Spying Glass)
    Backward Sucking (Heat Miser)
    Tag? y/n: y
    

## Requirements

*   [eyeD3][2]

## Installation

### Pip

    $ pip install MP3AlbumCheck

### Source

    $ tar xzvf MP3AlbumCheck-1dev.tar.gz
    $ cd MP3AlbumCheck
    $ python setup.py install
    

## Support, Bugs, and Questions

Please contact [Joe Topjian][3].

 [1]: http://www.freedb.org/
 [2]: http://eyed3.nicfit.net/
 [3]: http://terrarum.net/contact.html
