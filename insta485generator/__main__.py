"""Build static HTML site from directory of HTML templates and plain files."""
import click
import pathlib
import json
import jinja2
import shutil


# def main():
#     """Top level command line interface."""
#     print("Hello world!")

@click.command()
@click.argument("input_dir", nargs=1, type=click.Path(exists=True))
@click.option('--output', '-o',  default=pathlib.Path(), nargs=1,help="Output directory.",type = click.Path())
@click.option('--verbose', '-v', is_flag=True,help="Print more output.")
def main(input_dir, output, verbose):
    """Templated static website generator."""
    try:
        input_dir = pathlib.Path(input_dir)
        json_dir = pathlib.Path.joinpath(input_dir, "config.json")
        jfile = json.load(open(json_dir))
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
                click.echo("Copied "+str(static_dir)+" -> "+str(opath))
        else:
            opath.mkdir()
        

        for j in jfile:
            template = template_env.get_template(j["template"])
            content = template.render(j["context"])
            url = j["url"].lstrip("/")
            url = pathlib.Path.joinpath(opath, url)
            # print(static_dir, opath)
            # should put on piazza
            # if pathlib.Path.exists(opath) & pathlib.Path.exists(static_dir):
            #     shutil.rmtree(opath)
            if(j["url"].lstrip("/")!=""):
                url.mkdir(parents=True)
            out = open(pathlib.Path.joinpath(opath, "index.html"), "w")
            out.write(content)
            click.echo("Rendered "+str(j["template"])+" -> " +
                       str(pathlib.Path.joinpath(opath, "index.html")))
    except FileNotFoundError:
        print(1)
        exit(1)
    except json.JSONDecodeError:
        print(2)
        exit(1)
    except jinja2.TemplateError:
        print(3)
        exit(1)
    except FileExistsError:
        print(4)
        exit(1)


    # print(jfile)
    # print(f"DEBUG input_dir={json_dir}")
if __name__ == "__main__":
    main()
