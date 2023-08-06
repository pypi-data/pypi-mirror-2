**html5witch** is a BSD-licensed, Python 2.5+ library that offers idiomatic XML generation based on [xmlwitch](http://pypi.python.org/pypi/xmlwitch/). It consists of a thin layer of subclasses to xmlwitch's **Builder** and **Element** classes. To install, just run **pip install html5witch**, **easy_install html5wich** or copy **html5witch.py** to your appropriate project's directroy. **pip** and **easy\_install** will automatically install **xmlwitch** if it's not present, but if you're manually maintaining a module directory you'll have to add **xmlwitch.py** to it too.

    import html5witch
    doc = html5witch.Builder()
    with doc.html:
        with doc.head:
            doc.title('Title')
        with doc.body:
            doc.p('Hello World')
            with doc.form(action="/", method="post"):
                doc.input(type="input", name="my_input_field")

Please refer to [http://jonasgalvez.com.br/Software/HTML5Witch.html](http://jonasgalvez.com.br/Software/HTML5Witch.html) for further info.

Pull requests are welcome.