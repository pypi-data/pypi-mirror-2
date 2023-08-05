'''
Created on 28.12.2009

@author: FladischerMichael <FladischerMichael@fladi.at>

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, 
   this list of conditions and the following disclaimer in the documentation 
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND ANY 
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGE.
'''

from django.db import models
import urllib2
import libxml2
import GeoIP

class Base(models.Model):
    published = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Stream(Base):
    name = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name
      
class Server(Base):
    hostname = models.CharField(max_length=512)
    port = models.IntegerField()
    country = models.CharField(max_length=4,null=True,blank=True)
    def __unicode__(self):
        return "http://%s:%i" % (self.hostname, self.port)
    def save(self, force_insert=False, force_update=False):
        geo = GeoIP.open("/usr/share/GeoIP/GeoIP.dat", GeoIP.GEOIP_STANDARD)
        self.country = geo.country_code_by_name(self.hostname)
        super(Server, self).save(force_insert, force_update)
        mounts = Mount.objects.filter(server=self)
        if len(mounts) > 0:
            try:
                doc = libxml2.parseDoc(urllib2.urlopen("%s/load.xsl" % (self)).read())
                for mount in mounts:
                    nodes = doc.xpathEval("/load/mount[@name='/%s']" % (mount.name))
                    if len(nodes) is 1:
                        mount.slots = int(nodes[0].content)
                    else:
                        mount.slots = 0
                    mount.save()
            except:
                for mount in mounts:
                    mount.slots = 0
                    mount.save()
      
class Mount(Base):
    stream = models.ForeignKey(Stream)
    server = models.ForeignKey(Server)
    name = models.CharField(max_length=512)
    slots = models.IntegerField(default=0)
    def __unicode__(self):
        return "%s/%s" % (self.server, self.name)    
