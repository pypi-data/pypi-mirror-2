import uuid

import datautil.id

def test_compress_and_uncompress_uuid():
    hexversion = '86c3f19d-8854-4ef5-8d88-f008e0817871'

    out = datautil.id.compress_uuid(hexversion)
    assert len(out) == 22

    orig = datautil.id.uncompress_uuid(out)
    assert orig == hexversion

    # test unicode
    orig = datautil.id.uncompress_uuid(unicode(out))
    assert orig == hexversion

    u1 = uuid.UUID(hexversion)
    out = datautil.id.compress_uuid(u1)
    assert len(out) == 22


def test_int_to_b32():
    def check(int_):
        out = datautil.id.int_to_b32(int_)
        assert isinstance(out, basestring)
        assert len(out) == 7, out

        back = datautil.id.b32_to_int(out)
        assert back == int_, (int_,back)

    check(1)
    check(2**28+1)
    check(2**30-1)

