""" This module includes unit tests for protocol.py using PostGIS as database"""

import unittest
from nose.tools import eq_, ok_, raises

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, MetaData, Column, Integer, Numeric)
from sqlalchemy import orm

from geoalchemy import (Point, Polygon, GeometryColumn, GeometryDDL)

from mapfish.sqlalchemygeom import GeometryTableMixIn
from mapfish.protocol import Protocol, create_geom_filter,\
    create_default_filter
from test_protocol import FakeRequest, FakeResponse

from webob.exc import HTTPNotFound
from exceptions import Exception
from geojson import Feature, FeatureCollection, GeoJSON
import os
from sqlalchemy.schema import Sequence
from sqlalchemy.sql.expression import text, select


os.environ['ORACLE_HOME'] = '/usr/lib/oracle/xe/app/oracle/product/10.2.0/server'
os.environ['LD_LIBRARY'] = '/usr/lib/oracle/xe/app/oracle/product/10.2.0/server/lib'

import cx_Oracle

#engine = create_engine('oracle://gis:gis@localhost:1521/gis', echo=True)
engine = create_engine('oracle://system:system@172.16.103.134:1521/gis', echo=True)

metadata = MetaData(engine)
sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)
session = orm.scoped_session(sm)


Base = declarative_base(metadata=metadata)

diminfo = "MDSYS.SDO_DIM_ARRAY("\
            "MDSYS.SDO_DIM_ELEMENT('LONGITUDE', -180, 180, 0.000000005),"\
            "MDSYS.SDO_DIM_ELEMENT('LATITUDE', -90, 90, 0.000000005)"\
            ")"

class Spot(Base, GeometryTableMixIn):
    __tablename__ = 'spots_mf'

    spot_id = Column(Integer, Sequence('spots_mf_id_seq'), primary_key=True)
    spot_height = Column(Numeric(precision=10, scale=2, asdecimal=False)) 
    spot_location = GeometryColumn(Point(2, diminfo=diminfo))

GeometryDDL(Spot.__table__)

class Lake(Base, GeometryTableMixIn):
    __tablename__ = 'lakes_mf'

    id = Column(Integer, Sequence('lakes_mf_id_seq'), primary_key=True)
    depth = Column(Numeric(precision=10, scale=2, asdecimal=False))
    geom = GeometryColumn(Polygon(2, diminfo=diminfo))

GeometryDDL(Lake.__table__)

class Test(unittest.TestCase):


    def setUp(self):
 
        metadata.drop_all()
        metadata.create_all()

        # Insert some points into the database
        session.add_all([
            Spot(spot_height=420.40, spot_location='POINT(0 0)'),
            Spot(spot_height=102.34, spot_location='POINT(10 10)'),
            Spot(spot_height=388.62, spot_location='POINT(10 11)'),
            Spot(spot_height=1454.66, spot_location='POINT(40 34)'),
            Spot(spot_height=54.66, spot_location='POINT(5 5)'),
            Spot(spot_height=333.12, spot_location='POINT(2 3)'),
            Spot(spot_height=783.55, spot_location='POINT(38 34)'),
            Spot(spot_height=3454.67, spot_location='POINT(-134 45)'),
            Spot(spot_height=6454.23, spot_location='POINT(-135 56)')
            ])
        
        session.commit()
        

    def tearDown(self):
        session.rollback()
        metadata.drop_all()
        

    def test_protocol_create(self):
        """Create a new point"""
        proto = Protocol(session, Spot)
        
        request = FakeRequest({})
        request.body = '{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"spot_height": 12.0}, "geometry": {"type": "Point", "coordinates": [45, 5]}}]}'
        
        response = FakeResponse()
        collection = proto.create(request, response)
        eq_(response.status, 201)
        eq_(len(collection.features), 1)
        feature0 = collection.features[0]
        eq_(feature0.id, 10)
        eq_(feature0.geometry.coordinates, (45.0, 5.0))
        eq_(feature0.properties["spot_height"], 12)

        new_spot = session.query(Spot).filter(Spot.spot_height==12.0).one()
        ok_(new_spot is not None)
        eq_(session.scalar(new_spot.spot_location.wkt), u'POINT (45.0 5.0)')
        

    def test_protocol_create_and_update(self):
        """Create a new point and also update an already existing point"""
        
        old_spot = session.query(Spot).filter(Spot.spot_height==102.34).one()
        
        proto = Protocol(session, Spot)
        
        request = FakeRequest({})
        request.body = '{"type": "FeatureCollection", "features": [\
            {"type": "Feature", "properties": {"spot_height": 12.0}, "geometry": {"type": "Point", "coordinates": [45, 5]}},\
            {"type": "Feature", "id": ' + str(old_spot.spot_id) + ', "properties": {}, "geometry": {"type": "Point", "coordinates": [1, 1]}}]}'       
        
        response = FakeResponse()
        collection = proto.create(request, response)
        eq_(response.status, 201)
        eq_(len(collection.features), 2)
        feature0 = collection.features[0]
        eq_(feature0.id, 10)
        eq_(feature0.geometry.coordinates, (45.0, 5.0))
        eq_(feature0.properties["spot_height"], 12)
        feature1 = collection.features[1]
        eq_(feature1.id, old_spot.spot_id)
        eq_(feature1.geometry.coordinates, (1, 1))

        new_spot = session.query(Spot).filter(Spot.spot_height==12.0).one()
        ok_(new_spot is not None)
        eq_(session.scalar(new_spot.spot_location.wkt), u'POINT (45.0 5.0)')
        
        updated_spot = session.query(Spot).filter(Spot.spot_height==102.34).one()
        ok_(updated_spot is not None)
        ok_(old_spot is updated_spot)
        eq_(updated_spot.spot_height, 102.34)
        eq_(session.scalar(updated_spot.spot_location.wkt), u'POINT (1.0 1.0)')
        

    @raises(Exception)
    def test_protocol_create_fails(self):
        """Try to create a feature without geometry"""
        proto = Protocol(session, Spot)
        
        request = FakeRequest({})
        request.body = '{"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"spot_height": 12.0}}]}'
        
        proto.create(request, FakeResponse())
        

    def test_protocol_update(self):
        """Update an existing point"""
        proto = Protocol(session, Spot)
        id = 1
        
        request = FakeRequest({})
        request.body = '{"type": "Feature", "id": ' + str(id) + ', "properties": {}, "geometry": {"type": "Point", "coordinates": [1, 1]}}'
        
        response = FakeResponse()
        feature = proto.update(request, response, id)
        eq_(response.status, 201)
        eq_(feature.id, 1)
        eq_(feature.geometry.coordinates, (1.0, 1.0))
        
        spot = session.query(Spot).get(id)
        ok_(spot is not None)
        eq_(session.scalar(spot.spot_location.wkt), u'POINT (1.0 1.0)')
        
        
    @raises(HTTPNotFound)
    def test_protocol_update_fails(self):
        """Try to update a not-existing feature"""
        proto = Protocol(session, Spot)
        id = -1
        
        request = FakeRequest({})
        request.body = '{"type": "Feature", "id": ' + str(id) + ', "properties": {}, "geometry": {"type": "Point", "coordinates": [1, 1]}}'
        
        response = FakeResponse()
        proto.update(request, response, id)
        

    def test_protocol_delete(self):
        """Delete an existing point"""
        proto = Protocol(session, Spot)
        id = 1
        
        request = FakeRequest({})
        response = FakeResponse()
        
        proto.delete(request, response, id)
        eq_(response.status, 204)
        
        spot = session.query(Spot).get(id)
        ok_(spot is None)
        

    @raises(HTTPNotFound)
    def test_protocol_delete_fails(self):
        """Try to delete a not-existing point"""
        proto = Protocol(session, Spot)
        
        proto.delete(FakeRequest({}), FakeResponse(), -1)
        

    def test_protocol_count(self):
        """Get the feature count"""
        proto = Protocol(session, Spot)
        
        eq_(proto.count(FakeRequest({})), '9')
        

    def test_protocol_count_filter_box(self):
        """Get the feature count with a box as filter"""
        proto = Protocol(session, Spot)
        request = FakeRequest({})
        
        request.params['bbox'] = '-10,-10,10,10'
        eq_(proto.count(request), '4')
        
        request.params['tolerance'] = '200000'
        eq_(proto.count(request), '5')
        
        # query features that are inside a bbox that uses a different CRS
        # note that we either have to specify a tolerance ('tol') or 
        # dimension information ('dim1' and 'dim2')
        filter = create_default_filter(request, Spot, additional_params={'tol': '0.005'})
        request.params['bbox'] = '-12.3364241712925,-10.0036833569465,7.66304367998925,9.9979519038951'
        request.params['epsg'] = '2210'
        request.params['tolerance'] = '0'
        eq_(proto.count(request, filter=filter), '5')
        
        # dimension information array for 54004
        # see http://download.oracle.com/docs/cd/E11882_01/appdev.112/e11830/sdo_objrelschema.htm#i1010905
        diminfo = "MDSYS.SDO_DIM_ARRAY("\
            "MDSYS.SDO_DIM_ELEMENT('LONGITUDE', -20037508, 20037508, 0.005),"\
            "MDSYS.SDO_DIM_ELEMENT('LATITUDE', -19929239, 19929239, 0.005)"\
            ")"
        
        request.params['bbox'] = '-975862.822682856,-999308.345117013,1027887.98627823,999373.702609189'
        request.params['epsg'] = '54004' # Oracles SRID number for World Mercator
        filter = create_default_filter(request, Spot, 
                                       additional_params={'dim1': text(diminfo),
                                                          'dim2' : text(diminfo)})
        eq_(proto.count(request, filter=filter), '3')
        

    def test_protocol_count_filter_within(self):
        """Get the feature count with a point as filter"""
        proto = Protocol(session, Spot)
        request = FakeRequest({})
        
        request.params['lat'] = '0'
        request.params['lon'] = '0'
        eq_(proto.count(request), '1')
        
        request.params['tolerance'] = '400000'
        eq_(proto.count(request), '2')
        
        filter = create_default_filter(request, Spot, additional_params={'params': 'unit=KM'})
        eq_(proto.count(request, filter=filter), '9')
        

    def test_protocol_count_filter_geometry(self):
        """Get the feature count with a geometry as filter"""
        proto = Protocol(session, Spot)
        request = FakeRequest({})
        
        request.params['geometry'] = '{"type": "Polygon", "coordinates": [[ [-10, -1], [10, -1], [0, 10], [-10, -1] ]]}'
        eq_(proto.count(request), '2')
        
        request.params['tolerance'] = '200000'
        eq_(proto.count(request), '3')
        

    def test_protocol_count_queryable(self):
        """Count all features that match a filter"""
        proto = Protocol(session, Spot)
        request = FakeRequest({})
        request.params['queryable'] = 'spot_height'
        request.params['spot_height__gte'] = '1454.66'
        
        eq_(proto.count(request), '3')
        

    def test_protocol_count_custom_filter(self):
        """Count all features that match a custom filter"""
        session.add_all([
            Lake(depth=20, geom='POLYGON((-88.7968950764331 43.2305732929936,-88.7935511273885 43.1553344394904,-88.716640299363 43.1570064140127,-88.7250001719745 43.2339172420382,-88.7968950764331 43.2305732929936))'),
            Lake(depth=5, geom='POLYGON((-88.1147292993631 42.7540605095542,-88.1548566878981 42.7824840764331,-88.1799363057325 42.7707802547771,-88.188296178344 42.7323248407643,-88.1832802547771 42.6955414012739,-88.1565286624204 42.6771496815287,-88.1448248407643 42.6336783439491,-88.131449044586 42.5718152866242,-88.1013535031847 42.565127388535,-88.1080414012739 42.5868630573248,-88.1164012738854 42.6119426751592,-88.1080414012739 42.6520700636943,-88.0980095541401 42.6838375796178,-88.0846337579618 42.7139331210191,-88.1013535031847 42.7423566878981,-88.1147292993631 42.7540605095542))'),
            Lake(depth=120, geom='POLYGON((-89.0694267515924 43.1335987261147,-89.1078821656051 43.1135350318471,-89.1329617834395 43.0884554140127,-89.1312898089172 43.0466560509554,-89.112898089172 43.0132165605096,-89.0694267515924 42.9898089171975,-89.0343152866242 42.953025477707,-89.0209394904459 42.9179140127389,-89.0042197452229 42.8961783439491,-88.9774681528663 42.8644108280255,-88.9440286624204 42.8292993630573,-88.9072452229299 42.8142515923567,-88.8687898089172 42.815923566879,-88.8687898089172 42.815923566879,-88.8102707006369 42.8343152866242,-88.7734872611465 42.8710987261147,-88.7517515923567 42.9145700636943,-88.7433917197452 42.9730891719745,-88.7517515923567 43.0299363057325,-88.7734872611465 43.0867834394905,-88.7885352038217 43.158678388535,-88.8738057324841 43.1620222929936,-88.947372611465 43.1937898089172,-89.0042197452229 43.2138535031847,-89.0410031847134 43.2389331210191,-89.0710987261147 43.243949044586,-89.0660828025478 43.2238853503185,-89.0543789808917 43.203821656051,-89.0376592356688 43.175398089172,-89.0292993630573 43.1519904458599,-89.0376592356688 43.1369426751592,-89.0393312101911 43.1386146496815,-89.0393312101911 43.1386146496815,-89.0510350318471 43.1335987261147,-89.0694267515924 43.1335987261147))'),
            Lake(depth=450, geom='POLYGON((-88.9122611464968 43.038296178344,-88.9222929936306 43.0399681528663,-88.9323248407643 43.0282643312102,-88.9206210191083 43.0182324840764,-88.9105891719745 43.0165605095542,-88.9005573248408 43.0232484076433,-88.9072452229299 43.0282643312102,-88.9122611464968 43.038296178344))')
            ])
        session.commit();
        
        proto = Protocol(session, Lake)
        
        from sqlalchemy.sql import and_
        
        request = FakeRequest({})
        request.params['bbox'] = '-90,40,-80,45'
        
        filter = create_geom_filter(request, Lake)
        
        compare_filter = Lake.geom.area >= 0.1
        filter = and_(filter, compare_filter)
            
        eq_(proto.count(request, filter=filter), '3')


    def test_protocol_read_all(self):
        """Return all features"""
        proto = Protocol(session, Spot)

        collection = proto.read(FakeRequest({}))
        ok_(collection is not None)
        ok_(isinstance(collection, FeatureCollection))
        eq_(len(collection.features), 9)


    def test_protocol_read_one(self):
        """Return one feature"""
        proto = Protocol(session, Spot)

        feature = proto.read(FakeRequest({}), id=1)
        ok_(feature is not None)
        ok_(isinstance(feature, Feature))
        eq_(feature.id, 1)
        eq_(feature.geometry.coordinates, (0.0, 0.0))
        eq_(feature.properties["spot_height"], 420.39999999999998)


    @raises(HTTPNotFound)
    def test_protocol_read_one_fails(self):
        """Try to get a single point with a wrong primary key"""
        proto = Protocol(session, Spot)
        
        proto.read(FakeRequest({}), id=-1)


    def test_within_distance(self):
        """Test the Oracle implementation for within_distance
        
        Because SDO_WITHIN_DISTANCE requires a spatial index for the geometry used
        as first parameter, we have to insert out test geometries into tables,
        unlike to the other databases.
        
        Note that Oracle uses meter as unit for the tolerance value for geodetic coordinate
        systems (like 4326)!
        """
        from mapfish.sqlalchemygeom import within_distance
        
        # test if SDO_WITHIN_DISTANCE is called correctly
        eq_(session.query(Spot).filter(within_distance(Spot.spot_location, 'POINT(0 0)', 0)).count(), 1)
        eq_(session.query(Spot).filter(within_distance(Spot.spot_location, 'POINT(0 0)', 0.1)).count(), 1)
        eq_(session.query(Spot).filter(within_distance(Spot.spot_location, 'POINT(9 9)', 100000)).count(), 0)
        
        eq_(session.query(Spot).filter(within_distance(Spot.spot_location, 
                                                       'Polygon((-5 -5, 5 -5, 5 5, -5 5, -5 -5))', 0)).count(), 3)
        
        eq_(session.query(Spot).filter(within_distance(Spot.spot_location, 
                                                       'Polygon((-10 -10, 10 -10, 10 10, -10 10, -10 -10))', 0)).count(), 4)
        
        eq_(session.query(Spot).filter(within_distance(Spot.spot_location, 
                                                       'Polygon((-10 -10, 10 -10, 10 10, -10 10, -10 -10))', 200000)).count(), 5)

        # test if SDO_GEOM.WITHIN_DISTANCE is called correctly
        eq_(session.scalar(select([text('1')], from_obj=['dual']).where(
                                                    within_distance('POINT(0 0)', 'POINT(0 0)', 0, 
                                                                    {'tol' : 0.00000005}))), 1)
        eq_(session.scalar(select([text('1')], from_obj=['dual']).where(
                                                    within_distance('POINT(0 0)', 'POINT(0 0)', 0, 
                                                                    {'dim1' : text(diminfo),
                                                                     'dim2' : text(diminfo)}))), 1)
