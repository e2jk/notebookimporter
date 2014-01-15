Notebook Importer
=================

Used to import notes into Evernote from a CSV file.

This utility will send one email per note to your secret Evernote email address, which you can find in `your Evenote settings page <https://www.evernote.com/Settings.action>`_. It uses Gmail to send the emails to Evernote.

How to use
----------

- Download the ``notebookimporter.py`` script.
- Adapt the following 3 variables to your situation:
  
  - ``GMAIL_LOGIN``
  - ``GMAIL_PASSWORD``
  - ``EVERNOTE_EMAIL``
  
- Run the script with your ``.csv`` file as the sole argument:
  
  ``python notebookimporter.py ~/Documents/notes.csv``

Format of the CSV file
----------------------

The file containing the notes you want to import to Evernote must follow these rules:

- The first line of the CSV file is the header, which must contain the following 5 columns (no more, no less):

  - Title
  - Content
  - Labels
  - Notebook
  - Do not upload
  
- One line in the CSN file represents one note
- A line that has any text in the 5th column ("Do not upload") will not be sent to Evernote

Have a look at the ``sample.csv`` file for an example.

Known Limitations
-----------------

- Evernote limits the number of emails that can be sent per day:

  - Non-premium Evernote accounts: 50 emails per day
  - Premium Evernote accounts: 200 emails per day
  
  In case you have more than 50/200 notes to upload to your Evernote account, you will need to do that over several days. After each upload, mark the notes that have been uploaded by adding some text (e.g. "Y") in the 5th column ("Do not upload") of your CSV file. This will allow you to not resent the same notes on the following day ;)

- Only one label can be specified (you should be able to cheat by specifying a first label without #, then separating further labels with spaces and ensuring the other labels do start with a # - not tested)

- Only Evernote is supported at this time, however it looks like all the major players are currently lacking an import feature, so this utility should prove helpful for other services, e.g. Springpad.

- You need a Gmail address/password to send the notes to Evernote.

License
-------

Notebook Importer is released under the GNU Affero General Public License. Contributions are welcome!

