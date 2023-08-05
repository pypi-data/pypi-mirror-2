from django.test import TestCase

'''
LayarView
    - verify_hash
    - invalid layer name
    - pagination
    - content_type
'''

class POITest(TestCase):

    def test_lat_lon_conversion(self):
        p = POI('id', 44.501, 55.005, 'title')
        d = p.to_dict()
        self.assert_(isinstance(p.lat, float))
        self.assert_(isinstance(p.lon, float))
        self.assert_(isinstance(d['lat'], int))
        self.assert_(isinstance(d['lon'], int))

    def test_str_id(self):
        p = POI(102, 33.5, 33.5, 'title')
        d = p.to_dict()
        self.assertEqual(d['id'] == str(p.id))

    def test_actions_dict(self):
        p = POI('id', 33.5, 33.5, 'title', actions={'call':'tel://555-555-555',
                                                    'link':'http://example.com'})
        d = p.to_dict()
        self.assert_(isinstance(d.actions, dict))
        self.assert_(isinstance(d['actions'], list))

if __name__ == '__main__':
    import unittest
    unittest.main()
