from django.utils import simplejson
from dynamicresponse.response import *

class DynamicFormatMiddleware:
    """
    Provides support for dynamic content negotiation, both in request  and reponse.
    """
    
    def _flatten_dict(self, obj, prefix=''):
        """
        Converts a possibly nested dictionary to a flat dictionary.
        """
        
        encoded_dict = {}
        if hasattr(obj, 'items'):
            for key, value in obj.items():
            
                item_key = '%(prefix)s%(key)s' % { 'prefix': prefix, 'key': key }
            
                # Decode lists into keys w/index for formset
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        item_prefix = '%(key)s-%(index)d-' % { 'key': key, 'index': i }
                        encoded_dict.update(self._flatten_dict(item, prefix=item_prefix))
                    
                # Decode nested objects into their ID/PK
                elif isinstance(value, dict):
                    encoded_dict[item_key] = value.get('id', value)
            
                # Other values are used directly
                else:
                    encoded_dict[item_key] = unicode(value)
                
        return encoded_dict
        
    def process_request(self, request):
        """"
        Parses the request, decoding JSON payloads to be compatible with forms.
        """
        
        # Does the request contain a JSON payload?
        content_length = request.META.get('CONTENT_LENGTH', 0)
        content_type = request.META.get('CONTENT_TYPE', '')
        if content_length > 0 and content_type != '' and content_type in ('application/json'):

            try:
                # Replace request.POST with flattened dictionary from JSON
                decoded_dict = simplejson.loads(request.raw_post_data)
                request.POST = request.POST.copy()
                request.POST.clear()
                for key, val in self._flatten_dict(decoded_dict).items():
                    request.POST[key] = val
            except:
                return HttpResponse('Invalid JSON', status=400)
            
    def process_response(self, request, response):
        """
        Handles rendering dynamic responses.
        """
        
        # Cause dynamic responses to be rendered
        if isinstance(response, DynamicResponse):
            return response.render_response(request, response)
        
        return response
