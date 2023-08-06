Introduction
============

An installable theme for Plone 4 made for Laboral - Center for arts and industrial creations

Features:
    - Built with multilanguage (LinguaPlone) in mind.
    - Footer reads a page (/footer) that creates menus out of lists.

Changelog
=========
3.6 (2011-3-16)
---------------
- Bugfixing

3.5 (2011-3-16)
---------------
- Added a file view override to make leadimage work with pdfcreator

3.4 (2011-3-8)
---------------
- Added date translations

3.3 (2011-2-23)
---------------
- Removed debug code

3.2 (2011-2-22)
---------------
- structure and CSS fix on dates
- menu bugfix that caused a crash on items without language

3.1 (2011-2-22)
---------------
- More CSS bugfixing
- Disabled links to leadimages

3.0 (2011-2-17)
---------------
- CSS bugfixing
- fixed sharebuttons on folder view

2.9 (2011-2-17)
---------------
- CSS bugfixing
- Added organization view structure

2.8 (2011-2-15)
---------------
- CSS for audio files

2.7 (2011-2-15)
---------------
- images are repeated in search results

2.6 (2011-2-15)
---------------
- used objectValues on menu instead of catalog search

2.5 (2011-2-3)
---------------
- Hidden calendar export on events
- iphone tweaks
- CSS fix on share buttons

2.4 (2011-2-1)
---------------
- New buttons and if zero do not show counter, check more than one digit case
- File view has pageWrapper in the wrong place
- Word published needs to be i18n
- Double check file view (should show published date too)
- Strange behaviour on paging  
- Cut dates on related items
- Design for form 
- Added a News tab to the search filter
- Check backend for design problems. Try to make a related item

2.3 (2011-1-26)
---------------
- Not allowing images to go full size
- fix on the share buttons
- fixes on the portlets lead images

2.2 (2011-1-26)
---------------
- Print CSS fix
- Screen CSS fix

2.1 (2011-1-25)
---------------
- make unpublished items red on folder view and slider view.
- review GS to avoid changing related slider views on install.
- Menu order was buggy.
- Move History and document by line to the end of the page.
- Change tile images size to 180px max height and width
- Review content size on backend.
- Remake CSS on Video tile.
- Realign paging.

2.0 (2011-1-18)
---------------
- Added first support to AddThis, still not stable though
- CSS fixes

1.9 (2011-1-18)
---------------
- Finished CSS on Search results
- Fixed language bug that affected the menu
- CSS for paging
- Removed icons even if icons on (annoying little things!)

1.8 (2011-1-18)
---------------
- Bugfix on dropdown menu on items with exclude from navigation
- Changed design on 
- Added Search result view
- Added search result python class and interface
- First CSS for search results 

1.7 (2011-1-13)
---------------
- Fixed logo translation bug that caused logo to disapear in some backend pages
- New view for the collection portlet with leadImages
- Menu fix to show only the main Folderish Items and Documents like in v2.theme
- Added javascript for square thumbnails but didn't activate it yet for the related items


1.6 (2011-1-13)
---------------
- Removed debugging code
- Deleted extra logo.pt file
- Added Date to news items (priority to Publication date, fall back on published date)

1.5 (2011-1-12)
---------------
- CSS Fixes
- Translatable logo
- Acid content test made for content CSS
- Created new file type and news item type views

1.4 (2011-1-6)
---------------
- CSS fixes for IE7
- New menu CSS and structure
- Several minor bugs

1.3 (2011-1-5)
---------------
- Searchfield CSS with better alignment, border size and image
- Text on the Tiles now wrap arround leadimage
- Corrected the script call for videos on tiles
- Fixed bug on line height of tile titles

1.2 (2011-1-5)
---------------
- Added background texture
- CSS for dates distinguishing past and future dates
- Added time and location of event to view (not final design)
- Added translation to location and time of event
- Search button rounded corners
- CSS for titles of the tiles
- CSS for titles of related items

1.1 (2011-1-4)
----------------
- CSS release
- new colors and titles
- Submenu on global_sections

1.0 (2010-12-31)
----------------
- First production release
- CSS alignments
- new view for videos

0.9 (2010-12-28)
----------------
- Moved slider to a new product collective.relatedSlideshow
- More CSS
- Javascript for flowplayer configuration
- Added missing images

0.8 (2010-12-28)
----------------
- removed useless icons from event_view

0.7 (2010-12-17)
----------------
- CSS, Viewlets ordering and hiding
- Slider hidden by default
- slider changes (title, leadimage etc...)

0.6 (2010-12-16)
----------------
- More CSS
- Added slider view


0.5 (2010-12-10)
----------------
- CSS for collective.portlet.relateditems
- fixed typography on footer
- Adapted CSS to collective.viewlet.references


0.4 (2010-12-10)
----------------

- Lots of CSS
- "Laboral Folder view" created
- Event view override and CSS
- Some Document view CSS

0.3 (2010-12-9)
----------------

- CSS fixes and alignments
- Footer bug fixed
- Login merged with footer menu
- Main menu recreated to occupy the hole width of the page
- Current language is hidden

0.2 (2010-12-7)
----------------

- Header and footer
- Backend CSS and general structure
- Viewlets reorganized
- Footer translatable (reads Page /footer on the root of a language if it exists create lists (ul li) to crate menus)

0.1dev (unreleased)
-------------------

- Initial release