import argparse
import glob
import os
import subprocess

import jinja2


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def main(dest):
    """
    Renders all files and places them in docs/ directory.
    """
    os.chdir(SCRIPT_DIR)

    # Update static/
    subprocess.run(
        ["rsync", "-av", "--delete", "src/static/", dest],
        capture_output=False,
        check=True
    )

    # Render templates
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.join('src', 'templates'))
    )

    # Render main site pages
    context = {
        'base_stylesheet_path': 'css/styles.css'
    }
    index = env.get_template('index.html')
    with open(os.path.join(dest, 'index.html'), 'w') as f:
        f.write(index.render(context))

    trips_index = env.get_template('trips.html')
    with open(os.path.join(dest, 'trips.html'), 'w') as f:
        f.write(trips_index.render(context))

    # Render trips
    os.mkdir(os.path.join(dest, 'trips'))
    for trip in glob.glob(os.path.join('src', 'templates', 'trips', '*.html')):
        trip_template = os.path.basename(trip)
        trip_name = os.path.splitext(trip_template)
        template = env.get_template(os.path.join('trips', trip_template))
        with open(os.path.join(dest, 'trips', trip_template), 'w') as f:
            f.write(template.render(
                base_stylesheet_path='../css/styles.css',
                trip_stylesheet_path=f'../css/styles/{trip_name}.css')
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the gallery.")
    parser.add_argument(
        "--destination",
        type=str,
        default="docs",
        help="Directory where built files will go.",
    )
    args = parser.parse_args()
    main(args.destination)
