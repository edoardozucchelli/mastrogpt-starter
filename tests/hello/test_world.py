import sys
sys.path.append("packages/hello/world")
import world

def test_world():
    args = {}
    res = world.world(args)
    assert res["output"] == "Hi, world"
    
    args = {"input": "Mike"}
    res = world.world(args)
    assert res["output"] == "Hi, Mike"
