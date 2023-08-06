#coding: utf-8
import logging

from django.http import HttpResponse, Http404
from django.views.generic.simple import direct_to_template
from django.shortcuts import get_object_or_404

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError: # django < 1.2
    from django.contrib.csrf.middleware import csrf_exempt

from netcash.forms import DataHandlerForm
from netcash.models import NetcashOrder, NetcashGateway
from netcash import signals
from netcash.conf import NETCASH_IP_HEADER

# setup logging
class NullHandler(logging.Handler):
    def emit(self, record):
        pass
logging.getLogger("netcash").addHandler(NullHandler())

@csrf_exempt
def data_handler(request, secret):
    """
    Data URL handler.

    This view is secured by 40-byte random secret string in the URL and
    the ip address limiting.

    On successful access 'netcash.signals.data' signal is sent.
    Orders should be processed in signal handler.
    """

    logger = logging.getLogger("netcash")

    try:
        gateway = NetcashGateway.objects.get(secret=secret)
    except NetcashGateway.DoesNotExist:
        logger.warn('Invalid gateway %s. Request: %s' % (secret, request.raw_post_data))
        raise Http404

    ip = request.META.get(NETCASH_IP_HEADER, None)
    reference = request.POST.get('Reference', None)

    try:
        order = NetcashOrder.objects.get(pk=reference)
    except NetcashOrder.DoesNotExist:
        logger.warn('Unknown order %s. Request: %s' % (reference, request.raw_post_data))
        raise Http404

    if order.trusted: # don't process processed orders again
        logger.warn('Order %s is already processed. Request: %s' % (
                    order.pk, request.raw_post_data))
        raise Http404

    if gateway.netcash_ip:
        # deny query if it come from untrusted ip
        if ip != gateway.netcash_ip:
            order.request_ip = ip
            order.debug_info = 'untrusted ip: %s != %s' % (gateway.netcash_ip, ip)
            order.trusted = False
            order.save()
            raise Http404

    form = DataHandlerForm(request.POST, instance = order)
    if form.is_valid():
        order = form.save(commit=False)
        order.request_ip = ip
        order.gateway = gateway
        order.debug_info = request.raw_post_data
        order.trusted = True
        order.save()
        signals.data.send(sender = data_handler, order=order)
        return HttpResponse()

    # deny query on validation errors
    errors = form.plain_errors()[:255]
    order.debug_info = errors
    order.trusted = False
    order.save()
    return HttpResponse(errors)


@csrf_exempt
def result_handler(request, template_name, extra_context=None):
    """
    Accept or Reject URL handler.

    There is no signing in Netcash protocol and these URLs are
    visible to user so processing orders on Accept/Reject URL access is very
    insecure and must be avoided. That's why django-netcash just renders a
    template and doesn't provide a hook for order processing here.
    """
    reference = request.REQUEST.get('Reference', False)
    order = get_object_or_404(NetcashOrder, pk=reference)
    context = {'order': order}
    context.update(extra_context or {})
    return direct_to_template(request, template_name, context)

