"""Build static HTML site from directory of HTML templates and plain files."""
import pathlib
import json
import shutil
import sys
import jinja2
import click


# def main():
#     """Top level command line interface."""
#     print("Hello world!")

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('--output', '-o',  default=pathlib.Path(),
              nargs=1, help="Output directory.", type=click.Path())
@click.option('--verbose', '-v', is_flag=True, help="Print more output.")
def main(input_dir, output, verbose):
    """Templated static website generator."""
    try:
        input_dir = pathlib.Path(input_dir)
        json_dir = pathlib.Path.joinpath(input_dir, "config.json")
        with open(json_dir, encoding="utf-8") as dashabi:
            jfile = json.load(dashabi)
        temp_dir = pathlib.Path.joinpath(input_dir, "templates")
        template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(temp_dir)),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
        )

        static_dir = pathlib.Path.joinpath(input_dir, "static")
        if output == pathlib.Path():
            opath = pathlib.Path.joinpath(input_dir, "html")
        else:
            opath = pathlib.Path(output)
        if pathlib.Path.exists(static_dir):
            shutil.copytree(static_dir, opath)
            if verbose:
                click.echo("Copied "+str(static_dir)+" -> "+str(opath))
        else:
            opath.mkdir()

        for j in jfile:
            template = template_env.get_template(j["template"])
            content = template.render(j["context"])
            url = j["url"].lstrip("/")
            url = pathlib.Path.joinpath(opath, url)

            if j["url"].lstrip("/") != "":
                url.mkdir(parents=True)
            with open(pathlib.Path.joinpath(
                    url, "index.html"), "w", encoding="utf-8") as csb:
                csb.write(content)
            if verbose:
                click.echo("Rendered "+str(j["template"])+" -> " +
                           str(pathlib.Path.joinpath(url, "index.html")))
    except FileNotFoundError:
        print(1)
        sys.exit(1)
    except json.JSONDecodeError:
        print(2)
        sys.exit(2)
    except jinja2.TemplateError:
        print(3)
        sys.exit(3)
    except FileExistsError:
        print(4)
        sys.exit(4)


if __name__ == "__main__":
    main()
