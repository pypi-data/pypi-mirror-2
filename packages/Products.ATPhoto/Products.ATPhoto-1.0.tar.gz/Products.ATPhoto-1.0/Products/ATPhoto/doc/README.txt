Eggification

    Products.ATPhoto has been eggified on 2009/16/03

About

    ATPhoto is a product to manage photos in your Plone site. It provides two
    new content types: Photo, Photo Album. A photo album is a container for
    photos. The "ATPhoto product page":http://plone.org/products/atphoto/
    contains the latest information about the product.

Background

    This product was conceived during the "Plone multimedia sprint":http://plone.org/events/sprints/multimedia
    and was developed primarily by Russ Ferriday (topia.com) and Jean-Francois Roche (jfroche.be).

    Development work on ATPhoto continued on "IRC":irc://irc.freenode.net/plone4artists,
    and there was another burst of activity during the "Snow Sprint 2006":http://plone.org/events/sprints/snow-sprint3 in Egg, Austria.

    You are welcome to join in the development and report bugs as you find them.
    See the mailing list and bug reporting section below.

    ATPhoto is bundled with the "PloneMultimedia":http://plone.org/products/plonemultimedia/
    package along with ATAudio and ATVideo, and some other programs which
    improve Plone's handling of multimedia files.


Mailing List

    Just send a mail to atphoto@plone4artists.org with "subscribe" as the subject.
    You can read/search the "archives":http://lists.plone4artists.org/atphoto

Issue tracker

    Submit any bug you find or any feature you would like to see in this product:
    "Issue tracker":http://plone.org/products/atphoto/issues

Documentation

    Please see the "documentation area":http://plone.org/products/atphoto/documentation/
    on the ATPhoto products page which also includes some screencasts.

Roadmap

    New features are considered by posting a message to the mailing list. If
    your new feature is deemed feasible, you will be asked to write an
    improvement proposal which will then be reviewed by the authors and others
    in the development community, and if approved, added to the "roadmap":http://plone.org/products/atphoto/roadmap

Important INFO:

    Since we don't want to see two different content type for images and photo, features in ATPhoto are for the moment
    migrated to ATContentTypes (in the photoimage merge branch of ATContentTypes -
    see http://svn.plone.org/svn/collective/ATContentTypes/branches/photoimagemerge-branch/ )
    so all the feature you see here should be included in Plone Image content type. We are using a lot of Zope 3 stuffs
    and don't know exactly when our branch will be merged with ATContentTypes. But anyway we will provide migration script
    the day we switch to ATContentTypes.

Install

    Simply place the ATPhoto folder in your Zope's Products dir, restart and
    install in your Plone site using the 'portal_quickinstaller' tool in the
    ZMI, or go to 'Site Setup' -> 'Add/Remove Products'.

Requirements

    ATPhoto is dependent on:

  - Zope 2.8.x

      - Five (included with Zope 2.8/2.9)

  - Plone 2.1.2

    - ATContentTypes (ATCT) product 1.0.3 (packaged in Plone 2.1.2)

  - Python Imaging Library (PIL): http://www.pythonware.com/products/pil/
    (incl. with OSX and Windows installers. On Linux you must install manually)

  - FileSystemStorage (if you want your photos to be stored on the file system
    instead of in the ZODB)
    http://plone.org/products/filesystemstorage

Maintainer(s)

    Russ Ferriday (russ AT topia DOT com) russf on #plone or #plone4artists
    Jean-Francois Roche (jfroche AT jfroche DOT be) jfroche on #plone or #plone4artists
    IRC channels on Freenode (irc.freenode.net)

    See 'AUTHORS.txt' for a list of other contributors
