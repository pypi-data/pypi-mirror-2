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

from icecast_balancer.models import Stream, Server, Mount
from django.contrib import admin

class StreamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    list_display = ('id', 'name', 'modified')
    list_filter = ['name', 'modified']
    search_fields = ['name']
    date_hierarchy = 'modified'

admin.site.register(Stream, StreamAdmin)

class ServerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['hostname', 'port', 'country']}),
    ]
    list_display = ('id', 'hostname', 'port', 'country')
    list_filter = ['hostname', 'port', 'country']
    search_fields = ['hostname', 'port']
    date_hierarchy = 'published'

admin.site.register(Server, ServerAdmin)

class MountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['stream', 'server', 'name']}),
    ]
    list_display = ('id', 'stream', 'server', 'name', 'slots', 'modified')
    list_filter = ['stream', 'server', 'name', 'modified']
    search_fields = ['server', 'stream', 'name']
    date_hierarchy = 'modified'

admin.site.register(Mount, MountAdmin)
