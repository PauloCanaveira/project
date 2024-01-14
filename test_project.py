import numpy as np
from project import cf_m, cf_g, cf_p, is_pregnant

def test_cf_m():
    assert cf_m(1000, "female", "yes", "no") == 0.386
    assert cf_m(1000, "male", "no", "no") == 0.370
    assert cf_m(731, "male", "no", "no") == 0.370
    assert cf_m(730, "male", "no", "no") == 0.322
    assert cf_m(1000, "male-castrate", "no", "yes") == 0.322
    assert cf_m(1000, "female", "no", "no") == 0.322

def test_cf_g():
    assert cf_g("female", "no") == 0.8
    assert cf_g("male-castrate", "yes") == 1
    assert cf_g("male", "no") == 1.2

def test_cf_p():
    assert cf_p("yes", "female") == 0.1
    assert cf_p("no", "male") == 0
    assert cf_p("no", "female") == 0
    assert cf_p("no", "male-castrate") == 0
    
def test_is_pregnant():
    age = np.arange(1, 7301)
    result = is_pregnant(age)
    assert result[545] == "no"
    assert result[546] == "yes"
    assert result[829] == "yes"
    assert result[830] == "no"
    assert result[972] == "no"
    assert result[973] == "yes"
