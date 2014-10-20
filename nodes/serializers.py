from rest_framework import serializers
#import common.lib as clib

"""
The basic idea is that we have nodes and their resources.
Nodes can be hierarchical.

Everything is build around one record with different types. Every record
can have own data: that is python dict.

Each resource can have special field - tag. We are able to find node's resource
by tag without specifying id.

Specific node type must inherit NodeSerializer, specify it's own type, specify 
serializer for data.
"""

class NodeSerializer(serializers.Serializer):
    uid = serializers.IntegerField(required=True, min_value=1)
    gid = serializers.IntegerField(required=True, min_value=1)
    # Can be of different types. Like google appengine.
    ntype = serializers.CharField(required=True, max_length=15)
    #timestamp
    created = serializers.DateTimeField(auto_now_add=True, read_only=True)
    #timestamp
    updated = serializers.DateTimeField(auto_now=True, read_only=True)
    #unix permission.
    perm = 
    # Parent node.
    pnid
    # typical access level.
    access_level
    # Shared to uids.
    shared
    # Some data - python dict.
    data
    # Tag = specific to resources only.
    tag = 



