Todo
====

Media viewer
------------
actions:
j next
k previous
d edit description
  delete
  keywords

display:
- exif selection
- description
- keywords
- location (can be the url)



Album browser
-------------
    Navigation:
        j down
        k up
        h parent
        l toggle in / not in library
    Fileview:
        Next / previous, with shortcuts j and k. also moves to next-in-tree outside folder.
        Load next with ajax; slide with bootstrap; remove previous.
        Also: Changes url. Must be exactly same page compared to when loaded directly.

    viewing a file in library:
        - date picker
        - description field
        - l removes file from library and moves to next
    viewing a file outside library that also exists in library:
        - date picker
        - description field
        - preview
        - l removes file from library
    viewing a file outside library
        - exif info, or file properties if no exif.
        - l adds file to library

    When a file is added to library:
        - Copy file to library
        - Path yyyy/mm/dd/filename
        - Date is from exif if possible, else modification date.
        - Create jsonfile:
            - description
            - date override for webalbum in isoformat. dateutil to parse. Datepicker.
            - keywords for partial album creation
    When a file is removed from library:
        - Empty file and metafile and any empty directories


Static site creator
-------------------
Plane html summingup of media and descriptions,
    grouped by date
    filtered for a keyword
