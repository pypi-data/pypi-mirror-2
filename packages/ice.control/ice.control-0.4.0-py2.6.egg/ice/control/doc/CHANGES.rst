Changelog
*********

0.4.0 (2010-08-27)
------------------

- support bluebream 1.0b4

- new dublincore permissions (zope.dublincore >= 3.7.0)

- added zope.principalannotation zcml into ice.control.zcml, introspector to work correctly

- minor fix in css - truncate too long urls in details header

0.3.3 (2010-07-02)
------------------

- support bluebream 1.0b2

- minor fixes in css and ice.control.zcml

- fix rst syntax in documentation

0.3.2 (2010-05-05)
------------------

- better support for Google Chrome 

- minor changes in skin, added BB favicon

- added method `clean` into REPL dispatcher

- LP #570887: REPL, help(): Error "ValueError: I/O operation on closed file"

- LP #570006: problems with monospace font for REPL in Google Chrome

- LP #571805: undented REPL input field, and prompt appear in the previous line.

- LP #575544: incorrect auto scrolling in REPL.


0.3.1 (2010-04-21)
------------------

- fixed docs


0.3.0 (2010-04-21)
------------------

- Namespace `++control++` instead of `++etc++control`.

- Transitive security for IControl (10x location proxy).

- Transitive access to content context from IControl (method get_content()).

- Use controls not only on root folder, but on any content,
  i.e. 'foo/bar/++control++/'

- Allow nested (recursive) namespaces, i.e. '++control++/++control++/'
  and etc.

- Auto scrolling in REPL.

- Used accurate permissions in all views.

- DEfine explicit layer in skin's views.

- Added ZODB Pack control.

- Added Ctrl+E keybinding in REPL ("go to line end")

- Front page for any context now (skin).

- More convenient authentication.

Two special permissions in the package:

- ice.control.View (display Tree)

- ice.control.REPL (use REPL)

In summary, it can now be used as pluggable CMS UI for users with
different permissions and roles, not only zope.Manager, from any nested
content object, not only root folder, and UI should correctly display menu
items and views accordingly to context and permissions.


0.2.0 (2010-04-15)
------------------

- Added details views for IErrorReportingUtility, display error logs
  and edit settings.

- Fixed XML TreeView for ISite.


0.1.3 (2010-04-14)
------------------

- Fixed a bug that appeared in 0.1.2: `details` view not send
  ajax form data.


0.1.2 (2010-04-12)
------------------

- 100% tests or something like.

- Added zcml condition for details: metadata.

- Apidoc window features: fixed.

- Fixed bug: anchor's behavior in introspector.

- Increased supported version of bluebream: 1.0a5


0.1.1 (2010-04-07)
------------------

Fixed MANIFEST.in to include docs into distribution.


0.1.0 (2010-04-07)
------------------

First release tag.
