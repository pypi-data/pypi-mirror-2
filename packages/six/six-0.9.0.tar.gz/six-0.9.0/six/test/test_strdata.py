from six import const, strdata


if const.PY3:

    def test_b():
        data = strdata.b("\xff")
        assert isinstance(data, bytes)
        assert len(data) == 1
        assert data == bytes([255])


    def test_u():
        s = strdata.u("hi")
        assert isinstance(s, str)
        assert s == "hi"

else:

    def test_b():
        data = strdata.b("\xff")
        assert isinstance(data, bytes)
        assert len(data) == 1
        assert data == "\xff"


    def test_u():
        s = strdata.u("hi")
        assert isinstance(s, unicode)
        assert s == "hi"


def test_StringIO():
    fp = strdata.StringIO()
    fp.write(strdata.u("hello"))
    assert fp.getvalue() == strdata.u("hello")


def test_BytesIO():
    fp = strdata.BytesIO()
    fp.write(strdata.b("hello"))
    assert fp.getvalue() == strdata.b("hello")
