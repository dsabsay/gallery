import argparse
import glob
import os
import subprocess

import jinja2
import yaml


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

    # Render trips
    os.mkdir(os.path.join(dest, 'trips'))
    for trip in glob.glob(os.path.join('src', 'templates', 'trips', '*')):
        _render_trip(trip, env, dest)


def _render_trip(trip, env, dest):
    """
    Params:
        trip (path-like) - The path to the trip.
        env (Jinja Environment)
        dest (path-like) - destination path for rendered files
    """
    name = os.path.basename(trip)
    os.mkdir(os.path.join(dest, 'trips', name))
    template = env.get_template(os.path.join('trips', name, 'index.html'))
    with open(os.path.join(dest, 'trips', name, 'index.html'), 'w') as f:
        f.write(template.render(
            base_stylesheet_path='../../css/styles.css',
            trip_stylesheet_path=f'../../css/trips/{name}.css')
        )

    template = env.get_template(os.path.join('trips', name, 'gallery.html'))
    # Parse gallery.yaml file
    with open(os.path.join(trip, 'gallery.yaml')) as f:
        gallery_cfg = yaml.safe_load(f)

    with open(os.path.join(dest, 'trips', name, 'gallery.html'), 'w') as f:
        f.write(
            template.render(
                base_stylesheet_path='../../css/styles.css',
                trip_stylesheet_path=f'../../css/trips/{name}.css',
                images=gallery_cfg['images']
            ),
        )

    # Render loupe pages
    loupe_template = env.get_template(os.path.join('trips', name, 'loupe.html'))
    for i in range(len(gallery_cfg['images'])):
        img = gallery_cfg['images'][i]
        if i + 1 < len(gallery_cfg['images']):
            next_img = gallery_cfg['images'][i+1]
        else:
            next_img = None
        if i > 0:
            prev_img = gallery_cfg['images'][i-1]
        else:
            prev_img = None
        try:
            os.mkdir(os.path.join(dest, 'trips', name, 'loupe'))
        except FileExistsError as e:
            pass  # Continue as normal of directory already exists
        with open(os.path.join(dest, 'trips', name, 'loupe', img['title'] + '.html'), 'w') as f:
            f.write(
                loupe_template.render(
                    base_stylesheet_path='../../../css/styles.css',
                    trip_stylesheet_path=f'../../../css/trips/{name}.css',
                    image=img,
                    next_img=next_img,
                    prev_img=prev_img
                )
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
