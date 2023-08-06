# -*- coding: utf-8 -*-
from django.dispatch import Signal

post_proj_save_m2m = Signal(providing_args=['instance'])
pre_comp_prep = Signal(providing_args=['instance'])
post_comp_prep = Signal(providing_args=['instance'])
submission_error = Signal(providing_args=['filename', 'message'])

pre_set_stats = Signal(providing_args=['instance'])
post_set_stats = Signal(providing_args=['instance'])

# Resource signals
post_resource_save = Signal(providing_args=['instance', 'created', 'user'])
post_resource_delete = Signal(providing_args=['instance', 'user'])

# SL Submit Translations signal
pre_submit_translation = Signal(providing_args=['instance'])
post_submit_translation = Signal(providing_args=['request', 'resource', 'language', 'modified'])

# This is obsolete:
sig_refresh_cache = Signal(providing_args=["resource"])
pre_refresh_cache = sig_refresh_cache
post_refresh_cache = Signal(providing_args=["resource"])

# This is obsolete:
sig_clear_cache = Signal(providing_args=["resource"])
pre_clear_cache = sig_clear_cache
post_clear_cache = Signal(providing_args=["resource"])

# Signals used by cla addon:
pre_team_request = Signal(providing_args=['project', 'user'])
pre_team_join = Signal(providing_args=['project', 'user'])
cla_create = Signal(providing_args=['project', 'license_text', 'requester'])
project_access_control_form_start = Signal(providing_args=['instance', 'project'])
class ClaNotSignedError(Exception): pass
