from sdfspu.sdf_text import randstring, split_name, obsc_email, path_is_url


def test_randstring():
    assert isinstance(randstring(), str)
    assert len(randstring(k_=20)) == 20
    assert len(randstring(k_=120)) == 120
    assert ' ' not in randstring()


def test_split_name():
    assert split_name('ok simple') == ('ok', 'simple')
    assert split_name('solo') == ('', 'solo')
    assert split_name('three part name') == ('three part', 'name')
    assert split_name('name with-hyphen') == ('name', 'with-hyphen')
    assert split_name('') == ('', '')


def test_obsc_email():
    assert obsc_email('something@example.com') == 'som...@e...'


def test_path_is_url():
    assert path_is_url('https://github.com/soundmaking/sdfspu')
    assert not path_is_url('/home/pi/gitclones/sdfspu/tests/test_sdf_text.py')
