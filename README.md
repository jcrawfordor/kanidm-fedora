# kanidm-fedora

This repository drives the [COPR build](https://copr.fedorainfracloud.org/coprs/jbcrawford/kanidm/) for Kanidm. This package is closely based on the SuSE build and in use on some production machines, but should probably still be regarded as beta.

The package should build automatically on KanIDM release for supported Fedora versions (current and previous). This is based on a once-per-day check so it might take until the next day after the release.

## How it works

GitHub actions runs once a day and updates the specfile with the version of the most recent [KanIDM release](https://github.com/kanidm/kanidm/releases). If that results in a change, it commits it back to this repo and submits a build job to COPR. COPR retrieves the sources directly from GitHub's tarball-generating service. This is indeed a little awkward but it seems to work fine.

## How to use

```
dnf copr enable jbcrawford/kanidm
dnf install kanidm-clients
```
