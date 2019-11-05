import sys
from pathlib import Path
from typing import Iterable, Mapping, NamedTuple

from cairosvg import svg2png
from colored import fg, attr
from ruamel.yaml import YAML

ICON_SIZE = 256

COLOR_YELLOW = fg("light_yellow")
COLOR_CYAN = fg("light_cyan")
COLOR_RESET = attr("reset")

DRAWABLE_NAME_PREFIX = "la_capitaine__"

PROJECT_DIR = Path(__file__).parent.resolve()

LA_CAPITAINE_ICONS_DIR = PROJECT_DIR / "la-capitaine-icon-theme/apps/scalable"
DRAWABLE_NODPI_DIR = PROJECT_DIR / "app/src/main/res/drawable-nodpi"

APPFILTER_XML_PATH = PROJECT_DIR / "app/src/main/res/xml/appfilter.xml"
APPFILTER_XML_TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!--
    <iconback img1="iconback" />
    <iconmask img1="iconmask" />
    <iconupon img1="iconupon" />
    <scale factor=".75" />
    -->
    {items}
</resources>
"""

DRAWABLE_XML_PATH = PROJECT_DIR / "app/src/main/res/xml/drawable.xml"
DRAWABLE_XML_TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <version>1</version>
    {items}
</resources>
"""

Icons = Mapping[str, str]


class App(NamedTuple):
    package: str
    activity: str
    icon: str


def get_drawable_name(icon_name: str) -> str:
    # Add a prefix so all generated PNGs can be excluded from version control
    return f"{DRAWABLE_NAME_PREFIX}{icon_name}"


def write_appfilter_xml(apps: Iterable[App]) -> None:
    items = [
        f'<item component="ComponentInfo{{{app.package}/{app.activity}}}"'
        f' drawable="{get_drawable_name(app.icon)}" />'
        for app in apps
    ]
    content = APPFILTER_XML_TEMPLATE.format(items="\n    ".join(items))
    print(f"Writing {COLOR_YELLOW}xml/appfilter.xml{COLOR_RESET}")
    APPFILTER_XML_PATH.write_text(content)


def write_drawable_xml(icons: Icons) -> None:
    items = [
        f'<item drawable="{get_drawable_name(icon_name)}" />'
        for icon_name in icons.keys()
    ]
    content = DRAWABLE_XML_TEMPLATE.format(items="\n    ".join(items))
    print(f"Writing {COLOR_YELLOW}xml/drawable.xml{COLOR_RESET}")
    DRAWABLE_XML_PATH.write_text(content)


def write_icon_images(icons: Icons) -> None:
    DRAWABLE_NODPI_DIR.mkdir(mode=0o755, parents=True, exist_ok=True)
    for icon_name, icon_file in icons.items():
        # Resolve allows using symlinks for icon file
        src = (LA_CAPITAINE_ICONS_DIR / icon_file).resolve()
        dest = DRAWABLE_NODPI_DIR / f"{get_drawable_name(icon_name)}.png"
        print(
            f"Writing {COLOR_YELLOW}{dest.parent.name}/{dest.name}{COLOR_RESET} ({COLOR_CYAN}{src.name}{COLOR_RESET})"
        )
        svg2png(
            src.read_text(),
            write_to=str(dest),
            output_width=ICON_SIZE,
            output_height=ICON_SIZE,
        )


def main() -> None:
    try:
        command = sys.argv[1]
    except IndexError:
        command = ""

    if command == "build":
        res_path = PROJECT_DIR / "res.yml"
        res = YAML().load(res_path)
        icons = res["icons"]
        apps = [App(**app) for app in res["apps"]]
        write_appfilter_xml(apps)
        write_drawable_xml(icons)
        write_icon_images(icons)
    elif command == "clean":
        for file in (APPFILTER_XML_PATH, DRAWABLE_XML_PATH):
            try:
                file.unlink()
                print(
                    f"Removed {COLOR_YELLOW}{file.parent.name}/{file.name}{COLOR_RESET}"
                )
            except FileNotFoundError:
                # missing_ok param is 3.8+ only
                pass
        for file in DRAWABLE_NODPI_DIR.glob(f"{DRAWABLE_NAME_PREFIX}*.png"):
            file.unlink()
            print(f"Removed {COLOR_YELLOW}{file.parent.name}/{file.name}{COLOR_RESET}")
    else:
        print(f"Usage: {__file__} [build|clean]")
        sys.exit(1)


if __name__ == "__main__":
    main()
