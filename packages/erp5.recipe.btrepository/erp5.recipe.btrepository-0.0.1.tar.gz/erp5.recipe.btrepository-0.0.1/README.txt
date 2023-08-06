Build your Business Template Repository
=========================================

This recipe is used to create ERP5 business templates repositories. Each
repository is compiled from a URL with uncompress business templates on it.
This implementation still quite experimental.

Example
====================

You can use it with a part like this:
::
  [bt5]
  recipe = erp5.recipe.btrepository
  url =
    https://svn.erp5.org/repos/public/erp5/trunk/products/ERP5/bootstrap/
    https://svn.erp5.org/repos/public/erp5/trunk/bt5

Options
====================

url 

  Provide 1 or more URL address where the business templates will be 
  downloaded from. 

download-command (Optional)

  We use "svn co .." as standard `command` but you can define alternative svn 
  command (or other) to download the repositories.

download-command-extra (Optional)

  Additional string appended to download-command. Usefull to define revision.
  Tip: Use "-r XXXXX" to set specific revision.

preserve-download (Optional)

  Define if download folder will be erased or not after download and compress
  is finished. Default value is 1.

location (Optional)

  Define alternative location to place your repository.
  Default is into parts/PARTNAME

auto-build (Optional) 0 or 1

  Define if buildout automatically launch business template download and 
  compress automatically or only generate update script for manually run. 
  Default is 0.
