
The idea is that you've two repositories, one holding the source code (the
source repository), another for the patches queue (the patch repository). You'll
have to have both of them modelized as cubicweb entities using vcsfile's
`Repository` entity type.

Provided you've already your source repository there, click 'add patch
repository' in the actions box. There gives it for instance a title and
url. Notice you *must* select option "import revision content" here else you
won't see patches, which make the whole thing useless.

Then repository's content should be imported later in the background. Once done,
you should see some `Patch` entities appearing.
