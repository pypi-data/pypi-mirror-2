# -*- coding:utf8 -*-

Usage
=====

>>> from hangul import translit
>>> translit.test()
한국                    --> han-guk
한국어                  --> han-gugeo
저작권                  --> cheojakkweon
저작                   --> cheojak
작심삼일                 --> chaksimsamil
밧줄                   --> patchul

>>> s = translit.romanize('한국어')
>>> print s
han-gugeo
>>>
>>> s = translit.romanize('안녕하세요!')
>>> print s
annyeonghaseyo!