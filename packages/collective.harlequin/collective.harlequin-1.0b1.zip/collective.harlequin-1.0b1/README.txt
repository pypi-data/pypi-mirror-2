Introduction
============

Harlequin provide infrastructure to make configurable browser view. This
module doesn't provide any feature to Plone.

How to use it
=============

You want to develop a browser view that need configuration ? Make your browser
view inherits from collective.harlequin.browser.Harlequin (or implements IHarlequinView)

Next you can define your configuration with a zope.schema interface which inherits from
collective.harlequin.forms.Schema

Next you have to make your z3cform with the configuration schema and inherits from
collective.harlequin.forms.Form.

The base harlequin view is not aware of your schema. you have to implements harlequin_schema method
from IHarlequinView and that's it, you have your 'harlequin' view !

Next make your view available in the display drop down menu, and try by selecting it ! You get
The form displayed, fill it and validate it, the job is made for you.

How it works
============

It override the setViewTemplate script, and redirect to a custom form if the
choosen view is an 'harlequin' view

The basic z3cform for configuration use a templateId field in hidden mode to store the templateId

By default configuration are stored with the property manager. It's simple to make it work with
annotation, but property has the advantage to be useable throw ZMI.

Credits
=======

|makinacom|_

  * `Planet Makina Corpus <http://www.makina-corpus.org>`_
  * `Contact us <mailto:python@makina-corpus.org>`_

Authors

  - JeanMichel FRANCOIS aka toutpt <toutpt@gmail.com>

Contributors


.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com
