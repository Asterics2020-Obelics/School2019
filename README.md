# 3rd ASTERICS-OBELICS International School


[![School indico](https://indico.in2p3.fr/event/18333/logo-1051603616.png)](https://indico.in2p3.fr/event/18333/)

This repository contains all the material needed for the [3rd
ASTERICS-OBELICS International
School](https://indico.in2p3.fr/event/18333/) on "Advanced software
programming for astrophysics and astroparticle physics".

# Table of contents

- [Install `git` and other tools](#git)
- [Get a copy of this repository with `git`](#repo)
- [Recommendation for Python install](#python)
    - [Linux](#linux)
    - [Mac](#mac)
    - [Windows](#windows)
    - [Library requirements](#req)
- [Having troubles?](#issues)
- [Jupyter](#jupyter)    
- [IDE: PyCharm](#pycharm)
- [Julia](#julia)
- [Chat room](#chat)
- [Tutors](#tutors)
- [Resources](#resources)


## Install git and other needed software <a name="git">

### Linux

1. Install required distribution packages :
    - Ubuntu: `sudo apt-get install -y git bzip2 wget`
    - Fedora 25: `sudo dnf install -y git wget bzip2`
    - CERN Scientific Linux 6: `sudo yum install -y git tar bzip2 wget`
    - CERN CentOS 7: `sudo yum install -y git bzip2 wget`
    - ARCH: `sudo pacman -S git bzip2 wget`

### Mac

Install git and other development tools by running

```
xcode-select --install
```


## Get a copy of this repository with `git` <a name="repo"></a>

Clone this repository on your personal computer.

      git clone https://github.com/Asterics2020-Obelics/School2019.git

You will need it before the school to install the different tools, and
during the school while attending the hands-on. For Windows, see [below](#windows).

## Recommendation for Python install <a name="python"></a>

You must install Python >=3.6 and a few Python libraries.
The recommended way to do so is to use [Anaconda](https://www.anaconda.com/distribution#download-section).
The procedure described below will help you install what is needed for the school.
If you already have Anaconda installed, you may skip to the [Library requirements section](#req).


### Linux <a name="linux"></a>

1. [Download](https://www.anaconda.com/distribution/#download-section)
the Linux `Anaconda` installer for Python 3.7.

1. Run the following command line in the directory with the file you downloaded:

```
bash Anaconda3-2018.12-Linux-x86_64.sh -b -p $HOME/.local/anaconda3
```

1. Edit your `.bashrc` to include the first or both of the following two lines  you `.bashrc`.
The first line should always be added and makes the `conda` command available.
The second command will make `anaconda` your default `python` in the shell,
you might want to leave it out, if you use another python installation regularly.

```
. "$HOME/.local/anaconda3/etc/profile.d/conda.sh"
conda activate
```

Set the correct path to your anaconda installation.
If you do not include the second command,
you need to run `conda activate` before using python for this workshop.

1. Close your current terminal window and open a new one after so the changes to the `.bashrc` can take effect

1. Install the [Requirements](#req)

### Mac <a name="mac"></a>

1. [Download](https://www.anaconda.com/distribution/#download-section)
the Mac `Anaconda` installer for Python 3.7.

1. Run the following command line in the directory with the file you downloaded:
```
bash Anaconda3-2018.12-MacOSX-x86_64.sh -b -p $HOME/.local/anaconda3
```

1. Edit your `~/.bash_profile` to include the first or both of the following two lines  you `~/.bash_profile`.
Create the file, if it does not exist.
The first line should always be added and makes the `conda` command available.
The second command will make `anaconda` your default `python` in the shell,
you might want to leave it out, if you use another python installation regularly.
```
. "$HOME/.local/anaconda3/etc/profile.d/conda.sh"
conda activate
```             
Set the correct path to your anaconda installation.
If you do not include the second command,
you need to run `conda activate` before using python for this workshop.

1. Close your current terminal window and open a new one after so the changes to the `.bash_profile` can take effect

1. Install the [Requirements](#req)

### Windows <a name="windows"></a>

There are two possibilities for Windows users:

1. If you have Windows 10 installed, then you can install WLS (Windows Linux Subsystem) which is an Ubuntu Linux distribution.
In this case, everything is done from the WSL terminal following the [Linux](#linux) instructions (for Ubuntu).

2. Alternatively, you can run the Windows Anaconda executable.
In this case please use the following instructions:

Instruction for Windows can be found [here](https://www.anaconda.com/distribution/#download-section) for the installation of Anaconda.
Once installed, you can run `Anaconda navigator`. To run Jupyter, on the main page of the Anaconda navigator,
click on `Launch` on the Jupyter notebook box.
This will open your favorite browser.
From there, you can either load a notebook (e.g. from the Git folder) or create a new notebook by clicking `new -> Python 3`.

When a `conda` command is required, run it from the `Anaconda prompt` terminal.

You can also install a Git tool for Windows: [Git for Windows](https://git-for-windows.github.io/).
Launch `Git GUI` or `Git bash` to get started.


## Library requirements <a name="req"></a>

We will use a common environment all along the school.
First of all, update conda to be able to use the latest features:
```
conda update conda
```
Windows users: run this command (and the followings) from the  `Anaconda prompt` terminal.

To create the environment, you just need to run the following command from the directory where you cloned this School2019 repository (since this repository contains the file `environment.yml`):

```
conda env create -f environment.yml
```

For the c++ tutorial,
we are going to need compiler tools.
For Linux and Windows with the WSL run
```
conda activate school19
conda install gcc_linux-64 gxx_linux-64 gfortran_linux-64
```

For macos we will just use the system compiler (`clang`).


If after the creation the file `environment.yml` was updated, you can update your installation with:
```
conda env update -f environment.yml
```

Once the environment has been created and all dependencies installed, you may activate it with (you will need to do that every time you want to use this environment):
```
conda activate school19
```

## Having troubles? <a name="issues"></a>

If you have any technical issue (e.g. regarding the install), first have a look at the [Issues](https://github.com/Asterics2020-Obelics/School2019/issues) tab and check that the issue has not been solved already (check the closed ones too). If not, please do open an issue (you will need a github account) for each question you may have before or during the school about software install and/or about one of the
classes.

You may also ask a question on [slack](#chat).


## Jupyter <a name="jupyter"></a>

To launch a Jupyter notebook, simply run the following command:

`jupyter notebook`

On Windows, see in the [above](#windows).

## IDE: PyCharm <a name="pycharm"></a>

We recommend to use pycharm, a full python IDE.
Free Community Edition: [Download PyCharm](https://www.jetbrains.com/pycharm/download) or opt for a free copy of the Professional Edition under [Student License](https://www.jetbrains.com/student/).

A more flexible text editor with good python integration is VS Code: https://code.visualstudio.com.

## Julia <a name="julia"></a>

There will be a short talk (in form of a live demonstration) on the [Julia Language](https://julialang.org). If you are interested and want to follow along, download the package here: https://julialang.org/downloads/

If you don't want to install anything but still eager to try Julia, you can spawn a Jupyter notebook on [JuliaBox](https://juliabox.com) for free.

## Chat rooms <a name="chat"></a>

[Slack chat rooms](https://obelics-school.slack.com/) are available before,
during and after the school (you should have received an email with an invitation).
If you need to talk to each other during a session, share information, ask questions, you can use the corresponding chat rooms to do so.
These chat rooms can also be used by the different tutors to give information or advices before or during the hands-on sessions.
You can also start one-to-one chat rooms.

Several channels are available, like *General* for all discussion/questions about the school, lectures, hands-on, etc.
There is also a channel *Social* to help you to get out together during the evening.

You can get the slack app directly on your phone: [Android](https://play.google.com/store/apps/details?id=com.Slack) or [Apple](https://itunes.apple.com/fr/app/slack/id618783545?mt=8). You can also get it for Windows, Mac, or Linux [here](https://slack.com).

## Tutors <a name="tutors"></a>

The full list of tutors is available [here](https://indico.in2p3.fr/event/18333/page/2038-list-of-tutors).


## Resources <a name="resources"></a>

See the [links file](LINKS.md)

- 2017 edition of the school: [program](https://indico.in2p3.fr/event/14227) and [github](https://github.com/Asterics2020-Obelics/School2017)

- 2018 edition of the school: [program](https://indico.in2p3.fr/event/16864/) and [github](https://github.com/Asterics2020-Obelics/School2018)

Complete Python tutorials:
 * [Python for Scientific Computing](http://bender.astro.sunysb.edu/classes/python-science/)
 * [A Whirlwind Tour of Python](https://github.com/jakevdp/WhirlwindTourOfPython)
 * [Python Data Science Handbook](https://github.com/jakevdp/PythonDataScienceHandbook)

 Workshops:
 * [Python for Astronomers and Particle Physicists](https://www.ice.csic.es/indico/event/5/overview) ([github](https://github.com/Python4AstronomersAndParticlePhysicists/PythonWorkshop-ICE))
