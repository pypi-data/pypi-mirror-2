from django.db.models import ForeignKey
from django.db.models.loading import get_app
from django.db.models.loading import get_models
from dfk.models import DeferredForeignKey

def point(from_model, rel_name, to_model, **fk_kwargs):
    """
    Cause the foreign key `rel_name` on `from_model` to point to
    `to_model`. `fk_kwargs` will be forwarded to the generated
    foreign key.
    """
    assert not to_model._meta.abstract
    deferred_fk = getattr(from_model, rel_name)
    if not isinstance(deferred_fk, DeferredForeignKey):
        raise ValueError, u'You only point a DeferredForeignKey'

    target_model = '%s.%s' % (
        to_model._meta.app_label,
        to_model._meta.object_name
    )

    new_kwargs = deferred_fk.kwargs.copy()
    new_kwargs.update(fk_kwargs)
    new_foreign_key = ForeignKey(
        target_model,
        *deferred_fk.args,
        **new_kwargs
    )
    from_model.add_to_class(rel_name, new_foreign_key)

def point_named(app_name, target_name, to_model, **fk_kwargs):
    # Grab all the models from the app
    if isinstance(app_name, basestring):
        app = get_app(app_name)
    else:
        app = app_name
    models = get_models(app, include_deferred=True)

    # Now look for dfk instances with the target name
    for model in models:
        for attr in dir(model):
            ob = getattr(model, attr)
            if not isinstance(ob, DeferredForeignKey):
                continue

            # We found a deferred foreign key. Check the name
            # to see if it's the one we're processing.
            if getattr(ob, 'name', None) != target_name:
                continue

            # We found a foreign key. Repoint it.
            point(model, attr, to_model, **fk_kwargs)


def repoint(from_model, rel_name, to_model, **kwargs):
    options = getattr(to_model, '_meta', None)
    if options:
        assert not options.abstract, u'Target model may not be abstract'
    field = from_model._meta.get_field(rel_name)
    rel = field.rel
    args = (to_model, rel.field_name)
    new_kwargs = {
        'related_name': rel.related_name,
        'limit_choices_to': rel.limit_choices_to,
        'lookup_overrides': rel.lookup_overrides,
        'parent_link': rel.parent_link
    }
    new_kwargs.update(kwargs)
    new_rel = rel.__class__(*args, **new_kwargs)
    field.rel = new_rel
