# Notes

There's not much up-to-date information about creating icon themes for Android
out there, so this document will collect a few useful tips and links.

First of all, I'm using Lawnchair as my main launcher, so that's obviously the
one I'm testing with. [Lawnchair is open source](https://github.com/LawnchairLauncher/Lawnchair)
which has been incredible helpful!

For example there's a list of icon pack intent names
([source for v10][lawnchair-iconpack-intents-v10], [source for v11][lawnchair-iconpack-intents-v11])
for which `<intent-filter>`s should exist, and from the `appfilter.xml` parsing
code ([source for v10][lawnchair-appfilter-xml-v10], [source for v11][lawnchair-appfilter-xml-v11])
we can see how that file should look like and how dynamic icons like clock and
calendar can be created.

There's some existing icon theme code as well, see
[`iamareebjamal/scratch_icon_pack_source`][scratch-icon-pack-source]. Notably it
includes an example `appfilter.xml`, `drawable.xml` and `AndroidManifest.xml`.

[lawnchair-iconpack-intents-v10]: https://github.com/LawnchairLauncher/lawnchair/blob/c4759ea716ef6ccb6863ff9e647d784babeef400/lawnchair/src/ch/deletescape/lawnchair/iconpack/IconPackManager.kt#L284-L291
[lawnchair-iconpack-intents-v11]: https://github.com/LawnchairLauncher/lawnchair/blob/3175955790d86119f44cea184f978065eadaf26a/lawnchair/src/app/lawnchair/ui/preferences/PreferenceViewModel.kt#L36-L42
[lawnchair-appfilter-xml-v10]: https://github.com/LawnchairLauncher/lawnchair/blob/c4759ea716ef6ccb6863ff9e647d784babeef400/lawnchair/src/ch/deletescape/lawnchair/iconpack/IconPackImpl.kt#L92-L161
[lawnchair-appfilter-xml-v11]: https://github.com/LawnchairLauncher/lawnchair/blob/a6645106a53c25f9bc8d0f13009b257b987d059a/lawnchair/src/app/lawnchair/iconpack/IconPack.java#L65-L156
[scratch-icon-pack-source]: https://github.com/iamareebjamal/scratch_icon_pack_source
