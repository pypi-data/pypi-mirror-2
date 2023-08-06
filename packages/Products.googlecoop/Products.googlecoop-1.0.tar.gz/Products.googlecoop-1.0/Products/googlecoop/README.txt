googlecoop
---

  Google Coop for Plone makes it easy for you to integrate a Google Co-op Custom
  Search engine in your plone site.
  
Install

  Install the Product in Site-Setup Add/Remove Products.
  Enter your Custom Search Engine's unique identifier in the 
  googlecoop configuration. (You find the identifier in the 'code' 
  section in the control panel of your searchengine)
  
  You can access the search page of your search engine by
  adding '/googlecoop' to the url of your plone instance.
  
Exporting Plone links to Google co-op
  
  If you have lots of Links in your site you want to add to
  your searchengine you can export them by adding '/coop-lable.xml'
  to the url of the folder in which the links are located or if you want to include 
  all links in your site 
  This produces an Annotation file with your plone subjects as lables.
  You may want to edit that file before uploading it to google.
  (In the 'Advanced' section in the control panel of your searchengine)
  
  You may also produce a context file for your CSE.
  If you use your sites keywords as labels for the CSE this contextfile will
  include the keywords you assigned to your google co-op tool as facets and labels.
  This comes in handy if you want to include more than 16 refinements in your stored
  CSE.

Building A Linked Custom Search Engine with 'Tasty Bookmarks'

  In a Linked CSE the specification of the search engine is hosted on your website.
  Google retrieves the CSE specification from your website when your user searches in the CSE. 
  This has several very important benefits:

    * You can easily convert your 'Tasty Links' to a Custom Search Engine.
    * You can automatically generate any number of CSEs, each tuned to the particular page ('Bookmark Folder') or as a response to a users query ('Tasty view').
    * You can easily update your Linked CSE definitions without pushing data to Google.
    * There are no global, per user annotation limits.

  You can now exploit the full power of your ideas to dynamically generate CSEs. 
  This makes it easier to share annotations between CSEs.
  
  Tasty Bookmarks generates two files for you:

   * tasty-cseref: The CSE specification
   * tasty-annotations: The Google Annotations (i.e. the sites you want to search)
  
