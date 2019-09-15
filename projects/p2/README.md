# P2: First Flask App - Poke-Info

**Assigned**: Week 3, September 15th

**Due**: Week 5, September 27th, 2019, 11:59 PM

**Late Deadline**: One day after due date, for 10% off: September 28th, 2019, 11:59 PM

## Description

You will be creating a website allowing users to pick a Pokemon and get more info
about the pokemon, as well as to see which pokemon have a certain ability.

## Setup

Activate your virtual environment, and `pip install Flask requests` if you haven't already.

Optionally, `pip install python-dotenv` to easily set environment variables when working.
For more info on how `python-dotenv` works, look at the end of the week 2 lecture.

## Project

In `model.py`, we've defined a class named `PokeClient`. In `app.py`, we create
an instance of the class. This is the only instance of the class that you need.
You **should not** modify the `PokeClient` class. Look at the methods in the 
class definition; you can call these methods with dot syntax, i.e. `poke_client.get_pokemon_list()`
or `poke_client.get_pokemon_info(self, 'bulbasaur')`.

We provided a `base.html` file from which you should extend all of your other templates.
There's an example `index.html` file that just displays `"Poke-Info website!"` when
the website is first opened. 

Implement the following functions with the corresponding routes:

1. `index()` - Should show a list of all Pokemon, with links to pages that give more info

    The list of pokemon should be seen at least at `/`.
    Each element in the list should be a link to another page which will give more info about
    the chosen Pokemon with a certain name.
    The other page should be located at `/pokemon/<pokemon_name>`.
    You can get a list of Pokemon names with the `get_pokemon_list` method of the 
    `PokeClient` class.

2. `pokemon_info(name)` - Should show all info about the specified Pokemon. 

    We should be able to navigate to `/pokemon/<pokemon_name>` and see info about the Pokemon
    identified by `name`. The info includes the name, weight, and other things. The
    `get_pokemon_info` method of the `PokeClient` class returns a dictionary with all of the
    info that you need. The dictionary of info will have a list of names of abilities.
    Each of these abilities must be presented as a clickable link to another page,
    located at `/ability/<ability_name>`.

    There should be a clearly visible link to go back to the front-page of the website, located
    at `/`, or another route that you choose.

3. `pokemon_with_ability(ability)` - Should show a list of Pokemon who have the specified ability.

    We should be able to navigate to `/ability/<ability_name>` and see a list of Pokemon names
    identifying Pokemon that have the specified ability. The `get_pokemon_with_ability` method of
    the `PokeClient` class returns a list of Pokemon names with the ability. The list of
    Pokemon names should be presented as a series of clickable links that will take the 
    website user to the info page for that Pokemon, located at `/pokemon/<pokemon_name>`.

    There should be a clearly visible link to go back to the front-page of the website, located
    at `/`, or another route that you choose.

You will find the `<ul>` and `<ol>` combined with the `<li>` HTML tag useful.

`<ul>` = Unordered list, bulleted
`<ol>` = Ordered list, numbered or alphabetized

Usage:

```html
<ul>
    <li>List Item 1</li>
    <li>List Item 2</li>
</ul>

<ol>
    <li>List Item 1</li>
    <li>List Item 2</li>
</ol>
```

Otherwise, all the tools and functions you need are imported, provided, or used
in the app created in the week 2 lecture directory.

## Testing

Run your flask app, make sure you have a long list of Pokemon names that are links, and try
clicking on some of them to see if the correct info page pops up. Try clicking on one
of the abilities under each Pokemon to see if you get working links to the Pokemon with 
that ability. Check that you have a link clearly visible on the page for Pokemon info and
ability info to go back to the frontpage of our website. 

If you check a few pokemon and abilities throughout the entire list, you should be fine, 
because its fairly certain that your logic is sound at that point.

## Submissions & Grading

Make sure that you've tested parts of your website and that links to the frontpage
exist and are clearly visible, and then zip the `flask_app/` directory, and submit that zip
to the submit server. The submit server will not show test results, but just display "ACCEPTED".

Your project will be graded as follows:

- 10 pts - All Pokemon visible on front page as clickable links
- 10 pts - All Pokemon info returned from the `PokeClient` class is visible on the 
           respective info page.
- 10 pts - All Pokemon names visible and presented as links to Pokemon info pages 
           on the ability pages.
- 10 pts - Link on Pokemon and ability info pages to the front page clearly visible and works.
- 20 pts - Two more templates created for the Pokemon and ability info pages extending `base.html`,
           10 points for each template, 2 total
- 20 pts - Correct routes in app
- 10 pts - `url_for` is used to create the links.
- 10 pts - `Jinja2` control flow statements used to dynamically create HTML in template files.

The project will be graded out of a 100 points. You won't be graded for style, but make
sure your code is readable.




