import json
import re
import sys
from pathlib import Path
from typing import Iterable, NamedTuple

from cairosvg import svg2png
from colored import fg, attr

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

ICONPACK_XML_PATH = PROJECT_DIR / "app/src/main/res/values/iconpack.xml"
ICONPACK_XML_TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string-array name="icon_pack" translatable="false">
        {items}
    </string-array>
</resources>
"""


class Icon(NamedTuple):
    package: str
    activity: str
    file: str


def activity_to_drawable_name(activity: str) -> str:
    slug = re.sub(r"\W+", "_", activity).lower()
    # Add a prefix so all generated PNGs can be excluded from version control
    return f"{DRAWABLE_NAME_PREFIX}{slug}"


def write_appfilter_xml(icons: Iterable[Icon]) -> None:
    items = [
        f'<item component="ComponentInfo{{{icon.package}/{icon.activity}}}"'
        f' drawable="{activity_to_drawable_name(icon.activity)}" />'
        for icon in icons
    ]
    content = APPFILTER_XML_TEMPLATE.format(items="\n    ".join(items))
    print(f"Writing {COLOR_YELLOW}xml/appfilter.xml{COLOR_RESET}")
    APPFILTER_XML_PATH.write_text(content)


def write_drawable_xml(icons: Iterable[Icon]) -> None:
    items = [
        f'<item drawable="{activity_to_drawable_name(icon.activity)}" />'
        for icon in icons
    ]
    content = DRAWABLE_XML_TEMPLATE.format(items="\n    ".join(items))
    print(f"Writing {COLOR_YELLOW}xml/drawable.xml{COLOR_RESET}")
    DRAWABLE_XML_PATH.write_text(content)


def write_iconpack_xml(icons: Iterable[Icon]) -> None:
    items = [
        f"<item>{activity_to_drawable_name(icon.activity)}</item>" for icon in icons
    ]
    content = ICONPACK_XML_TEMPLATE.format(items="\n        ".join(items))
    print(f"Writing {COLOR_YELLOW}values/iconpack.xml{COLOR_RESET}")
    ICONPACK_XML_PATH.write_text(content)


def write_icon_images(icons: Iterable[Icon]) -> None:
    DRAWABLE_NODPI_DIR.mkdir(mode=0o755, parents=True, exist_ok=True)
    for icon in icons:
        # Resolve allows using symlinks for icon.file
        src = (LA_CAPITAINE_ICONS_DIR / icon.file).resolve()
        dest = DRAWABLE_NODPI_DIR / f"{activity_to_drawable_name(icon.activity)}.png"
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
        res_json_path = PROJECT_DIR / "res.json"
        res_json_content = res_json_path.read_text()
        icons = [Icon(**icon) for icon in json.loads(res_json_content)]
        write_appfilter_xml(icons)
        write_drawable_xml(icons)
        write_iconpack_xml(icons)
        write_icon_images(icons)
    elif command == "clean":
        for file in (APPFILTER_XML_PATH, DRAWABLE_XML_PATH, ICONPACK_XML_PATH):
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
