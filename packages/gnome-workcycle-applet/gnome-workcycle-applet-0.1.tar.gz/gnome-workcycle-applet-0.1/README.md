# gnome-workcycle-applet

## Overview

This applet reminds you to make breaks when working.
The work and fun/relax times can be changed to personal preference.

Here is a quick video demo: [Link](http://www.youtube.com/watch?v=ktSs1kuROhQ)


## Requirements (Ubuntu Linux)

- python-gconf

- python-gnome2

- python-gnomeapplet

- python-gobject

- python-gtk2

- python-notify

I hope I didn´t forget some.

## Installation instructions (Ubuntu linux with pip)

- `sudo pip install gnome-workcycle-applet`

- Restart your gnome session

- Add the Workcycle applet to your panel

- Set your desired times in the preferences


## Installation instructions (Ubuntu linux with easy_install/setuptools)

- `sudo easy_install gnome-workcycle-applet`

- Restart your gnome session

- Add the Workcycle applet to your panel

- Set your desired times in the preferences

## Installation instructions (Ubuntu Linux without easy_install/pip)

- [Download](http://github.com/downloads/daddz/gnome-workcycle-applet/gnome-workcycle-applet-0.1.tar.gz) tarball

- `sudo python setup.py install`

- Restart your gnome session

- Add the Workcycle applet to your panel

- Set your desired times in the preferences


I only tested this on Ubuntu but it should work without problems on other distributions.


## Usage

- Click to start the work timer

- Click again to switch to the fun timer immediately

- Rightclick and hit 'Stop' to stop it completely

## Features

- Automatically switches from worktime to funtime and vice versa

- Adjustable times

- Notifications

## Planned

- Sound notification

- Funny comments for the notifications

- ??

## About

I had the idea for this project after reading [this](http://www.reddit.com/r/programming/comments/e3you/life_hack_the_3030_minute_work_cycle_feels_like/) article I found on reddit.
It´s my first ever python project - _I never touched python before_ - so the code might be unclean und messy (suggestions are welcome).
Also I´m not sure about how the python packets get distributed. I hope I got it right with the `setup.py` (again suggestions welcome).

## Thanks

Thanks to the few people who already used python for gnome applets and made their source available or have written blog posts.
Without your sources I would have never finished this applet.


