*****************************
menhir.contenttype.photoalbum
*****************************

``menhir.contenttype.photoalbum`` provides a single content type
useable to display images as a collection. The content type has two
different rendering views, allowing to render the images as static
thumbnails or as an animated gallery.

Interfaces
==========

The ``menhir.contenttype.photoalbum`` `IPhotoAlbum` interface extendes
`IContainer` from ``zope.container``::

  >>> from zope.container.interfaces import IContainer
  >>> from menhir.contenttype.photoalbum import IPhotoAlbum

  >>> IPhotoAlbum.isOrExtends(IContainer)
  True

The `IPhotoAlbum` interface defines a containership contraint,
allowing only `IImage` contents, from ``menhir.contenttype.image``::

  >>> from menhir.contenttype.photoalbum import PhotoAlbum
  >>> album = PhotoAlbum(title=u"My nice images")

  >>> from zope.container.constraints import checkObject
  >>> checkObject(album, 'temporary', object())
  Traceback (most recent call last):
  ...
  InvalidItemType: (<menhir.contenttype.photoalbum.album.PhotoAlbum ...>,
  <object object at ...>, (<InterfaceClass menhir.contenttype...IImage>,))

A `PhotoAlbum` object provides the `IPhotoAlbum` interface but also
the `IViewSelector` interface, defining the name of the view used to
render the object::

  >>> IPhotoAlbum.providedBy(album)
  True

  >>> from dolmen.app.viewselector import IViewSelector
  >>> IViewSelector.providedBy(album)
  True


Factory
=======

The factory is protected by a common ``dolmen.app.security`` right::

  >>> from dolmen.content import require
  >>> print require.bind().get(album)
  dolmen.content.Add


Icon
====

The content registers an icon, thanks to the ``dolmen.app.content``
package::

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> request = TestRequest()
  >>> icon = getMultiAdapter((album, request), name="icon")
  >>> print icon
  <zope.browserresource.icon.IconView object at ...>


Population
==========

  >>> import os.path
  >>> from menhir.contenttype.image import Image

  >>> testpath = os.path.join(os.path.dirname(__file__), 'tests')
  >>> path1 = os.path.join(testpath, 'dolmen.png')
  >>> path2 = os.path.join(testpath, 'dolmen-test-site.png')

  >>> imagefile = open(path1)
  >>> image1 = Image(title=u"Logo", image=imagefile)
  >>> imagefile.close()

  >>> imagefile = open(path2)
  >>> image2 = Image(title=u"Example", image=imagefile)
  >>> imagefile.close()

  >>> from zope.component.hooks import getSite
  >>> site = getSite()
  >>> site['album'] = album
  >>> site['album']['dolmen_logo'] = image1
  >>> site['album']['dolmen_site_example'] = image2


Views
=====

Thumbnails view
---------------

  >>> print album.selected_view	
  thumbnails_view

  >>> import fanstatic
  >>> fanstatic.init_needed()
  <fanstatic.core.NeededResources object at ...>

  >>> index = getMultiAdapter((album, request), name="index")

  >>> index.update()
  >>> print index.content()
  <h1>My nice images</h1>
  <div class="photo-album">   
    <div class="gallery-thumbs">
       <ul class="thumbs noscript">
         <li>
    	   <a class="thumb image-link" 
              href="http://127.0.0.1/album/dolmen_logo/++thumbnail++image.preview"
              title="Logo" rel="gallery-...">
    	      <img src="http://127.0.0.1/album/dolmen_logo/++thumbnail++image.square"
                   title="Logo" alt="Logo" />
    	   </a>
        </li>
        <li>
    	   <a class="thumb image-link"
              href="http://127.0.0.1/album/dolmen_site_example/++thumbnail++image.preview"
              title="Example" rel="gallery-...">
    	      <img src="http://127.0.0.1/album/dolmen_site_example/++thumbnail++image.square"
                   title="Example" alt="Example" />
    	  </a>
        </li>
      </ul>
    </div>
  </div>

  >>> fanstatic.get_needed().resources()
  [<Resource 'css/slimbox2.css' in library 'jquery_slimbox'>,
   <Resource 'gallery.css' in library 'photoalbum.resources'>,
   <Resource 'jquery.js' in library 'jquery'>,
   <Resource 'js/slimbox2.js' in library 'jquery_slimbox'>,
   <Resource 'popup.js' in library 'menhir.contenttype.image'>]


Animated view
-------------

  >>> album.selected_view = "gallery_view"
  
  >>> fanstatic.init_needed()
  <fanstatic.core.NeededResources object at ...>

  >>> index = getMultiAdapter((album, request), name="index")

  >>> index.update()
  >>> print index.content()
  <h1>My nice images</h1>
  <div class="photo-album">   
    <div class="gallery-thumbs navigation">
      <ul class="thumbs noscript">
        <li style="opacity: 0.67">
    	  <a class="thumb"
             href="http://127.0.0.1/album/dolmen_logo/++thumbnail++image.preview"
	     title="Logo">
  	     <img src="http://127.0.0.1/album/dolmen_logo/++thumbnail++image.square"
                  title="Logo" alt="Logo" />
    	  </a>
    	  <div class="caption">Logo</div>
    	</li>
    	<li style="opacity: 0.67">
    	  <a class="thumb"
             href="http://127.0.0.1/album/dolmen_site_example/++thumbnail++image.preview"
	     title="Example">
    	     <img src="http://127.0.0.1/album/dolmen_site_example/++thumbnail++image.square"
                  title="Example" alt="Example" />
    	  </a>
    	  <div class="caption">Example</div>
    	</li>
      </ul>
    </div>
    <div class="gallery">
      <div class="controls"></div>
      <div class="loader"></div>
      <div class="main-image"></div>
      <div class="captions"></div>
    </div>    
    <div class="gallery-footer" />
  </div>

  >>> fanstatic.get_needed().resources()
  [<Resource 'gallery.css' in library 'photoalbum.resources'>,
   <Resource 'jquery.js' in library 'jquery'>,
   <Resource 'jquery.galleriffic.js' in library 'galleriffic'>,
   <Resource 'gallery.js' in library 'photoalbum.resources'>]
