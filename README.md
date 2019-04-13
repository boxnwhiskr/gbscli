# GreedyBandit CLI

[![Build Status](https://travis-ci.org/boxnwhiskr/gbscli.svg?branch=master)](https://travis-ci.org/boxnwhiskr/gbscli)
[![Python 3.4](https://img.shields.io/badge/python-3.4-blue.svg)](https://www.python.org/downloads/release/python-340/)
[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

GreedyBandit is a cloud-based A/B testing and optimization engine developed by Box and Whisker. **GreedyBandit CLI** is a command-line interface for GreedyBandit.

## Installation

The CLI supports Python 3.4 or higher. In most cases, you may use `pip` to
install the CLI:

    pip install gbscli

Run `gbs` to verify:

    gbs


## How to use

### Create an account and obtain the service credential

You must register a new account with your e-mail address:

    gbs account create "YOUR-EMAIL-ADDRESS" "YOUR NAME"

You will receive an e-mail containing a link to obtain the service credential.
Click the link and copy the content or use `curl` or `wget` to download the
credential.

Please note that the URL is temporary and won't work twice. If you want to get
another service credential, use the following command to get another link:

    gbs account credential "YOUR-EMAIL-ADDRESS"

Save the credential as a file and place it `~/.config/gbs/credential.json`. If
there is no such directory, you should create one.

Run the following command to check if the credential registered correctly:

    gbs account describe

### Services, experiments, and goals

A `service` represents a website or an app. A single account may have one or
more services. To see registered services run the following command:

    gbs service list

If you've just created new account, the command will show an empty list.

Each service may contain zero or more `experiment`s and `goal`s. Each
`experiment` represents independent A/B test session, and each `goal` represents
goals or objectives of the service such as new customer acquisition, purchase
completion, or reach to the target page.

In GreedyBandit, individual experiments don't contain goals. Instead, goals
belong to the service and **every single experiment in the service is evaluated
against every single goal.**  This separation of experiments and goals helps
you to avoid local optimizations caused by conflicting experiments.

### Configure experiments

Let's say your website is google.com, and you want to run an experiment to see
whether or not a new logo image leads to more purchases. First, you have to
create a new service and configure an experiment there:

    gbs service edit google-com

In the command above, `google-com` is a service ID. You may freely use any name
works for you. This command will open your default editor such as `vim` or
`emacs`, and you will see an empty configuration:

```json
{
  "experiments": [],
  "goals": []
}
```

In `experiments` array, add the following snippet:

```json
{
  "exp_id": "logo-image",
  "description": "Testing new logo image",
  "alpha": 0.05,
  "epsilon": 0.1,
  "start_dt": "2019-01-01T00:00:00+00:00",
  "end_dt": "2020-01-01T00:00:00+00:00",
  "paused": false,
  "selection_rate": 0.2,
  "target_segs": [],
  "ttl": 86400,
  "trial_pattern": "^https://google.com(/|/index\\.html)$",
  "variables": [
    {
      "var_id": "img",
      "values": ["new"]
    }
  ]
}
```

Let's see what each value means:

* `exp_id`: The ID of your experiment. This ID should be unique within the
  service.
* `description`: Short description of the experiment.
* `alpha`: A smoothing factor for exponential smoothing function used to update
  statistics such as `score`. GreedyBandit uses exponential smoothing functions
  to support long-running - possibly never-ending - experiments.
* `epsilon`: A constant for epsilon-Greedy multi-armed bandit algorithm. `0.1`
  means the engine will assign 10% of the incoming traffic to A/B testing and
  the other 90% of the traffic to exploit the currently best performing *arm*.
* `start_dt`: Start date of the experiment. You may omit this field to start
  the experiment immediatly.
* `end_dt`: End date of the experiment. You may omit this field to run the
  experiment forever.
* `pause`: Set this field `true` to temporarily pause the experiment.
* `selection_rate`: Specify sampling rate. `0.2` means that the 20% of the
  entire visitors will be allocated to the experiment.
* `target_segs`: A list of tags to specify a target user segment. Only users
  bearing matching tags will be allocated to the experiment.
* `ttl`: Time-to-live of the allocation. Once a user has assigned to a specific
  *arm*, this assignment will be retained for TTL seconds. After the period,
  the GreedyBandit engine will try to reassign the user to optimize
  exploit-explore ratio. The value `86400` is `24 * 60 * 60`, which means a day.
* `trial_pattern`: A regular expression pattern to detect *trial* logs. Any
  visit to pages with matching URLs are regarded as exposures to the trial. 
* `variables`: A list of variables and their values. For conventional A/B test,
  there will be a single variable with one or more values. For multi-variate
  test, there will be two or more variables. Every variable has an implicit
  value called `_DEFAULT`. As a result, in the configuration above, the variable
  `img` have two values: `_DEFAULT` and `new`.

Save and quit the editor to apply the changes.

### Configure goals

Now, it's time to register a new goal for your website. Goals are defined for
the entire website, not for an specific experiment. **Every single experiment in
the service is evaluated against every single goal.**

Let's edit the service configuration again to add the goal:

    gbs service edit google-com

In `goals` array, add the following snippet:

```json
{
  "goal_id": "purchase",
  "description": "Product purchase",
  "goal_patterns": [
    {
      "pattern": "^https://google\\.com/purchase_complete$",
      "reward": 100
    }
  ]
}
```

Let's see what each value means:

* `goal_id`: The ID of the goal.
* `description`: A short description of the goal.
* `goal_patterns`: A list of goal patterns and default reward amount of the
  goal. `pattern` is a regular expression pattern to detect *reward* logs. Any
  visit to pages with matching URLs are regarded as success of the trial. If the
  log contains `reward` field, this value will override the default `reward`
  amount specified in the configuration.

Save and exit the editor to apply changes.

### Apply experiments to the service using SDK

Since you've just created the service configuration with one experiment and a
single goal, you are ready to apply the experiment to your website. You need
a `public_token` to connect your client code to the service configuration:

    gbs service describe google-com

Copy the value of `public_token` and it's all done.

Now you have to apply experiments to your service using GreedyBandit service's
Javascript SDK. Please visit the
[SDK's homepage](https://github.com/boxnwhiskr/gbsdk-js) to see the instruction.

If your service is not a website, you should use HTTP API directly:

* Use [Collecting API](https://api.greedybandit.com/ui/#/collect) to send logs
* Use [Assignment API](https://api.greedybandit.com/ui/#/assignment) to get the
  assignment table.

### Monitor the performance on-going experiments

GreedyBandit keeps three set of statistics for each experiment:

* Arms statistics: TODO
* Segments statistics: TOdo
* Goals statistics: TODO

Current snapshots vs. time-series data:

* TODO

## Concepts

* Service: TODO
* Experiment: TODO
* Goal: TODO
* Variable and value: TODO
* Arm: TODO
* Multi-armed bandit problem: TODO
* epsilon-Greedy algorithm: TODO
* Exponential smoothing: TODO

## Development

Setting up virtual environment:

    pyenv virtualenv 3.7.3 gbs-gbscli
    pip install -e .

Unit testing:

    ptw

To run tox:

    pyenv install 3.7.3
    pyenv install 3.6.8
    pyenv install 3.5.7
    pyenv install 3.4.9
    pyenv local 3.7.3 3.6.8 3.5.7 3.4.9
    tox
