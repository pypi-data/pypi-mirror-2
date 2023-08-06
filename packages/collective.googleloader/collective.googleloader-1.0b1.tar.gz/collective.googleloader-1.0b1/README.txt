Introduction
============

From google:

    In order to use the Google APIs, you must import them using the Google API
    loader in conjunction with the API key. The loader allows you to easily import
    one or more APIs, and specify additional settings (such as language, location,
    API version, etc.) applicable to your needs.
    
    In addition to the basic loader functionality, savvy developers can also use
    dynamic loading or auto-loading to enhance the performance of your application.
    

This add-on provide integration of the google loader (aka jsapi) into Plone.
It provides autoupdate of javascript registry depend on hostname. API keys are
stored into plone.app.registry, so you can use the provided control panel to
configure it (adding API keys)

