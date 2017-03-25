import os
import json

import click
import toml
import pipfile

# from .__about__ import __version__


def err(*a, **kw):
    kw["err"] = True
    click.echo(*a, **kw)


def format_toml(data):
    data = data.split('\n')
    for i, line in enumerate(data):
        if i > 0:
            if line.startswith('['):
                data[i] = '\n{0}'.format(line)

    return '\n'.join(data)


def create_pipfile():
    data = {
        "source": [{
            "url": "https://pypi.python.org/simple",
            "verify_ssl": True,
        }],
        "packages": {},
        "dev-packages": {},
    }

    with open("Pipfile", "w") as f:
        f.write(format_toml(toml.dumps(data)))


@click.group()
def cli():
    pass


@cli.command()
@click.option("-m", "--module-path", prompt=True)
def init(module_path):
    had_pipfile = False
    if os.path.isfile("Pipfile"):
        had_pipfile = True
        err("Pipfile already exists, skipping...")
    else:
        err("Creating Pipfile...")
        create_pipfile()

    vendor_path = os.path.join(module_path, "vendor")
    if os.path.isdir(vendor_path):
        err("%s already exists, skipping..." % vendor_path)
    else:
        err("Creating vendor dir (%s)..." % vendor_path)
        os.makedirs(vendor_path, exist_ok=True)

    err("\nDone! Please add the following lines to your %s/__init__.py:\n"
        % module_path)

    err("    v_path = os.path.sep.join([")
    err("        os.path.dirname(os.path.realpath(__file__)), 'vendor'])")
    err("    if os.path.isdir(v_path):")
    err("        sys.path.append(v_path)")

    if not had_pipfile:
        err("\nTo install dependencies, run `vend install`.")


@cli.command()
@click.option("--dev", is_flag=True)
@click.option("--ignore-hashes", is_flag=True)
def install(dev, ignore_hashes):
    if os.path.isfile("Pipfile.lock"):
        lockfile_location = pipfile.Pipfile.find() + ".lock"
        if not os.path.isfile(lockfile_location):
            err("Lockfile not found.")

        with open(lockfile_location) as f:
            lock = json.load(f)

        deps = lock["default"]
        if dev:
            deps.update(lock["develop"])

        pip_deps = []

        if not ignore_hashes:
            for name, dep in deps.items():
                pip_deps.append("{name}{version} --hash={hash}".format(
                    name=name, version=dep["version"], hash=dep["hash"]))
        else:
            for name, dep in deps.items():
                pip_deps.append("{name}{version}".format(
                    name=name, version=dep["version"]))

        print("\n".join(pip_deps))


if __name__ == '__main__':
    cli()
