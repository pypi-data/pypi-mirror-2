'''
Created on 25.03.2010

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
from django.core.management.base import BaseCommand
from django.conf import settings
from icecast_balancer.models import Server

class Command(BaseCommand):
    """Poll all icecast instances."""
    option_list = BaseCommand.option_list
    help = 'Poll all icecast instances.'

    def handle(self, *args, **options):
        """Handle the management command."""
        if 'celery' in settings.INSTALLED_APPS:
            # Use the celery task to update the servers asynchronously
            from icecast_balancer.tasks import poll_icecast_server
            for server in Server.objects.all():
                poll_icecast_server.delay(server)
        else:
            # Update the servers the conventional way
            for server in Server.objects.all():
                server.save()
