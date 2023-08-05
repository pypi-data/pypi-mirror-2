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

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseRedirect
from icecast_balancer.models import Stream, Mount

def index(request):
    streams = Stream.objects.all().order_by('name')
    return render_to_response('icecast_balancer/index.html', {'streams': streams})

def go(request, stream):
    instance = get_object_or_404(Stream, name=stream)
    if 'GEOIP_COUNTRY_CODE' in request.META:
        mounts = Mount.objects.filter(stream=instance, slots__gt=0, server__country=request.META['GEOIP_COUNTRY_CODE']).order_by('-slots')
        if len(mounts) is 0:
            mounts = Mount.objects.filter(stream=instance, slots__gt=0).order_by('-slots')
    else:
        mounts = Mount.objects.filter(stream=instance, slots__gt=0).order_by('-slots')
    if len(mounts) > 0:
        return HttpResponseRedirect(mounts[0])
    else:
        return HttpResponseNotFound("No relay available at the moment. Please try again later.")