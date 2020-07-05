# Donate
![.github/workflows/ci.yml](https://github.com/JimMadge/donate/workflows/.github/workflows/ci.yml/badge.svg)

Generate donations to projects you want to support according to a distribution
you control.

## About
### The Problem

I want to donate to many (mostly software) projects which I like, use or depend
on. This creates a tension between what donation strategy would suit me and what
would suit those projects.

Because there are many projects, if I regularly donate a reasonable amount to
each I will be spending more money than I am comfortable with. However, if I
split the amount I am comfortable with between all the projects then each will
receive a tiny amount and loose (proportionally) more of my contributions
through payment-service and currency transactions fees. Also, I may value some
projects more than others and want them to receive a greater share.

### A Possible Solution

Donate lets the user set,

1. The total amount they want to regularly donate
1. How many projects this will be split between (and hence the individual
   donation amount)
1. A collection of recipients with a weighting to favour their favourite or most
   important projects

This ensure that the user can donate an amount they are happy with, weighted
as they like and that the individual donations will be significant.

### New Problems

This system is certainly not perfect. Here are some problems I can see,

- Making donations requires discipline and manual intervention, unlike services
  like [Liberapay](https://liberapay.com/)
- The amounts and regularity at which projects will receive donations is
  unpredictable which could make their financial planning more difficult

## Installation
### User Install Using Pip

Clone the repository
```
$ git clone https://github.com/JimMadge/donate.git
```
Install using pip
```
$ cd doante
$ pip install --user .
```
Ensure `~/.local/bin` is in your `$PATH`.

## Usage
### Configuration

Donate needs to be configured before use Donate is configured with a single
[YAML](https://yaml.org/) file. This files path should be
`$XDG_CONFIG_HOME/donate/config.yml` (generally `~/.config/donate/config.yml`).

The configuration file has the following top level keys

| key                | description                                        | required | default  |
| ---                | ---                                                | ---      | ---      |
| `total_donation`   | Total amount to donate                             | yes      |          |
| `split`            | How  many donees to split `total_donation` between | yes      |          |
| `schedule`         | Donation schedule, one of `ad hoc` and `monthly`   | no       | `ad hoc` |
| `currency_symbol`  | Symbol of the currency of `total_donation`         | no       | `£`      |
| `decimal_currency` | Whether the currency can be split into hundredths  | no       | `false`  |
| `donees`           | List of donees                                     | yes      |          |

Each donee requires the following keys

| key      | description                                                                                                                |
| ---      | ---                                                                                                                        |
| `name`   | Name of the donee                                                                                                          |
| `weight` | Relative weight of donation frequency to this donee, one of `critical`, `large`, `medium`, `small`, or an arbitrary number |
| `type`   | Type of donee, one of `software`, `distribution`, `service`, `podcast`, `organisation`, `charity` or `other`               |
| `url`    | Donation url of the donee                                                                                                  |

Here is a short example

```yaml
---
total_donation: 40
split: 8
schedule: monthly
currency_symbol: £
decimal_currency: true

donees:
  - name: Arch Linux
    weight: critical
    type: distribution
    url: https://www.archlinux.org/donate/
  - name: Kodi
    weight: 0.8
    type: software
    url: https://kodi.tv/contribute/donate
  - name: Python Software Foundation
    weight: large
    type: organisation
    url: https://www.python.org/psf/donations/
...
```

### Command Line

To generate a set of donations

```
$ donate
```

To see more command line options

```
$ donate -h
```
