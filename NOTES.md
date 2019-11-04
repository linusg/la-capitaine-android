# Notes

There's not much up-to-date information about creating icon themes for Android
out there, so this document will collect a few useful tips and links.

First of all, I'm using Lawnchair as my main launcher, so that's obviously the
one I'm testing with. Lawnchar is open source which has been incredible helpful!

For example there's a [list of icon pack intent names][lawnchair-iconpack-intents]
for which `<intent-filter>`s should exist and from the [`appfilter.xml` parsing
code][lawnchair-appfilter-xml] we can see how that file should look like and how
dynamic icons like clock and calendar can be created.

There's some existing icon theme code as well, see
[`iamareebjamal/scratch_icon_pack_source`][scratch-icon-pack-source]. Notably it
includes an example `appfilter.xml`, `drawable.xml` and `AndroidManifest.xml`.

[lawnchair-iconpack-intents]: https://github.com/LawnchairLauncher/Lawnchair/blob/5a8a4be9c6ecbbbcffaf813c32cc60dc2bf46833/lawnchair/src/ch/deletescape/lawnchair/iconpack/IconPackManager.kt#L287-L294
[lawnchair-appfilter-xml]: https://github.com/LawnchairLauncher/Lawnchair/blob/5a8a4be9c6ecbbbcffaf813c32cc60dc2bf46833/lawnchair/src/ch/deletescape/lawnchair/iconpack/IconPackImpl.kt#L92-L161
[scratch-icon-pack-source]: https://github.com/iamareebjamal/scratch_icon_pack_source
