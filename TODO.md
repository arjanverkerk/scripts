Todo
====

Album browser
-------------
    Librarypath
    Do something smart when in library and unchecking the toggle
    Fileview:
        Next / previous, with shortcuts j and k. also moves to next-in-tree outside folder.
        Load next with ajax; slide with bootstrap; remove previous.
        Also: Changes url. Must be exactly same page compared to when loaded directly.
    In library toggle with shortcut l.
    exif info, or file properties if no exif.
    If file is in library, it is checked.
    Also, a small preview of the file in the library is shown
    If not, it is unchecked.
    If going to checked state, do ajax:
        - Copy file to library
        - Path yyyy/mm/dd/name.img (collision detection?)
        - Date is from exif if possible, else modification date.
        - Create jsonfile:
            - description
            - date override for webalbum in isoformat. dateutil to parse. Datepicker.
            - keywords for partial album creation
    If going to unchecked state, remove
        - library file and meta file and empty directories from filesystem
        - metatext and datepicker and thumbnail previewer

Static site creator
-------------------
Plane html summingup of media and descriptions,
    grouped by date
    filtered for a keyword
