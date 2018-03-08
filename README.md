# Python text randomizer

Generate random text based on template

## Examples

``
template = '{Brown|Red} fox {jump over|dig under} [lazy|crazy] dog'
text_rnd = TextRandomizer(template)
print(text_rnd.get_text())
``

You will get random text like 'Red fox dig under crazy lazy dog'.