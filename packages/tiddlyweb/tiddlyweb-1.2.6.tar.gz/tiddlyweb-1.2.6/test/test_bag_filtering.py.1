"""
Test that things work correctly when attempting to filter
the contents of a bag.
"""

from tiddlyweb.config import config
from tiddlyweb.filters import parse_for_filters
from tiddlyweb import control
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler

from tiddlywebplugins.utils import get_store

from fixtures import reset_textstore, tiddlers


def setup_module(module):
    reset_textstore()
    module.store = get_store(config)
    module.environ = {'tiddlyweb.config': config,
            'tiddlyweb.store': module.store}
    store.put(Bag("foo"))
    tiddler1 = Tiddler("x", "foo")
    tiddler1.tags = ["bar"]
    tiddler2 = Tiddler("y", "foo")
    tiddler2.tags = ["foo", "bar"]
    store.put(tiddler1)
    store.put(tiddler2)
    
def test_filter_bag_by_filter():
    """
    Confirm a bag will properly filter.
    """

    bagfour = Bag('bagfour')
    store.put(bagfour)
    bagfour.store = store
    for tiddler in tiddlers:
        tiddler.bag = 'bagfour'
        store.put(tiddler)

    filtered_tiddlers = list(control._filter_tiddlers_from_bag(bagfour,
        'select=title:TiddlerOne', environ=environ))
    assert len(filtered_tiddlers) == 1
    assert filtered_tiddlers[0].title == 'TiddlerOne'

    filtered_tiddlers = list(control._filter_tiddlers_from_bag(bagfour,
        'select=tag:tagone', environ=environ))
    assert len(filtered_tiddlers) == 2

    filters, thing = parse_for_filters(
            'select=tag:tagone;select=title:TiddlerThree', environ=environ)
    filtered_tiddlers = list(control._filter_tiddlers_from_bag(bagfour,
        filters, environ=environ))
    assert len(filtered_tiddlers) == 1
    assert filtered_tiddlers[0].title == 'TiddlerThree'

def test_recipe_filtering():
  recipe = Recipe('myRecipe')
  recipe.set_recipe([["foo", ""]])
  recipe.store = store

  recipe2 = Recipe('myRecipe2')
  recipe2.set_recipe([["foo", "select=tag:bar"]])
  recipe2.store = store

  recipe3 = Recipe('myRecipe2')
  recipe3.set_recipe([["foo", "select=tag:foo"]])
  recipe3.store = store

  tiddlers = list(control.get_tiddlers_from_recipe(recipe))
  tiddlers2 =  list(control.get_tiddlers_from_recipe(recipe2))
  tiddlers3 =  list(control.get_tiddlers_from_recipe(recipe3))

  assert len(tiddlers) is 2
  assert len(tiddlers2) is 2
  assert len(tiddlers3) is 1
