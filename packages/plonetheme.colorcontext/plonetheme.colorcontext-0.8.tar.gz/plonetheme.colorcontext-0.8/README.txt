Introduction
============

Total CSS reformatting and color themed sections

Instructions
============

The Color Context Theme colors your menu, cllection and folder view blocks and search results depending on the URL of item in question.
Take for example a 'projects section' of a site under www.mysite.com/projects that is colored red. Every item under projects would be colored red.
It is also possible to color in more than one level on the url path. imagine that www.mysite.com/projects is red but you want www.mysite.com/projects/project1 (and everything under it) to be blue. It is possible by creating anoter section block on the colors.css file and substituting .projects by .projects.project1 and the color attributes to blue
  
To configure the colors of the sections of your site:

- Go to site setup -> ZMI (Zope Management Interface)
- Choose portal_skins -> plonetheme_colorcontext_styles 
- click on colors.css
- click customize
- copy/paste or alter any of the section blocks on the file (Projects Section for example)
- substitute .projects by the any part of your site url (for example .events or .events.past)
- click save changes and check the results.
