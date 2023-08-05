# Copyright (c) 2010 by Yaco Sistemas <msaelices@yaco.es>
#
# This file is part of Merengue.
#
# Merengue is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Merengue is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Merengue.  If not, see <http://www.gnu.org/licenses/>.


from south.db import db
from django.db import models
from merengue.places.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table('places_location', (
            ('id', orm['places.Location:id']),
            ('main_location', orm['places.Location:main_location']),
            ('borders', orm['places.Location:borders']),
            ('address', orm['places.Location:address']),
            ('postal_code', orm['places.Location:postal_code']),
        ))
        db.send_create_signal('places', ['Location'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table('places_location')
        
    
    
    models = {
        'places.location': {
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'borders': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['places']
