Creating tree structures like those used for HTML and XML should be dead easy.
The xml.etree.ElementTree library goes quite far in creating a simple to use library
for creating and modifying such structures. I'd like to go a step further, building
on top of ElementTree::

    from magictree import html, head, title, body, h1, p
    doc = html(
            head(
              title('Chapter 1: Greeting')),
            body(
              h1('Chapter 1: Greeting'),
              p('Hello, world!')))

    from xml.etree import ElementTree as et    
    et.dump(doc)

Results in this: (added some whitespace for formatting)

::

    <html>
      <head>
        <title>Chapter 1: Greeting</title>
      </head>
      <body>
        <h1>Chapter 1: Greeting</h1>
        <p>Hello, world!</p>
      </body>
    </html>

This works by replacing this module with a wrapper object in sys.modules that
creates factory functions for elements based on their name.

I used this page as a basis for the hack: http://stackoverflow.com/questions/2447353/getattr-on-a-module
