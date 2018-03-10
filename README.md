# Python text randomizer

Generate random text based on template

## Example

```python
from text_randomizer import TextRandomizer

template = '{Brown|Red} fox {jump over|dig under} [lazy|crazy] dog'
text_rnd = TextRandomizer(template)
print(text_rnd.get_text())
```

You will get random text like 'Red fox dig under crazy lazy dog'.

## Template string

Template is a usual short or long text with special randomize commands:
* 'Synonyms' command - {variant1 | variant2 | variant3} - insert one of the variants to the result string
* If you want to omit text - use 'empty' variant - {|variant}
* Mixin command = [ text 1 | text 2 | text 3] - will mix this variants randomly
* You can use separator in mixin - [+,+text 1|text2 ] - you will get text2,text1. Separator can by any symbol or set of symbols:
  [+==+ a|b] - a==b or b==a
* If you want to get spesial symbol in your result ('{', '}', '[', ']', '|', '+') - use backslash for it - \{, \}, \[,
   \], \|, \+
* All this commands can be mixed and nested in all combinations: 'start {aa|bb|{cc1|cc2}} or [a1|{word1|word2}|a3| [aa1|aa2|aa3]]'
* You can use special predefined random functions in templates - {random integer = $RANDINT(1,10), uuid = $UUID, now = $NOW(%Y-%M-%d)}.
  Result will be = 'random integer = 4, uuid = 8ae6bdf4-d321-40f6-8c3c-81d20b158acb, now = 2017-08-01'
  You can define your own randomization functions and use it in templates. Read about functions further.

## API and more examples

Pass template string to TextRandomizer constructor. It will be parsed at once. After creating randomizer object, you can use
its get_text() method.

This behaviour can be changed - if you pass parse=False parameter to constructor: TextRandomizer(templ_str, parse=False) -
template will not be parsed before you run TextRandomizer.parse() method. Only after this method you can use get_text() method.
This can be usefull is several cases. Lets see some examples.

```python
from text_randomizer import TextRandomizer

# parse template at once
text_rnd1 = TextRandomizer('randomize {me|it|him|her} please')
for i in range(0,10):
    print(text_rnd1.get_text())

# Do not parse template. Parse when needed. This can save you time and memory
text_rnd2 = TextRandomizer('randomize {me|it|him|her} please $YOUR_FUNC(5)', parse=False)
# you can register your own randomization functions before parsing
# run parse() before get_text() call. Otherwise you will get exception
text_rnd2.parse()
for i in range(0,10):
    print(text_rnd2.get_text())
```

You can get number of all possible variants by calling TextRandomizer.variants_number() method. But if you use randomize functions - this value will be imprecise.

For example - 'start {word1 | word2} end' - will give you 2 variants. And 'start {word1 | word2} $UUID end' will give you infinite variants.

Next example shows how to register your own function. Do it before parse() call

```python
text_rnd = TextRandomizer('$YOUR_FUNC1(5, 10) and $FUNC2(param1, param2)', parse=False)

# use simple callable for function
text_rnd.add_function('FUNC2', lambda p1, p2: '{} and {}'.format(p1, p2))

# use dictionary for more complicated cases.
text_rnd.add_function('YOUR_FUNC1', {'callable': lambda x, y: randint(x,y), 'coerce': int})

text_rnd.parse()
print(text_rnd.get_text())
```