# GreedyBandit CLI

## Installation

The CLI supports Python 3.4 or higher. In most cases you may use `pip` to
install the CLI:

    pip install gbscli

Run `gbs` to verify:

    gbs


## How to use

### Create an account and obtain the service credential

You must register new account with your e-mail address:

    gbs account create "YOUR-EMAIL-ADDRESS" "YOUR NAME"

You will receive an e-mail containing a link to obtain the service credential.
Click the link and copy the content or use `curl` or `wget` to download the
credential.

Please note that the URL is temporary and won't work twice. If you want to get
another service credential use the following command to get another link:

    gbs account credential "YOUR-EMAIL-ADDRESS"

Save the credential as a file and place it `~/.config/gbs/credential.json`. If
there is no such directory, you should create one.

Run the following command to check if the credential registered correctly:

    gbs account describe

### Services, experiments, and goals

A `service` represents a website or an app. Single account may have one or more
services. To see registered services run the following command:

    gbs service list

If you've just created new account, the command will show an empty list.

Each service may contain zero or more `experiment`s and `goal`s. Each
`experiment` represents independent A/B test session and each `goal` represents
goals or objectives of the service such as new customer acquisition, purchase
completion, or reach to the target page.

In GreedyBandit, individual experiments don't contain goals. Instead, goals
belong to the service and **every single experiment in the service is evaluated
against every single goal.**  This separation of experiments and goals helps
you to avoid local optimizations caused by conflicting experiments.

### Configure experiments

### Configure goals

### Apply experiments to the website using Javascript SDK

### Monitor the performance on-going experiments

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
