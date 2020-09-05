#!/usr/bin/env python
import os
import pkg_resources

import click
import helpers

# Check the required configuration files exist, and create defaults if not.
helpers.check_install()


def echo_data(data):
    for data_key, data_value in data.items():
        click.echo("%s = %s" % (data_key, data_value))


@click.group()
@click.version_option(pkg_resources.get_distribution("rcl").version)
def cli():
    pass


@click.command()
@click.argument('entry_id')
@click.argument('local_path')
@click.argument('remote_path')
def add(entry_id, local_path, remote_path):
    """Add a new entry."""
    helpers.add_entry({
        "id": entry_id,
        "local": local_path,
        "remote": remote_path
    })
    click.echo("Added new entry: %s" % entry_id)


@click.command('rm')
@click.argument('entry_id')
def remove(entry_id):
    """Remove an entry."""
    try:
        helpers.remove_entry(entry_id)
        click.echo("Deleted entry: %s" % entry_id)
    except KeyError:
        click.echo("ERROR: No entry found with id: %s." % entry_id)


@click.command('view')
@click.argument('entry_id', default="*")
def view_entries(entry_id):
    """View all entries or view a specific entry by using its ENTRY_ID."""
    config = helpers.load_config()

    if entry_id == "*":
        click.echo('\n==== Entries ====\n')
        for entry_id, entry_data in config['entries'].items():
            click.echo("[%s]" % entry_id)
            echo_data(entry_data)
            click.echo("\n")

    else:
        click.echo("[entries.%s]" % entry_id)
        echo_data(config['entries'][entry_id])


@click.command('config')
def open_config():
    """Open the config file ~/.rcl-config using the editor set in config. Default editor is 'nano'."""
    config = helpers.load_config()
    os.system("%s %s" % (config['editor'], helpers.CONFIG_FILE))


@click.command()
@click.argument('entry_id')
@click.option('--dry/--execute', default=False, help='Run rclone sync with --dry-run flag.')
def pull(entry_id, dry):
    """Sync local to match remote."""
    config = helpers.load_config()
    entry = config['entries'][entry_id]

    if dry:
        os.system("rclone sync %s %s --dry-run" % (entry['remote'], entry['local']))
    else:
        os.system("rclone sync %s %s --progress" % (entry['remote'], entry['local']))


@click.command()
@click.argument('entry_id')
@click.option('--dry/--execute', default=False, help='Run rclone sync with --dry-run flag.')
def push(entry_id, dry):
    """Sync remote to match local."""
    config = helpers.load_config()
    entry = config['entries'][entry_id]

    if dry:
        os.system("rclone sync %s %s --dry-run" % (entry['local'], entry['remote']))
    else:
        os.system("rclone sync %s %s  --progress" % (entry['local'], entry['remote']))


@click.command()
@click.argument('entry_id')
def diff(entry_id):
    """Show the difference between the local and remote."""
    config = helpers.load_config()
    entry = config['entries'][entry_id]

    os.system("rclone check %s %s --dry-run" % (entry['local'], entry['remote']))


cli.add_command(add)
cli.add_command(remove)
cli.add_command(view_entries)
cli.add_command(pull)
cli.add_command(push)
cli.add_command(diff)
cli.add_command(open_config)


if __name__ == '__main__':
    cli()
