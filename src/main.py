#!/usr/bin/env python3

# imports
import os
import json
import click
import requests
import configparser
from tabulate import tabulate

# default settings
default_config_dir = os.path.expanduser("~") + "/.lanlords"
default_config_file = default_config_dir + "/config"
default_options = {"api": {"url": {"env": "LANLORDS_API_URL"}}}

# read cli config file
def read_config(config_file=default_config_file):
    """
    Check if config file exists, read it and return dictionary
    """

    # check if config file exists
    if not (os.path.isfile(config_file)):
        # raise missing file exception
        raise FileNotFoundError('The config file "' + config_file + '" does not exist!')

    else:
        # read config file
        config = configparser.ConfigParser()
        config.read(config_file)

        # transform config to proper dict
        config_dict = {s: dict(config.items(s)) for s in config.sections()}

        # return parsed config
        return config_dict


# parse given option
def parse_option(option):
    """
    Parse given option to split on section, value and lookup related
    info in list of default options. Gives back info in dict form
    """

    # check if option is in correct format
    try:
        # set section/option variable
        option_section = option.split(".")[0]
        option_name = option.split(".")[1]

    except IndexError:
        # return error message and exit with err code
        click.echo(
            click.style("The option ", fg="red")
            + option
            + click.style(
                " is in an incorrect format!\n"
                + "This function expects input in the form of [section].[option]",
                fg="red",
            )
        )
        exit(code=11)

    # check if option is in predefined list
    try:
        # set current option configuration
        option_config = default_options[option_section][option_name]

    except KeyError:
        # return error message and exit with err code
        click.echo(
            click.style("The option ", fg="red")
            + option
            + click.style(" is not a valid option!", fg="red")
        )
        exit(code=11)

    # construct dict from option info
    parsed = {"name": option_name, "section": option_section, "config": option_config}

    return parsed


# retrieve config
def read_option(option):
    """
    Read option from config or environment variable
    This function expects input in the form of [section].[option]
    """

    # check if option is valid and parse it
    option_parsed = parse_option(option)

    # check for set environment variable
    try:
        # try to return set environment variable
        return os.environ[option_parsed["config"]["env"]]

    except KeyError:
        # read config and return value
        try:
            # retrieve and return option value from config
            option_config = read_config()
            option_value = option_config[option_parsed["section"]][
                option_parsed["name"]
            ]

            # return retrieved option value
            return option_value

        except KeyError:
            # return error message and exit with err code
            click.echo(
                click.style("The option ", fg="red")
                + option
                + click.style(
                    " is not defined in the config or as an " + "environment variable!",
                    fg="red",
                )
            )
            exit(code=11)


# call api and properly catch errors
def call_api(method, uri, data=None, url=read_option("api.url")):
    """
    Call API with given method and uri
    Request errors will be mostly catched and triggers exit
    """

    # default connection settings
    connect_timeout = 5.0

    # connect to api
    try:
        # execute get request to api
        if method == "get":
            # execute get request
            request = requests.get(url + uri, timeout=connect_timeout)

            # parse json and return output
            return json.loads(request.text)

        elif method == "post":
            # execute post request
            request = requests.post(url + uri, data=data, timeout=connect_timeout)

            # return response
            return request.text

        else:
            # raise incorrect method
            raise NameError('The HTTP method "' + method + '" is not valid!')

    except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
        # return error message and exit with err code
        click.echo(
            click.style("Could not connect to API ", fg="red")
            + url
            + click.style(" because of a timeout or connection error!", fg="red")
        )
        exit(code=11)


# main command group
@click.group()
def main():
    """Lanlords CLI Help"""


@main.command("test")
def main_test():
    """Test code snippets quickly"""
    ### DEBUG
    trying = read_option("api.url")
    print(trying)


# init config command
@main.group()
def config():
    """Configure the CLI"""


@config.command("init")
@click.confirmation_option(
    prompt="Are you sure? Any existing config wil be overwritten!"
)
@click.option("--api-url", prompt="Enter API url", help="API URL")
def config_init(api_url):
    """
    Create a new cli config
    """

    # check for lanlords directory
    if not (os.path.isdir(default_config_dir)):
        # create directory
        os.makedirs(default_config_dir)

    # construct config content
    config = configparser.ConfigParser()
    config["api"] = {}
    config["api"]["url"] = api_url

    # write config file
    with open(default_config_file, "w") as configfile:
        config.write(configfile)

    # output result
    click.echo("Configuration file has been created/updated")


@config.command("show")
def config_show():
    """
    Show current cli config
    """

    # check for lanlords config file
    if not (os.path.isfile(default_config_file)):
        # return no config error message and exit with err code
        click.echo(
            click.style("No config could be found at ", fg="red") + default_config_file
        )
        exit(code=11)
    else:
        # read current config file
        config = read_config()

        # output current config path
        click.echo(click.style(default_config_file, fg="yellow") + ":\n")

        # initialize empty list
        config_list = []

        # flatten config dictionary for output
        for section in config.keys():
            # separate per section
            for option in config[section]:
                # add setting to output list
                config_list = config_list + [
                    {
                        "Setting": "> " + section + "." + option,
                        "Value": click.style(config[section][option], fg="blue"),
                    }
                ]

        # output config settings and it's values
        click.echo(tabulate(config_list, tablefmt="plain"))


# init server command
@main.group()
def server():
    """Manage game servers"""


@server.command("start")
def server_start():
    """
    Start game server
    """
    click.echo("this is not yet implemented")


@server.command("stop")
def server_stop():
    """
    Stop game server
    """
    click.echo("this is not yet implemented")


@server.command("list")
def server_list():
    """
    List running game servers
    """
    click.echo("this is not yet implemented")


# init games command
@main.group()
def game():
    """Manage defined games"""


@game.command("list")
@click.option("--output-json", help="Output in JSON format", is_flag=True)
def game_list(output_json):
    """
    List defined games in admin
    """

    # execute api request
    request_output = call_api("get", "/servermanagement/games")

    # check if json output
    if output_json:
        # output in json format to terminal
        click.echo(json.dumps(request_output))

    else:
        # output in pretty table format to terminal
        click.echo(tabulate(request_output, headers="keys"))


# init containers command
@main.group()
def container():
    """Manage running containers"""


@container.command("list")
@click.option("--output-json", help="Output in JSON format", is_flag=True)
def container_list(output_json):
    """
    List running containers on server
    """

    # execute api request
    request_output = call_api("get", "/servermanagement/listContainers")

    # check if json output
    if output_json:
        # output in json format to terminal
        click.echo(json.dumps(request_output))

    else:
        # output in pretty table format to terminal
        click.echo(tabulate(request_output, headers="keys"))


# init main cli
if __name__ == "__main__":
    main()
